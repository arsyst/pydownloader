from youtube_dl.utils import DownloadError
from requests.exceptions import Timeout, TooManyRedirects, ConnectionError, HTTPError

__all__ = ('IncorrectLinkError',
           'InternetConnectionError',
           'OtherError')


class IncorrectLinkError(Exception):
    def __init__(self):
        super(IncorrectLinkError, self).__init__('Incorrect link format')


class InternetConnectionError(Exception):
    def __init__(self):
        super(InternetConnectionError, self).__init__('No internet connection')


class OtherError(Exception):
    def __init__(self, err: Exception):
        super(OtherError, self).__init__(str(err))
        self.err = err
