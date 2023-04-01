import os
import re
import shutil
import zipfile
from typing import Pattern

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

    @staticmethod
    def zip(path: str, zip_filename, wrap: bool = True):
        with zipfile.ZipFile(zip_filename, mode='w') as archive:
            if os.path.isfile(path):
                archive.write(path, os.path.basename(path))
            elif os.path.isdir(path):
                dirname = os.path.dirname(path)
                for foldername, subfolders, filenames in os.walk(path):
                    rel_dir_path = os.path.relpath(foldername, dirname if wrap else path)
                    archive.write(foldername, rel_dir_path)
                    for filename in filenames:
                        file_path = os.path.join(foldername, filename)
                        rel_file_path = os.path.relpath(file_path, dirname if wrap else path)
                        archive.write(file_path, rel_file_path)
            else:
                print(f"{path} is not a valid file or directory.")

    @staticmethod
    def copy(source, destination):
        if os.path.isfile(source):
            shutil.copy(source, destination)
        elif os.path.isdir(source):
            shutil.copytree(source, destination)
        else:
            raise ValueError(f"{source} is not a valid file or directory.")

    @staticmethod
    def remove_file_or_directory(path, ignore_errors=False):
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path, ignore_errors=ignore_errors)
        else:
            raise ValueError(f"{path} is not a valid file or directory.")

    @staticmethod
    def replace_in_file(filename, search_string, replace_string):
        with open(filename, 'r') as f:
            contents = f.read()
        if re.search(search_string, contents):
            new_contents = re.sub(search_string, replace_string, contents)
            with open(filename, 'w') as f:
                f.write(new_contents)
            print(f"Replaced '{search_string}' with '{replace_string}' in file '{filename}'.")
        else:
            print(f"'{search_string}' not found in file '{filename}'.")

    @staticmethod
    def str_to_file(path: str, content: str):
        with open(path, 'w') as f:
            f.write(content)
