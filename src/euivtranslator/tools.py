import os.path
from typing import Generator
from datetime import datetime


os.system('color')


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
            full_dest_path: str = os.path.join(dir_root, folder)
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
            yield os.path.join(dir_root, file)


def log(printable: any, prio: int = 0, logfile_path='logs.txt', hide_logs=False, write_logs=False) -> None:
    """Creates a log with additional information such as time of creation."""

    log_entry: str = f"{BColors.get_color(prio)}{datetime.now().strftime('%H:%M:%S')} {printable}{BColors.END_COLOR}"

    if not hide_logs or prio < 0:
        print(log_entry)

    if write_logs or prio < 0:
        with open(logfile_path, 'a+') as logfile:
            logfile.write(f'{log_entry}\n')


class BColors:
    HINT = '\033[94m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    HEADER = '\033[95m'
    END_COLOR = '\033[0m'

    @staticmethod
    def get_color(priority: int) -> str:
        if priority == 0:
            return ''

        # err and warn
        if priority == -1:
            return BColors.WARNING
        elif priority == -2:
            return BColors.FAIL

        # colors
        elif priority == 1:
            return BColors.HEADER
        elif priority == 2:
            return BColors.HINT

        else:
            raise ValueError  # TODO genauer beschreiben
