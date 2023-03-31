import os
import zipfile

import humanfriendly


class FileUtil:

    @staticmethod
    def split_file(filename: str, chunk_size: str or int) -> None:
        if isinstance(chunk_size, str):
            chunk_size_bytes: int = humanfriendly.parse_size(chunk_size)
        else:
            chunk_size_bytes: int = chunk_size

        with open(filename, 'rb') as large_file:
            chunk_number: int = 0

            while True:
                chunk: bytes = large_file.read(chunk_size_bytes)

                if not chunk:
                    break

                with open(f'{filename}_part{chunk_number}', 'wb') as chunk_file:
                    chunk_file.write(chunk)

                chunk_number += 1

    @staticmethod
    def merge_files(filename_prefix: str, output_filename: str) -> None:
        with open(output_filename, 'wb') as output_file:
            chunk_number: int = 0

            while True:
                part_filename: str = f'{filename_prefix}_part{chunk_number}'

                if not os.path.exists(part_filename):
                    break

                with open(part_filename, 'rb') as part_file:
                    output_file.write(part_file.read())

                chunk_number += 1

    @staticmethod
    def unzip(zip_file: str, dest_dir: str) -> None:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(dest_dir)
