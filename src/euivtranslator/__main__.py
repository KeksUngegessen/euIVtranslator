import sys
import os.path
from traceback import format_exc
from concurrent.futures import ThreadPoolExecutor

import tools
import cmdlineparser
from datetime import datetime
from filehandling import process_file
from pywebtranslator.services.deepl import DeepL
from pywebtranslator.browsers.firefox import Firefox
from pywebtranslator.threading import TranslationServicePool


def log(printable: any, prio=0) -> None:
    tools.log(printable, prio, PROGRESS_LOGFILE, ARGS.hide_logs, ARGS.write_logs)


if __name__ == "__main__":
    ARGS = cmdlineparser.ARGS
    PROGRESS_LOGFILE: str = os.path.join(ARGS.logfile_dir, 'log.txt')
    CORRUPT_FILES_LOGFILE: str = os.path.abspath(os.path.join(ARGS.logfile_dir, 'corrupt_files.txt'))
    SESSION_INFO: str = f"Session from {datetime.now().strftime('%d/%m/%Y started at %H:%M:%S')}\n\n"
    INDENT: str = f'\n{" " * 15}'

    log('=== EU IV Translator ===', prio=1)

    # create logfile directory
    if not os.path.isdir(ARGS.logfile_dir):
        os.mkdir(ARGS.logfile_dir)

    # create/clear logfile
    if ARGS.write_logs:
        with open(PROGRESS_LOGFILE, 'w+') as progress_log:
            progress_log.write(SESSION_INFO)

    # create/clear corrupt files logfile; corrupt files will always be logged
    with open(CORRUPT_FILES_LOGFILE, 'w+') as corrupt_files_log:
        corrupt_files_log.write(SESSION_INFO)

    # copy directory structure for later use
    if os.path.isfile(ARGS.src_path):
        pass
    else:
        log('Building directory tree...', prio=2)
        dir_creation_needed: bool = tools.copy_dir_tree(ARGS.src_path, ARGS.dest_path)
        log('Building complete.', 2) if dir_creation_needed else log('Directory tree has already been built.', prio=2)

    start_time: datetime = datetime.now()
    file_paths_generator = tools.get_file_paths_from(ARGS.src_path)
    executor: ThreadPoolExecutor = ThreadPoolExecutor(max_workers=ARGS.threads)

    # now process each file
    with TranslationServicePool(service_type=DeepL, browser_type=Firefox, is_headless=False) as service_pool:
        for filepath in file_paths_generator:
            filepath = os.path.normpath(filepath)
            log(f'FILE: {filepath}')

            try:
                process_file(filepath, service_pool, executor)

            except ValueError as err:
                log(f'WARN: {err}', prio=-1)

            # log erroneous files
            except UnicodeEncodeError as err:
                line: str = err.args[1]
                char_index: int = err.args[2]
                err_msg: str = f'Char &#{ord(line[char_index])} on pos {char_index} cannot be encoded with cp1252.'

                log(f'WARN: {err_msg}{INDENT}Details can be found at {CORRUPT_FILES_LOGFILE}', prio=-1)
                with open(f'{CORRUPT_FILES_LOGFILE}', 'a') as corrupt_files_log:
                    corrupt_files_log.write(f'{os.path.abspath(filepath)}\n {err_msg}\n\n')

            # close WebDrivers when something goes wrong
            except Exception as exc:
                service_pool.quit()
                log(f'{format_exc()}', prio=-2)
                sys.exit(1)

    log(f'FINISHED: Processing took {datetime.now() - start_time}', prio=2)
