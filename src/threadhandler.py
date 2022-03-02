import concurrent.futures
from typing import Iterable
from pyWebTranslate.src.services import DeepL
from pyWebTranslate.src.browsers import Browser, Firefox
from pyWebTranslate.src.threading import BrowserPool


def _translate(txt: str, browser_pool: BrowserPool) -> str:
    browser: Browser = browser_pool.claim()
    translation: str = DeepL(browser).translate(txt, 'ru', 'en')
    browser_pool.stash(browser)
    return translation


def threaded_translation(max_threads: int, lines: Iterable[str]):
    if max_threads < 1:
        raise ValueError  # TODO add an error message

    with BrowserPool(browser_type=Firefox) as browsers:
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_threads)
        futures = executor.map(lambda txt: _translate(txt, browser_pool=browsers), lines)
        for result in futures:
            print(result)
