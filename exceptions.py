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


def exceptions_raiser(func):
    def wrapper(*args, **kwargs):
        try:
            returned = func(*args, **kwargs)

        except DownloadError as err:
            err_message = str(err).split(': ')[1]

            if err_message.startswith('Unable to download API page'):
                raise InternetConnectionError()
            else:
                raise IncorrectLinkError()

        except (Timeout, TooManyRedirects, ConnectionError, HTTPError) as err:
            raise InternetConnectionError()

        except Exception as err:
            raise OtherError(err)
