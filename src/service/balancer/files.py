"""
Files and FileStors
"""


def gen_file_name(file_uuid: str, quality: int, extension: str = 'mp4') -> str:
    return f"{file_uuid}.{quality}.{extension}"
