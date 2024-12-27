#!/usr/bin/env python3


import telebot
import cfg
import utils


bot = telebot.TeleBot(cfg.token)



def restore_message_text(s1: str, l) -> str:
    """
    Функция принимает строку s1 и список l с описанием форматирования,
    и возвращает строку s0 с примененным форматированием.

    Args:
        s1: Строка, к которой нужно применить форматирование.
        l: Список словарей, описывающих форматирование.
        Каждый словарь содержит информацию о типе форматирования (type),
        начальной позиции (offset), длине (length) и языке (language,
        если применимо).

    Returns:
        Строка s0 с примененным форматированием.
    """
    s0 = ""
    last_pos = 0
    for i in sorted(l, key=lambda x: x.offset):
        # Добавляем текст до текущего форматированного блока
        s0 += s1[last_pos:i.offset]
        
        # Извлекаем форматируемый текст
        formatted_text = s1[i.offset:i.offset + i.length]

        # Применяем соответствующий формат
        if i.type == 'bold':
            s0 += f"**{formatted_text}**"
        elif i.type == 'italic':
            s0 += f"__{formatted_text}__"
        elif i.type == 'strikethrough':
            s0 += f"~~{formatted_text}~~"
        elif i.type == 'code':
            s0 += f"`{formatted_text}`"
        elif i.type == 'pre':
            if i.language:
                s0 += f"```{i.language}\n{formatted_text}\n```"
            else:
                s0 += f"```\n{formatted_text}\n```"

        # Обновляем индекс последней позиции
        last_pos = i.offset + i.length

    # Добавляем оставшийся текст после последнего форматирования
    s0 += s1[last_pos:]
    return s0


@bot.message_handler()
# @bot.message_handler(commands=['start'])
def command_code(message: telebot.types.Message):
    t = r"""
✨ **Вечер игр с родителями!** ✨

Сегодня вечером на нашем участке  царила  особенная  атмосфера!  Мы  с  ребятами  и  их  родителями  перенеслись  в  детство  мам  и  пап  и  сыграли  в  замечательную  игру  "***Мы немножко порезвились, по местам все разместились. Ты загадку отгадай, кто позвал тебя, узнай!***" 😊

Дети  с  задором  бегали,  прятались  и  отгадывали,  кто  же  их  позвал.  Родители  тоже  не  отставали  и  с  улыбками  вспоминали  своё  детство!  😄

Как  же  здорово  проводить  время  вместе,  играть  и  веселиться!  Такие  моменты  объединяют  нас  и  дарят  незабываемые  эмоции! ❤️

#детскийсад #игрысродителями #вечерниеигры #детство #родители #дети #веселье #воспоминания #семейныйвечер
"""


    t = utils.bot_markdown_to_html(t)
    bot.reply_to(message, t, parse_mode = 'HTML')
    # tt = utils.bot_markdown_to_html(t)
    # print(len(tt))
    # print(tt)
    # for ttt in utils.split_html(tt, 3800):
    #     print(ttt)
    #     bot.reply_to(message, ttt, parse_mode = 'HTML')

    # url = 'https://youtu.be/zB7DVYSltGM?si=ldHqem6B4FfW1nEN'
    # kbd  = telebot.types.InlineKeyboardMarkup()
    # button1 = telebot.types.InlineKeyboardButton('ссылка', url=url)
    # kbd.add(button1)
    # video = telebot.types.InputMediaVideo(url)
    # bot.send_video(chat_id=message.chat.id,
    #                caption = 'caption',
    #                video = video,
    #                reply_markup = kbd)

    # print(restore_message_text(message.text, message.entities))



if __name__ == '__main__':
    bot.polling()
