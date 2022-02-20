import os
import argparse


parser = argparse.ArgumentParser(description='To do')

# positional args
parser.add_argument('src_path', type=str,
                    help='Specify the source directory to translate files from.')

# optional args
parser.add_argument('-d', '--dest_path', type=str,
                    help='Specify the destination directory in which translated files go. '
                         'It gets created if it not exists.')
parser.add_argument('-t', '--threads', type=int,
                    help='Specify the maximum number of threads used.')
parser.add_argument('-l', '--hide_logs', action='store_true',
                    help='Hides logs on console. Default is False.')
parser.add_argument('-w', '--write_logs', action='store_true',
                    help='Writes logs to logfile. Default is False.')
parser.add_argument('-c', '--skip_file_check', action='store_true',
                    help='Skips the check on already existing translations in the destination path. '
                         'May increase performance when execution has been interrupted beforehand. Default is False.')
parser.add_argument('--logfile_dir', type=str,
                    help="Specify the directory where to put log files. Default is '../logs'.")

parser.set_defaults(
    dest_path='../translations',
    threads=4,
    hide_logs=False,
    write_logs=False,
    skip_file_check=False,
    logfile_dir=r'..\logs'
)

ARGS = parser.parse_args()

# Argument validation
if not os.path.exists(ARGS.src_path):
    parser.error(f'Source path not found: {ARGS.src_path}')

if ARGS.threads < 1:
    parser.error('Number of threads must be greater than 0')
elif ARGS.threads > 32:
    parser.error(
        'More than 32 threads are currently not supported, though it might be possible. '
        'This soft cap solely exists out of precaution.'
    )


def get_args() -> argparse.Namespace:
    return ARGS
