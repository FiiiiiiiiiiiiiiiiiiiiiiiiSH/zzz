#!/usr/bin/env python3

import cachetools.func
import urllib.parse
import traceback

import googlesearch

import cfg
import my_log
import my_cohere
import my_gemini
import my_gemini_google
import my_ddg
import my_groq
import my_sum
import utils


@cachetools.func.ttl_cache(maxsize=10, ttl=10 * 60)
def search_v3(query: str,
              lang: str = 'ru',
              max_search: int = 10,
              download_only = False,
              chat_id: str = '',
              role: str = ''):

    query = query.strip()

    if not query.startswith('!'):
        # сначала пробуем спросить в гроке
        groq_response = my_groq.search(query, lang, system = role, user_id = chat_id)
        if groq_response:
            if download_only:
                return groq_response
            else:
                return groq_response, groq_response

    if not query.startswith('!'):
        # сначала пробуем спросить в гугле
        google_response = my_gemini_google.google_search(query, chat_id, role=role, lang=lang)
        if google_response:
            if download_only:
                return google_response
            else:
                return google_response, google_response

    query = query.lstrip('!')

    ## Если гугол не ответил или был маркер ! в запросе то ищем самостоятельно
    # добавляем в список выдачу самого гугла, и она же первая и главная
    urls = [f'https://www.google.com/search?q={urllib.parse.quote(query)}',]
    # добавляем еще несколько ссылок, возможно что внутри будут пустышки, джаваскрипт заглушки итп
    try:
        r = my_ddg.get_links(query, max_search)
    except Exception as error:
        my_log.log2(f'my_google:search_google_v3: {error}')
        try:
            # r = my_ddg.get_links(query, max_search)
            r = googlesearch.search(query, stop = max_search, lang=lang)
        except Exception as error:
            my_log.log2(f'my_google:search_google_v3: {error}')
            return ''

    bad_results = ('https://g.co/','.pdf','.docx','.xlsx', '.doc', '.xls')

    try:
        for url in r:
            if any(s.lower() in url.lower() for s in bad_results):
                continue
            urls.append(url)
    except Exception as error:
        error_traceback = traceback.format_exc()
        my_log.log2(f'my_google:search_v3: {error}\n\n{error_traceback}')

    text = my_sum.download_text(urls, my_gemini.MAX_SUM_REQUEST)

    if download_only:
        return text

    q = f'''Answer to the user's search query.
Guess what they were looking for and compose a good answer using search results and your own knowledge.

The structure of the answer should be similar to the following: 

Show a block with the user`s intention briefly.
Show a block with a short and clear answer that satisfies most users.
Show a block with a full answer and links, links should be formatted for easy reading, markdown in links is mandatory.
Answer in "{lang}" language.

User`s query: "{query}"
Current date: {utils.get_full_time()}

Search results:

{text[:my_gemini.MAX_SUM_REQUEST]}
'''
    r = ''

    if not r:
        r =  my_gemini.ai(q[:100000], model=cfg.gemini_flash_model, temperature=1, system=role)
        if r:
            r += '\n\n--\n[Gemini Flash]'

    if not r:
        r = my_cohere.ai(q[:my_cohere.MAX_SUM_REQUEST], system=role)
        if r:
            r += '\n\n--\n[Command R+]'

    if not r:
        r = my_groq.ai(q[:my_groq.MAX_SUM_REQUEST], max_tokens_ = 4000, system=role)
        if r:
            r += '\n\n--\n[Llama 3.2 90b]'
    if not r:
        r = my_groq.ai(q[:32000], max_tokens_ = 4000, model_ = 'mixtral-8x7b-32768', system=role)
        if r:
            r += '\n\n--\n[Mixtral-8x7b-32768]'

    return r, f'Data extracted from Google with query "{query}":\n\n' + text


if __name__ == "__main__":
    pass
    # lines = [
    #     # 'курс доллара',
    #     'что значит 42',
    #     'что значит 42',
    #     ]
    # for x in lines:
    #     print(search_v3(x)[0], '\n\n')
