import os.path
import tools
import cmdlineparser
from datetime import datetime
from filehandler import process_file


def log(printable: any) -> None:
    tools.log(printable, PROGRESS_LOGFILE, ARGS.hide_logs, ARGS.write_logs)


def do_initial_setup() -> None:
    session_identifier: str = f"Session from {datetime.now().strftime('%d/%m/%Y started at %H:%M:%S')}\n\n"

    # create logfile directory
    if not os.path.isdir(ARGS.logfile_dir):
        os.mkdir(ARGS.logfile_dir)

    # create/clear logfile
    if ARGS.write_logs:
        with open(PROGRESS_LOGFILE, 'w+') as progress_log:
            progress_log.write(session_identifier)

    # create/clear corrupt files logfile; corrupt files will always be logged
    with open(CORRUPT_FILES_LOGFILE, 'w+') as corrupt_files_log:
        corrupt_files_log.write(session_identifier)

    # copy directory structure for later use
    if os.path.isfile(ARGS.src_path):
        pass
    else:
        log('Building directory tree...')
        dir_creation_needed: bool = tools.copy_dir_tree(ARGS.src_path, ARGS.dest_path)
        log('Building complete.') if dir_creation_needed else log('Directory tree has been built already.')


if __name__ == "__main__":
    ARGS = cmdlineparser.get_args()
    PROGRESS_LOGFILE: str = os.path.join(ARGS.logfile_dir, 'log.txt')
    CORRUPT_FILES_LOGFILE: str = os.path.join(ARGS.logfile_dir, 'corrupt_files.txt')

    log('=== EU IV Translator ===')
    do_initial_setup()

    # process each file
    start_time = datetime.now()
    file_paths_generator = tools.get_file_paths_from(ARGS.src_path)
    for filepath in file_paths_generator:
        filepath = os.path.normpath(filepath)
        log(f'FILE: {filepath}')

        try:
            process_file(filepath)

        # log erroneous files
        except (UnicodeError, ValueError) as err:
            log(f'ERROR: {err}\n{" " * 17}Filepath logged to {os.path.abspath(CORRUPT_FILES_LOGFILE)}')
            with open(f'{CORRUPT_FILES_LOGFILE}', 'a') as corrupt_files_log:
                corrupt_files_log.write(f'{os.path.abspath(filepath)}\n -> {err}\n\n')

    log(f'FINISHED: Processing took {datetime.now() - start_time}')
