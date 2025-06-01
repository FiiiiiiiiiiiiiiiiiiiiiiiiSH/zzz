
# SKIP_PENDING = False
# DB_BACKUP = True
# DB_VACUUM = False


# не журналировать id чатов из этого списка
DO_NOT_LOG = [xxx, yyy,]

# описание бота, которое отображается в чате с ботом, если чат пуст. До 512 символов.
bot_description = """Free chat bot

Голосовое управление, озвучивание текстов, пересказ веб страниц и видеороликов на Youtube, распознавание текста с картинок и из PDF."""

# краткое описание бота, которое отображается на странице профиля бота и отправляется
# вместе со ссылкой, когда пользователи делятся ботом. До 120 символов.
bot_short_description = """Free chat bot"""

# Имя бота (псевдоним), это не уникальное имя, можно назвать как угодно,
# это не имя бота на которое он отзывается. До 64 символов.
bot_name = "Бот"

# максимальное количество сообщений в чате для проверки подписки
# если у юзера больше то надо требовать подписку, точнее звезды
# 50 звезд это примерно 100 рублей, повторять каждый месяц
# MAX_TOTAL_MESSAGES = 500
# MAX_FREE_PER_DAY = 10
# DONATE_PRICE = 50

# имя на которое отзывается бот по умолчанию
default_bot_name = 'бот'


# путь к папке с загруженными файлами, их можно загружать через отдельный сервис
# например для транскрибации файлов
# PATH_TO_UPLOAD_FILES = '/uploads'
# UPLOADER_URL = 'https://myuploder.url/'


# какой бот отвечает по умолчанию
# 'gemini', 'gemini25_flash', 'gemini15', 'gemini-lite', 'gemini-exp', 'gemini-learn', 'gemini-pro-15',
# 'openrouter', 'mistral', 'cohere', 'gpt-4o', 'deepseek_r1',
# 'deepseek_v3', 'llama4_maverick', 'gpt_41', 'gpt_41_mini'

chat_mode_default = 'gemini'

img2_txt_model = 'gemini-2.5-flash-preview-05-20'
img2_txt_model_solve = 'gemini-2.5-flash-preview-05-20'

gemini_flash_model = 'gemini-2.0-flash'
gemini_flash_model_fallback = 'gemini-2.0-flash-exp'

gemini25_flash_model = 'gemini-2.5-flash-preview-05-20'
gemini25_flash_model_fallback = 'gemini-2.5-flash-preview-04-17-thinking'

gemini_flash_light_model = 'gemini-2.0-flash-lite-preview-02-05'
gemini_flash_light_model_fallback = 'gemini-2.0-flash-lite-001'

gemini_pro_model = 'gemini-2.5-pro-exp-03-25'
gemini_pro_model_fallback = 'gemini-2.0-pro-exp-02-05'

gemma3_27b_model = 'gemma-3-27b-it'
gemma3_27b_model_fallback = 'gemini-2.0-flash-lite'

gemini_exp_model = 'gemini-exp-1206'
gemini_exp_model_fallback = 'gemini-2.0-pro-exp-02-05'

gemini_learn_model = 'learnlm-2.0-flash-experimental'
gemini_learn_model_fallback = 'gemini-2.0-flash'


# default locale, язык на который переводятся все сообщения
DEFAULT_LANGUAGE = 'ru'

# languages for init command ['en', 'ru', ..]
INIT_LANGS = ['ru', 'en']

# default text to speech engine 'whisper' 'gemini', 'google', 'assembly.ai', 'deepgram_nova3'
DEFAULT_STT_ENGINE = 'whisper'

# список админов, кому можно использовать команды /restart и вкл-выкл автоответы в чатах
admins = [xxx,]

# группа для логов, вместо(вместе с :) сохранения в текстовые файлы
# сообщения будут копироваться в эту группу, группа должна быть закрытой,
# у бота должны быть права на управление темами (тредами)
# LOGS_GROUP = -1234567890
# если есть такая подгруппа то будет посылать в нее подозрения на плохие промпты на рисование (голые лоли итп)

# -1 - do not log to files
# 0 - log users to log2/ only
# 1 - log users to log/ and log2/
# LOG_MODE = 1

# группа для сапорта если есть
# SUPPORT_GROUP = 'https://t.me/xxx'

# id группы на которую юзеры должны подписаться что бы юзать бота
# бот должен быть в группе и возможно иметь какие то права что бы проверять есть ли в ней юзер
# subscribe_channel_id = -xxx
# subscribe_channel_mes = 'Подпишитесь на наш канал http://t.me/blabla'
# subscribe_channel_cache = 3600*24 # сутки

# сколько раз раз в минуту можно обращаться к боту до бана
DDOS_MAX_PER_MINUTE = 10
# на сколько секунд банить
DDOS_BAN_TIME = 60*10

# telegram bot token
token   = "7676743321:AAFvC2Jx1fBe6mTrHvfEmersFdpdY5vQA9o"


# id телеграм группы куда скидываются все сгенерированные картинки
# группы надо создать, добавить туда бота и дать права на публикацию
pics_group = 0
# pics_group = xxx


# разрешить некоторым юзерам пропускать nsfw фильтр при рисовании через бинг
#ALLOW_PASS_NSFW_FILTER = [
#    123653534,              # xxx1
#    3453453453,             # xxx2
#]

# юзеры которые слишком много рисуют бингом, бывает 1000 картинок за сутки итп
# надо их как то затормозить если не забанить
#SLOW_MODE_BING = [
#    1234668,         # нехороший юзер, возможно робот
#]


# размер буфера для поиска в гугле, чем больше тем лучше ищет и отвечает
# и тем больше токенов жрет
# для модели с 4к памяти
#max_request = 2800
#max_google_answer = 1000
# для модели с 16к памяти
max_request = 14000
max_google_answer = 2000


# насколько большие сообщения от юзера принимать, больше 20000 делать не стоит,
# всё что больше будет преобразовано в файл и дальше можно будет задавать вопросы командой /ask
max_message_from_user = 20000


# показывать ли рекламу группы Neural Networks Forum при рисовании,
# что бы люди туда уходили рисовать и отстали от моего бота
enable_image_adv = False

# https://ai.google.dev/
# ключи для Gemini
gemini_keys = ['AIzaSyCtNospWdjBhsdRXjp8jcpYa8P-kawUn6k']

# размер истории gemini. чем больше тем больше токенов и дольше
# GEMINI_MAX_CHAT_LINES = 40

# прокси для gemini, если не указать то сначала попытается работать
# напрямую а если не получится то будет постоянно искать открытые прокси
gemini_proxies = ['http://172.28.1.5:3128', 'socks5h://172.28.1.5:1080']


# запускать ли апи для бинга, для раздачи картинок другим ботам
# на локалхосте
# BING_API = False

# отлавливать ли номера телефонов для проверки по базе мошенников
# если боту написать номер то он попробует проверить его на сайтах для проверки телефонов
PHONE_CATCHER = True


# рисование кандинским, бесплатное
# https://fusionbrain.ai/docs/ru/doc/api-dokumentaciya/
KANDINSKI_API = [
    ('api key', 'secret key'),
]

# https://console.groq.com/keys
GROQ_API_KEY = [
    'gsk_xxx',
    'gsk_yyy',
    ]
# GROQ_PROXIES = ['socks5://172.28.1.8:1080',]


# ключ от опенроутера openrouter.ai
OPEN_ROUTER_KEY = 'xxx'
# ключи для использования бесплатных моделей с олпенроутера.
# нужен аккаунт с картой, или просто оплаченный хотя бы раз хз
# Free limit: If you are using a free model variant (with an ID ending in :free), then you will be
# limited to 20 requests per minute and 200 requests per day.
OPEN_ROUTER_FREE_KEYS = [
    'xxx',
    'yyy'
]


# shell команды которые бот может выполнять /shell
#SYSTEM_CMDS = [
#    'sudo systemctl restart wg-quick@wg1.service',
#    'python /home/ubuntu/bin/d.py',
#    'dir c:\\'
#]



# https://www.assemblyai.com/ speech-to-text free 100hours. slow in free account?
#ASSEMBLYAI_KEYS = [
#    'key1',
#    'key2',
#]


# курсы валют
# https://openexchangerates.org/api
# OPENEXCHANGER_KEY = 'xxx'


# https://console.mistral.ai/api-keys/
MISTRALAI_KEYS = [
    'xxx1',
    'xxx2',
]

# https://dashboard.cohere.com/api-keys (1000 per month, 20 per minute?)
COHERE_AI_KEYS = [
    'xxx',
    'yyy',
]

# прокси для скачивания с ютуба, на случай если он забанил ип
#YTB_PROXY = [
#    'socks5://127.0.0.1:9050', # tor
#]
# отдельно список для скачивания (первый для субтитров, второй для других данных)
#YTB_PROXY2 = [
#    # 'socks5://127.0.0.1:9050', # tor
#    'socks5://172.28.1.8:9050',
#]

# github 150 requests per day for small llms and 50 requests per day for large llms
# https://github.com/settings/tokens (no any rights required)
#GITHUB_TOKENS = [
#    'xxx',
#    'yyy',
#]


# https://studio.nebius.ai/billing -> Add funds -> Add voucher -> google it
# https://studio.nebius.ai/settings/api-keys
#NEBIUS_AI_KEYS = [
#    'xxx',
#    'yyy',
#]
# use flux images if other fails
# USE_FLUX_IF_EMPTY_IMAGES = False


## https://app.tavily.com/home 1000 поисковых запросов в месяц на аккаунт бесплатно
#TAVILY_KEYS = [
#    'xxx',
#    'yyy',
#]

# string for /donate command html parsing
# DONATION_STRING = '<a href = "https://www.donationalerts.com/r/xxx">DonationAlerts</a>'



# DEBUG = False
