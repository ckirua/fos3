import io
import zipfile
from typing import Tuple


def read_zip_from_bytes(content: bytes) -> Tuple[str, bytes]:
    """
    Read content from a zip file and return the filename and file content.

    Args:
        content: Bytes content of the zip file (or HTTPResponse.content...)

    Returns:
        Tuple[filename: str, content: bytes]
    """
    zip_data = io.BytesIO(content)
    with zipfile.ZipFile(zip_data, "r") as zip_ref:
        csv_file = zip_ref.namelist()[0]
        with zip_ref.open(csv_file) as f:
            return csv_file.split(".")[0], f.read()
