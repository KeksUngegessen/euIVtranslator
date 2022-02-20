import os.path
from typing import Generator
from datetime import datetime


def copy_dir_tree(src_path: str, dest_path: str) -> bool:
    """
    Sets up a new directory tree by copying directories from src_path to dest_path, but leaving out files in them.
    Returns if new directories were created in the process.
    """

    if not os.path.isdir(src_path):
        raise ValueError(f'Not a directory: {src_path}')
    if os.path.abspath(src_path) in os.path.abspath(dest_path):
        raise ValueError('Cannot copy a directory tree into its own subdirectory as it will recurse indefinitely.')

    if not os.path.isdir(dest_path):
        os.mkdir(dest_path)

    dir_creation_needed: bool = False

    for (dir_root, folders, _) in os.walk(src_path):
        for folder in folders:
            subdir_dest_path: str = os.path.join(dir_root[len(src_path) + 1:], folder)
            full_dest_path: str = os.path.join(dest_path, subdir_dest_path)
            if not os.path.isdir(full_dest_path):
                os.mkdir(full_dest_path)
                dir_creation_needed = True

    return dir_creation_needed


def get_file_paths_from(dir_path: str) -> Generator[str, None, None]:
    """
    Returns a generator yielding every filepath within a sub directory of src_path.
    Paths returned are relative to src_path.
    """

    if not os.path.isdir(dir_path):
        raise ValueError(f'No valid directory: {dir_path}')

    for (dir_root, _, files) in os.walk(dir_path):
        for file in files:
            yield os.path.join(dir_path, dir_root[len(dir_path) + 1:], file)


def log(printable: any, logfile_path='logs.txt', hide_logs=False, write_logs=False) -> None:
    """Creates a log with additional information such as time of creation."""

    log_entry: str = f"{datetime.now().strftime('%H:%M:%S')}  {printable}"

    if not hide_logs:
        print(log_entry)

    if write_logs:
        with open(logfile_path, 'a+') as logfile:
            logfile.write(f'{log_entry}\n')