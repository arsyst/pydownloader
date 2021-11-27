# Файл конфигурации

from downloaders import *

# Словарь загрузчиков видеороликов (ключ - название источника видео, значение - класс загрузчика)
DOWNLOADERS = {
    'YouTube': youtube.Youtube,
    'Twitter': twitter.Twitter,
}
