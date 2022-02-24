import os.path
import tools
import cmdlineparser
from datetime import datetime
from filehandler import process_file


def log(printable: any, prio=0) -> None:
    tools.log(printable, prio, PROGRESS_LOGFILE, ARGS.hide_logs, ARGS.write_logs)


if __name__ == "__main__":
    ARGS = cmdlineparser.get_args()
    PROGRESS_LOGFILE: str = os.path.join(ARGS.logfile_dir, 'log.txt')
    CORRUPT_FILES_LOGFILE: str = os.path.abspath(os.path.join(ARGS.logfile_dir, 'corrupt_files.txt'))
    SESSION: str = f"Session from {datetime.now().strftime('%d/%m/%Y started at %H:%M:%S')}\n\n"
    INDENT: str = f'\n{" " * 17}'

    log('=== EU IV Translator ===', prio=1)

    # create logfile directory
    if not os.path.isdir(ARGS.logfile_dir):
        os.mkdir(ARGS.logfile_dir)

    # create/clear logfile
    if ARGS.write_logs:
        with open(PROGRESS_LOGFILE, 'w+') as progress_log:
            progress_log.write(SESSION)

    # create/clear corrupt files logfile; corrupt files will always be logged
    with open(CORRUPT_FILES_LOGFILE, 'w+') as corrupt_files_log:
        corrupt_files_log.write(SESSION)

    # copy directory structure for later use
    if os.path.isfile(ARGS.src_path):
        pass
    else:
        log('Building directory tree...', prio=2)
        dir_creation_needed: bool = tools.copy_dir_tree(ARGS.src_path, ARGS.dest_path)
        log('Building complete.', 2) if dir_creation_needed else log('Directory tree has already been built.', 2)

    # process each file
    start_time = datetime.now()
    file_paths_generator = tools.get_file_paths_from(ARGS.src_path)
    for filepath in file_paths_generator:
        filepath = os.path.normpath(filepath)
        log(f'FILE: {filepath}')

        try:
            process_file(filepath)

        # log erroneous files
        except UnicodeEncodeError as err:
            line: str = err.args[1]
            char_index: int = err.args[2]
            err_msg: str = f'-> Char &#{ord(line[char_index])} on position {char_index} cannot be encoded with cp1252.'
            log(f'ERROR: In file {filepath}{INDENT}'
                f'{err_msg}{INDENT}Error message can be found at {CORRUPT_FILES_LOGFILE}',
                prio=-2)

            with open(f'{CORRUPT_FILES_LOGFILE}', 'a') as corrupt_files_log:
                corrupt_files_log.write(f'{os.path.abspath(filepath)}\n {err_msg}\n\n')

    log(f'FINISHED: Processing took {datetime.now() - start_time}', prio=2)
