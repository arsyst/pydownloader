# Файл конфигурации

# Режим отладки
DEBUG = True

# Настройки основного окна
MAIN_WINDOW_TITLE = 'PyDownloader'
APP_ICON_PATH = 'images/icon.png'

# Путь до файла базы данных
DB_PATH = 'db/db.sqlite'

# Таймаут работы потоков скачивания информации о видеоролике и превью (в милисекундах)
THREAD_WORKING_TIMEOUT = 16000

# Шаблон имени выходного файла
OUTPUT_FILE_TEMPLATE = '%(title)s.%(ext)s'

# Форматная строка свойств формата видеоролика cо значением FPS и без него
FORMAT_PROPTIES_FPS_TEMPLATE = '{height}p {fps}fps'
FORMAT_PROPTIES_TEMPLATE = '{height}p'

# Шаблон строки состояния скачивания видеоролика
DOWNLOAD_STATUS_TEMPLATE = '{ind}/{total_videos}  Скачано {downloaded} / {total_bytes}  {status}'

# Cтрока свойств формата аудио потока
AUDIO_FORMAT_PROPERTIES_STRING = 'Только аудио'

# Разрешенные расширения видеороликов
ALLOWED_VIDEO_EXTENSIONS = ['mp4', 'webm', 'mp3']

# Путь до папки, для превью видеороликов
THUMBNAILS_DIRECTORY_PATH = 'db/thumbnails'

# Путь до файла логирования
LOGGING_FILE_PATH = 'logs/logs.log'

# YoutubeDL-based downloaders: Индекс превью среднего качества
MEDIUM_QUALITY_THUMBNAIL_INDEX = -2
