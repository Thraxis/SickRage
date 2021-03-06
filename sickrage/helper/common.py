# This file is part of SickRage.
#
# URL: https://sickrage.github.io
# Git: https://github.com/SickRage/SickRage.git
#
# SickRage is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SickRage is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SickRage.  If not, see <http://www.gnu.org/licenses/>.

import re
import sickbeard

dateFormat = '%Y-%m-%d'
dateTimeFormat = '%Y-%m-%d %H:%M:%S'
# Mapping HTTP status codes to official W3C names
http_status_code = {
    300: 'Multiple Choices',
    301: 'Moved Permanently',
    302: 'Found',
    303: 'See Other',
    304: 'Not Modified',
    305: 'Use Proxy',
    306: 'Switch Proxy',
    307: 'Temporary Redirect',
    308: 'Permanent Redirect',
    400: 'Bad Request',
    401: 'Unauthorized',
    402: 'Payment Required',
    403: 'Forbidden',
    404: 'Not Found',
    405: 'Method Not Allowed',
    406: 'Not Acceptable',
    407: 'Proxy Authentication Required',
    408: 'Request Timeout',
    409: 'Conflict',
    410: 'Gone',
    411: 'Length Required',
    412: 'Precondition Failed',
    413: 'Request Entity Too Large',
    414: 'Request-URI Too Long',
    415: 'Unsupported Media Type',
    416: 'Requested Range Not Satisfiable',
    417: 'Expectation Failed',
    418: 'Im a teapot',
    419: 'Authentication Timeout',
    420: 'Enhance Your Calm',
    422: 'Unprocessable Entity',
    423: 'Locked',
    424: 'Failed Dependency',
    426: 'Upgrade Required',
    428: 'Precondition Required',
    429: 'Too Many Requests',
    431: 'Request Header Fields Too Large',
    440: 'Login Timeout',
    444: 'No Response',
    449: 'Retry With',
    450: 'Blocked by Windows Parental Controls',
    451: [
        'Redirect',
        'Unavailable For Legal Reasons',
    ],
    494: 'Request Header Too Large',
    495: 'Cert Error',
    496: 'No Cert',
    497: 'HTTP to HTTPS',
    498: 'Token expired/invalid',
    499: [
        'Client Closed Request',
        'Token required',
    ],
    500: 'Internal Server Error',
    501: 'Not Implemented',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
    504: 'Gateway Timeout',
    505: 'HTTP Version Not Supported',
    506: 'Variant Also Negotiates',
    507: 'Insufficient Storage',
    508: 'Loop Detected',
    509: 'Bandwidth Limit Exceeded',
    510: 'Not Extended',
    511: 'Network Authentication Required',
    520: 'Cloudfare - Web server is returning an unknown error',
    521: 'Cloudfare - Web server is down',
    522: 'Cloudfare - Connection timed out',
    523: 'Cloudfare - Origin is unreachable',
    524: 'Cloudfare - A timeout occurred',
    525: 'Cloudfare - SSL handshake failed',
    526: 'Cloudfare - Invalid SSL certificate',
    598: 'Network read timeout error',
    599: 'Network connect timeout error',
}
media_extensions = [
    '3gp', 'avi', 'divx', 'dvr-ms', 'f4v', 'flv', 'img', 'iso', 'm2ts', 'm4v', 'mkv', 'mov', 'mp4', 'mpeg', 'mpg',
    'ogm', 'ogv', 'rmvb', 'tp', 'ts', 'vob', 'webm', 'wmv', 'wtv',
]
subtitle_extensions = ['ass', 'idx', 'srt', 'ssa', 'sub']
timeFormat = '%A %I:%M %p'


def http_code_description(http_code):
    """
    Get the description of the provided HTTP status code.
    :param http_code: The HTTP status code
    :return: The description of the provided ``http_code``
    """

    if http_code in http_status_code:
        description = http_status_code[http_code]

        if isinstance(description, list):
            return '(%s)' % ', '.join(description)

        return description

    # TODO Restore logger import
    # logger.log(u'Unknown HTTP status code %s. Please submit an issue' % http_code, logger.ERROR)

    return None


def is_sync_file(filename):
    """
    Check if the provided ``filename`` is a sync file, based on its name.
    :param filename: The filename to check
    :return: ``True`` if the ``filename`` is a sync file, ``False`` otherwise
    """

    if isinstance(filename, (str, unicode)):
        extension = filename.rpartition('.')[2].lower()

        return extension in sickbeard.SYNC_FILES.split(',') or filename.startswith('.syncthing')

    return False


def is_torrent_or_nzb_file(filename):
    """
    Check if the provided ``filename`` is a NZB file or a torrent file, based on its extension.
    :param filename: The filename to check
    :return: ``True`` if the ``filename`` is a NZB file or a torrent file, ``False`` otherwise
    """

    if not isinstance(filename, (str, unicode)):
        return False

    return filename.rpartition('.')[2].lower() in ['nzb', 'torrent']


def pretty_file_size(size):
    """
    Return a human readable representation of the provided ``size``.
    :param size: The size to convert
    :return: The converted size
    """
    if isinstance(size, (str, unicode)) and size.isdigit():
        size = float(size)
    elif not isinstance(size, (int, long, float)):
        return ''

    remaining_size = size

    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if remaining_size < 1024.:
            return '%3.2f %s' % (remaining_size, unit)

        remaining_size /= 1024.

    return size


def remove_extension(filename):
    """
    Remove the extension of the provided ``filename``.
    The extension is only removed if it is in `sickrage.helper.common.media_extensions` or ['nzb', 'torrent'].
    :param filename: The filename from which we want to remove the extension
    :return: The ``filename`` without its extension.
    """

    if isinstance(filename, (str, unicode)) and '.' in filename:
        basename, _, extension = filename.rpartition('.')

        if basename and extension.lower() in ['nzb', 'torrent'] + media_extensions:
            return basename

    return filename


def replace_extension(filename, new_extension):
    """
    Replace the extension of the provided ``filename`` with a new extension.
    :param filename: The filename for which we want to change the extension
    :param new_extension: The new extension to apply on the ``filename``
    :return: The ``filename`` with the new extension
    """

    if isinstance(filename, (str, unicode)) and '.' in filename:
        basename, _, _ = filename.rpartition('.')

        if basename:
            return '%s.%s' % (basename, new_extension)

    return filename


def sanitize_filename(filename):
    """
    Remove specific characters from the provided ``filename``.
    :param filename: The filename to clean
    :return: The ``filename``cleaned
    """

    if isinstance(filename, (str, unicode)):
        filename = re.sub(r'[\\/\*]', '-', filename)
        filename = re.sub(r'[:"<>|?]', '', filename)
        filename = re.sub(ur'\u2122', '', filename)  # Trade Mark Sign
        filename = filename.strip(' .')

        return filename

    return ''


def try_int(candidate, default_value=0):
    """
    Try to convert ``candidate`` to int, or return the ``default_value``.
    :param candidate: The value to convert to int
    :param default_value: The value to return if the conversion fails
    :return: ``candidate`` as int, or ``default_value`` if the conversion fails
    """

    try:
        return int(candidate)
    except Exception:
        return default_value
