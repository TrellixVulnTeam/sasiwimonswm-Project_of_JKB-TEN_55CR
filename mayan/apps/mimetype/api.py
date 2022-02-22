from shutil import copyfileobj

import magic

from mayan.apps.storage.utils import NamedTemporaryFile


def get_mimetype(file_object, mime=True, mimetype_only=False):
    """
    Determine a file's mimetype by calling the system's libmagic
    library via python-magic.
    """
    file_mimetype = None
    file_mime_encoding = None

    with NamedTemporaryFile() as temporary_file_object:
        file_object.seek(0)
        copyfileobj(fsrc=file_object, fdst=temporary_file_object)
        file_object.seek(0)
        temporary_file_object.seek(0)

        kwargs = {'mime': mime}

        if not mimetype_only:
            kwargs['mime_encoding'] = True

        mime = magic.Magic(**kwargs)

        if mimetype_only:
            file_mimetype = mime.from_file(filename=temporary_file_object.name)
        else:
            file_mimetype, file_mime_encoding = mime.from_file(
                filename=temporary_file_object.name
            ).split('; charset=')

        return file_mimetype, file_mime_encoding
