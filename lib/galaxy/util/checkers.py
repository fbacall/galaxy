import bz2
import gzip
import re
import tarfile
import zipfile
from io import (
    BytesIO,
    StringIO
)

from galaxy import util
from galaxy.util.image_util import image_type

HTML_CHECK_LINES = 100
CHUNK_SIZE = 2 ** 15  # 32Kb
HTML_REGEXPS = (
    re.compile(r"<A\s+[^>]*HREF[^>]+>", re.I),
    re.compile(r"<IFRAME[^>]*>", re.I),
    re.compile(r"<FRAMESET[^>]*>", re.I),
    re.compile(r"<META[\W][^>]*>", re.I),
    re.compile(r"<SCRIPT[^>]*>", re.I),
)


def check_html(name, file_path=True):
    """
    Returns True if the file/string contains HTML code.
    """
    # Handles files if file_path is True or text if file_path is False
    if file_path:
        temp = open(name, "r", encoding='utf-8')
    else:
        temp = StringIO(util.unicodify(name))
    try:
        for _ in range(HTML_CHECK_LINES):
            line = temp.readline(CHUNK_SIZE)
            if not line:
                break
            if any(regexp.search(line) for regexp in HTML_REGEXPS):
                return True
    except UnicodeDecodeError:
        return False
    finally:
        temp.close()
    return False


def check_binary(name, file_path=True):
    # Handles files if file_path is True or text if file_path is False
    if file_path:
        temp = open(name, "rb")
    else:
        temp = BytesIO(name)
    try:
        return util.is_binary(temp.read(1024))
    finally:
        temp.close()


def check_gzip(file_path, check_content=True):
    # This method returns a tuple of booleans representing ( is_gzipped, is_valid )
    # Make sure we have a gzipped file
    try:
        with open(file_path, "rb") as temp:
            magic_check = temp.read(2)
        if magic_check != util.gzip_magic:
            return (False, False)
    except Exception:
        return (False, False)
    # We support some binary data types, so check if the compressed binary file is valid
    # If the file is Bam, it should already have been detected as such, so we'll just check
    # for sff format.
    try:
        with gzip.open(file_path, 'rb') as fh:
            header = fh.read(4)
        if header == b'.sff':
            return (True, True)
    except Exception:
        return(False, False)

    if not check_content:
        return (True, True)

    with gzip.open(file_path, mode='rb') as gzipped_file:
        chunk = gzipped_file.read(CHUNK_SIZE)
    # See if we have a compressed HTML file
    if check_html(chunk, file_path=False):
        return (True, False)
    return (True, True)


def check_bz2(file_path, check_content=True):
    try:
        with open(file_path, "rb") as temp:
            magic_check = temp.read(3)
        if magic_check != util.bz2_magic:
            return (False, False)
    except Exception:
        return(False, False)

    if not check_content:
        return (True, True)

    with bz2.BZ2File(file_path, mode='rb') as bzipped_file:
        chunk = bzipped_file.read(CHUNK_SIZE)
    # See if we have a compressed HTML file
    if check_html(chunk, file_path=False):
        return (True, False)
    return (True, True)


def check_zip(file_path, check_content=True, files=1):
    if not zipfile.is_zipfile(file_path):
        return (False, False)

    if not check_content:
        return (True, True)

    chunk = None
    for filect, member in enumerate(iter_zip(file_path)):
        handle, name = member
        chunk = handle.read(CHUNK_SIZE)
        if chunk and check_html(chunk, file_path=False):
            return (True, False)
        if filect >= files:
            break
    return (True, True)


def is_bz2(file_path):
    is_bz2, is_valid = check_bz2(file_path, check_content=False)
    return is_bz2


def is_gzip(file_path):
    is_gzipped, is_valid = check_gzip(file_path, check_content=False)
    return is_gzipped


def is_zip(file_path):
    is_zipped, is_valid = check_zip(file_path, check_content=False)
    return is_zipped


def is_single_file_zip(file_path):
    for i, _ in enumerate(iter_zip(file_path)):
        if i > 1:
            return False
    return True


def is_tar(file_path):
    return tarfile.is_tarfile(file_path)


def iter_zip(file_path):
    with zipfile.ZipFile(file_path) as z:
        for f in filter(lambda x: not x.endswith('/'), z.namelist()):
            yield (z.open(f), f)


def check_image(file_path):
    """ Simple wrapper around image_type to yield a True/False verdict """
    if image_type(file_path):
        return True
    return False


__all__ = (
    'check_binary',
    'check_bz2',
    'check_gzip',
    'check_html',
    'check_image',
    'check_zip',
    'is_gzip',
    'is_bz2',
    'is_zip',
)
