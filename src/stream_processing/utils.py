import os

from src.log import log


def delete_file(path: str) -> None:
    """
    Deletes a file at the specified path.
    :param path: Path to the file to be deleted.
    :return: None
    """
    try:
        os.remove(path)
    except FileNotFoundError as e:
        log.error(e)
