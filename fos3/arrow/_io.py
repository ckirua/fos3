import io
from typing import Optional

import pyarrow as pa
import pyarrow.csv as pacsv
import pyarrow.fs as fs
import pyarrow.parquet as pq


def read_csv_bytes(
    content: bytes,
    read_options: Optional[pacsv.ReadOptions] = None,
    convert_options: Optional[pacsv.ConvertOptions] = None,
):
    return pacsv.read_csv(
        io.BytesIO(content),
        read_options=read_options,
        convert_options=convert_options,
    )


def write_parquet_table(
    table: pa.Table,
    path: str,
    filesystem: fs.FileSystem,
    compression: str = "gzip",
):
    pq.write_table(table, path, filesystem=filesystem, compression=compression)
