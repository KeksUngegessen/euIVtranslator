import os
import argparse


# argument defaults
DEFAULT_DEST_PATH: str = os.path.normpath(r'..\translations')
DEFAULT_LOGFILE_DIR: str = os.path.normpath(r'..\logs')
DEFAULT_THREADS: int = 4
DEFAULT_HIDE_LOGS: bool = False
DEFAULT_WRITE_LOGS: bool = False
DEFAULT_SKIP_FILE_CHECK: bool = False

PARSER = argparse.ArgumentParser(description='TODO')

# positional args
PARSER.add_argument('src_path', type=str,
                    help='Specify the source file/directory to translate.')

# optional args
PARSER.add_argument('-d', '--dest_path', type=str,
                    help='Specify the destination file/directory in which translated files will be saved. '
                         f'It gets created if it not exists. Default is {DEFAULT_DEST_PATH}.')
PARSER.add_argument('--logfile_dir', type=str,
                    help=f"Specify the logfile directory. Default is {DEFAULT_LOGFILE_DIR}.")
PARSER.add_argument('-t', '--threads', type=int,
                    help=f'Specify the maximum number of threads used. Default is {DEFAULT_THREADS}.')
PARSER.add_argument('-l', '--hide_logs', action='store_true',
                    help=f'Hides status logs on console, but keeps error messages. Default is {DEFAULT_HIDE_LOGS}.')
PARSER.add_argument('-w', '--write_logs', action='store_true',
                    help=f'Writes logs to logfile. Error Messages will always be logged. Default is {DEFAULT_WRITE_LOGS}.')
PARSER.add_argument('-c', '--skip_file_check', action='store_true',
                    help='Skips the check for already existing translations in the destination path. '
                         'May increase performance when a previous execution has been interrupted. '
                         f'Default is {DEFAULT_SKIP_FILE_CHECK}.')

PARSER.set_defaults(
    dest_path=DEFAULT_DEST_PATH,
    logfile_dir=DEFAULT_LOGFILE_DIR,
    threads=DEFAULT_THREADS,
    hide_logs=DEFAULT_HIDE_LOGS,
    write_logs=DEFAULT_WRITE_LOGS,
    skip_file_check=DEFAULT_SKIP_FILE_CHECK,
)

ARGS = PARSER.parse_args()

# argument validation
if not os.path.exists(ARGS.src_path):
    PARSER.error(f'Source path not found: {ARGS.src_path}')

if ARGS.threads < 1:
    PARSER.error('Number of threads must be greater than 0')
elif ARGS.threads > 32:
    PARSER.error(
        'More than 32 threads are currently not supported, though it might be possible. '
        'This soft cap solely exists out of precaution.'
    )


def get_args() -> argparse.Namespace:
    return ARGS
