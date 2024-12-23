#!/usr/bin/env python3
# pip install -U google-generativeai
# pip install assemblyai

import cachetools.func
import os
import random
import subprocess
import threading
import traceback
from io import BytesIO

import speech_recognition as sr
import assemblyai as aai
from pydub import AudioSegment

import cfg
import my_db
import my_groq
import my_transcribe
import my_log
import utils


# locks for chat_ids
LOCKS = {}


DEFAULT_STT_ENGINE = cfg.DEFAULT_STT_ENGINE if hasattr(cfg, 'DEFAULT_STT_ENGINE') else 'whisper' # 'gemini', 'google', 'assembly.ai'


def audio_duration(audio_file: str) -> int:
    """
    Get the duration of an audio file.

    Args:
        audio_file (str): The path to the audio file.

    Returns:
        int: The duration of the audio file in seconds.
    """
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', audio_file], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        r = float(result.stdout)
    except ValueError:
        r = 0
    try:
        r = int(r)
    except ValueError:
        r = 0
    return r


def convert_to_ogg_with_ffmpeg(audio_file: str) -> str:
    """
    Converts an audio file to a ogg format using FFmpeg.

    Args:
        audio_file (str): The path to the audio file to be converted.

    Returns:
        str: The path to the converted wave file.
    """
    tmp_wav_file = utils.get_tmp_fname() + '.ogg'
    subprocess.run(['ffmpeg', '-i', audio_file, '-map', '0:a', '-c:a','libvorbis', tmp_wav_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return tmp_wav_file


@cachetools.func.ttl_cache(maxsize=10, ttl=1 * 60)
def stt_google(audio_file: str, language: str = 'ru') -> str:
    """
    Speech-to-text using Google's speech recognition API.
    
    Args:
        audio_file (str): The path to the audio file to be transcribed.
        language (str, optional): The language of the audio file. Defaults to 'ru'.
    
    Returns:
        str: The transcribed text from the audio file.
    """
    google_recognizer = sr.Recognizer()

    audio = AudioSegment.from_file(audio_file)
    # Сохраняем сегмент в BytesIO
    wav_bytes = BytesIO()
    audio.export(wav_bytes, format="wav")
    wav_bytes.seek(0)

    with sr.AudioFile(wav_bytes) as source:
        audio = google_recognizer.record(source)  # read the entire audio file

    text = google_recognizer.recognize_google(audio, language=language)

    return text


def stt(input_file: str, lang: str = 'ru', chat_id: str = '_', prompt: str = '') -> str:
    """
    Generate the function comment for the given function body in a markdown code block with the correct language syntax.

    Args:
        input_file (str): The path to the input file.
        lang (str, optional): The language for speech recognition. Defaults to 'ru'.
        chat_id (str, optional): The ID of the chat. Defaults to '_'.

    Returns:
        str: The recognized speech as text.
    """
    speech_to_text_engine = my_db.get_user_property(chat_id, 'speech_to_text_engine') or DEFAULT_STT_ENGINE
    if chat_id not in LOCKS:
        LOCKS[chat_id] = threading.Lock()
    with LOCKS[chat_id]:
        text = ''

        dur = audio_duration(input_file)
        input_file2 = convert_to_ogg_with_ffmpeg(input_file)

        done_flag = False

        try:
            # first try google if short
            if dur < 30:
                # быстро и хорошо распознает но до 1 минуты всего
                # и часто глотает последнее слово
                try:
                    text = stt_google(input_file2, lang)
                    if text and not done_flag:
                        done_flag = True
                        my_db.add_msg(chat_id, 'STT google-free')
                except Exception as unknown_error:
                    my_log.log2(str(unknown_error))
            
            if not text:
                # try first shot from config
                if speech_to_text_engine == 'whisper':
                    text = my_groq.stt(input_file2, lang, prompt=prompt, model = 'whisper-large-v3')
                    if text and not done_flag:
                        done_flag = True
                        my_db.add_msg(chat_id, 'STT whisper-large-v3')
                elif speech_to_text_engine == 'gemini':
                    try: # gemini
                        text = stt_genai(input_file2, lang)
                        if text and not done_flag:
                            done_flag = True
                            my_db.add_msg(chat_id, cfg.gemini_flash_model)
                    except Exception as error:
                        my_log.log2(f'my_stt:stt:genai:{error}')
                elif speech_to_text_engine == 'google':
                    text = my_transcribe.stt_google_pydub_v2(input_file2, lang = lang)
                    if text:
                        my_db.add_msg(chat_id, 'STT google-free')
                elif speech_to_text_engine == 'assembly.ai':
                    text = assemblyai(input_file2, lang)
                    if text and not done_flag:
                        done_flag = True
                        my_db.add_msg(chat_id, 'STT assembly.ai')

            if not text and dur < 60:
                text = my_groq.stt(input_file2, lang, prompt=prompt, model = 'whisper-large-v3-turbo')
                if text and not done_flag:
                    done_flag = True
                    my_db.add_msg(chat_id, 'STT whisper-large-v3-turbo')

            if not text and dur < 55:
                # быстро и хорошо распознает но до 1 минуты всего
                # и часто глотает последнее слово
                try: # пробуем через гугл
                    text = stt_google(input_file2, lang)
                    if text and not done_flag:
                        done_flag = True
                        my_db.add_msg(chat_id, 'STT google-free')
                except Exception as unknown_error:
                    my_log.log2(str(unknown_error))

            if not text:
                try: # gemini
                    # может выдать до 8000 токенов (30000 русских букв) более чем достаточно для голосовух
                    # у него в качестве fallback используется тот же гугл но с разбиением на части
                    text = stt_genai(input_file2, lang)
                    if text and not done_flag:
                        done_flag = True
                        my_db.add_msg(chat_id, cfg.gemini_flash_model)
                    if len(text) < 100: # failed?
                        done_flag = False
                        my_log.log2(f'my_stt:stt: stt_genai failed long file, trying groq')
                        text = my_groq.stt(input_file2, lang, prompt=prompt, model = 'whisper-large-v3-turbo') or text
                        if text and not done_flag:
                            done_flag = True
                            my_db.add_msg(chat_id, 'STT whisper-large-v3-turbo')
                        if len(text) < 100: # failed?
                            my_log.log2(f'my_stt:stt: stt groq failed long file, trying assemblyai')
                            text = assemblyai(input_file2, lang) or text
                            if text and not done_flag:
                                done_flag = True
                                my_db.add_msg(chat_id, 'STT assembly.ai')
                except Exception as error:
                    my_log.log2(f'my_stt:stt:genai:{error}')

            if not text:
                text = my_groq.stt(input_file2, lang, prompt=prompt, model = 'whisper-large-v3')
                if text and not done_flag:
                    done_flag = True
                    my_db.add_msg(chat_id, 'STT whisper-large-v3')

            if not text:
                text = assemblyai(input_file2, lang)
                if text and not done_flag:
                    done_flag = True
                    my_db.add_msg(chat_id, 'STT assembly.ai')

        finally:
            utils.remove_file(input_file2)

        if text and len(text) > 1:
            return text

    return ''


def stt_genai_worker(audio_file: str, part: tuple, n: int, fname: str, language: str = 'ru') -> None:
    with my_transcribe.download_worker_semaphore:
        utils.remove_file(f'{fname}_{n}.ogg')

        proc = subprocess.run([my_transcribe.FFMPEG, '-ss', str(part[0]), '-i', audio_file, '-t',
                        str(part[1]), f'{fname}_{n}.ogg'],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out_ = proc.stdout.decode('utf-8', errors='replace').strip()
        err_ = proc.stderr.decode('utf-8', errors='replace').strip()
        if 'error' in err_:
            my_log.log2(f'my_stt:stt_genai_worker: Error in FFMPEG: {err_}')
        if 'error' in out_:
            my_log.log2(f'my_stt:stt_genai_worker: Error in FFMPEG: {out_}')

        text = ''

        if not text:
            text = my_transcribe.transcribe_genai(f'{fname}_{n}.ogg', language=language)

        if text:
            with open(f'{fname}_{n}.txt', 'w', encoding='utf-8') as f:
                f.write(text)

        utils.remove_file(f'{fname}_{n}.ogg')


@cachetools.func.ttl_cache(maxsize=10, ttl=1 * 60)
def stt_genai(audio_file: str, language: str = 'ru') -> str:
    """
    Converts the given audio file to text using the Gemini API.

    Args:
        audio_file (str): The path to the audio file to be converted.

    Returns:
        str: The converted text.
    """
    prompt = "Listen carefully to the following audio file. Provide a transcript. Fix errors, make a fine text without time stamps."
    duration = audio_duration(audio_file)

    part_size = 10 * 60 # размер куска несколько минут
    treshold = 5 # захватывать +- несколько секунд в каждом куске
    output_name = utils.get_tmp_fname()

    parts = []
    start = 0
    while start < duration:
        end = min(start + part_size, duration)
        if start == 0:
            parts.append((0, min(duration, end + treshold)))  # Первый фрагмент
        elif end == duration:
            parts.append((max(0, start - treshold), duration - start))  # Последний фрагмент
        else:
            parts.append((max(0, start - treshold), min(duration - start, part_size) + 2 * treshold))  # Остальные фрагменты
        start = end

    n = 0
    threads = []

    for part in parts:
        n += 1
        t = threading.Thread(target=stt_genai_worker, args=(audio_file, part, n, output_name))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    result = ''
    for x in range(1, n + 1):
        # check if file exists
        if os.path.exists(f'{output_name}_{x}.txt'):
            with open(f'{output_name}_{x}.txt', 'r', encoding='utf-8') as f:
                result += f.read() + '\n\n'
            utils.remove_file(f'{output_name}_{x}.txt')

    if 'please provide the audio file' in result.lower() and len(result) < 150:
        return ''
    return result


@cachetools.func.ttl_cache(maxsize=10, ttl=1 * 60)
def assemblyai(audio_file: str, language: str = 'ru'):
    '''Converts the given audio file to text using the AssemblyAI API.'''
    try:
        aai.settings.api_key = random.choice(cfg.ASSEMBLYAI_KEYS)
        transcriber = aai.Transcriber()
        audio_url = (audio_file)
        config = aai.TranscriptionConfig(speaker_labels=True, language_code = language)
        transcript = transcriber.transcribe(audio_url, config)
        # my_log.log2(f'my_stt:assemblyai:DEBUG: {transcript.text}')
        return transcript.text or ''
    except Exception as error:
        traceback_error = traceback.format_exc()
        my_log.log2(f'my_stt:assemblyai: {error}\n\n{traceback_error}')
        return ''


def miliseconds_to_str(miliseconds: int) -> str:
    '''int milliseconds to str 00:00:00'''
    seconds = miliseconds // 1000
    minutes = seconds // 60
    hours = minutes // 60
    seconds %= 60
    minutes %= 60
    return f'{hours:02}:{minutes:02}:{seconds:02}'


def assemblyai_2(audio_file: str, language: str = 'ru'):
    '''Converts the given audio file to text using the AssemblyAI API.
    Multivoice version'''
    try:
        aai.settings.api_key = random.choice(cfg.ASSEMBLYAI_KEYS)
        transcriber = aai.Transcriber()
        audio_url = (audio_file)
        config = aai.TranscriptionConfig(speaker_labels=True,
                                         language_code = language,
                                         entity_detection=True,
                                         )
        transcript = transcriber.transcribe(audio_url, config)
        # my_log.log2(f'my_stt:assemblyai:DEBUG: {transcript.text}')
        result = ''
        for l in transcript.utterances:
            text = l.text
            speaker = l.speaker
            start = l.start
            start_ = miliseconds_to_str(start)
            result += f'[{start_}] [{speaker}] {text}\n'
        result = result.strip()
        return result or ''
    except Exception as error:
        traceback_error = traceback.format_exc()
        my_log.log2(f'my_stt:assemblyai: {error}\n\n{traceback_error}')
        return ''


if __name__ == "__main__":
    pass
    r = assemblyai_2('d:\\Downloads\\rt_podcast919.mp3')
    with open('d:\\Downloads\\rt_podcast919.mp3.txt', 'w', encoding='utf-8') as f:
        f.write(r)
    print(r[:1000])
