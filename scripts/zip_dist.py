import os.path
import re
import zipfile


def zip_it(path: str, zip_filename):
    with zipfile.ZipFile(zip_filename, mode='w') as archive:
        if os.path.isfile(path):
            archive.write(path, os.path.basename(path))
        elif os.path.isdir(path):
            for foldername, subfolders, filenames in os.walk(path):
                for filename in filenames:
                    file_path = os.path.join(foldername, filename)
                    archive.write(file_path, os.path.relpath(file_path, path))
        else:
            print(f"{path} is not a valid file or directory.")


with open('pyproject.toml', 'r') as f:
    contents: str = f.read()
    version: str = re.search(r'^version = "([\d\.]+)"', contents, re.MULTILINE).group(1)
    version = version.strip()

directory: str = os.path.join('dist', 'bfv-hacker-checker')
dest_zip: str = os.path.join('dist', f'bfv-hacker-checker_{version.replace(".", "_")}.zip')
zip_it(directory, dest_zip)
