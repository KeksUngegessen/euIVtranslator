import re
import os.path
from typing import Generator, Iterator
from concurrent.futures import ThreadPoolExecutor

from pywebtranslator.threading import TranslationServicePool
from pywebtranslator.services.translationservice import TranslationService


# catches valid YAML key-value pairs
# the second capture group catches any values between 2 quote marks
YAML_KEY_VAL_PATTERN: re.Pattern = re.compile(r'(^(?!#).[A-z0-9._]+:[0-9]? \")([^#]*)(\")')

# catches 2 or more cyrillic characters - without EU4 specific formatting characters - that are between 2 quote marks
CYRILLIC_PATTERN: re.Pattern = re.compile(r'[\u0400-\u04FF]+[^[\"}§£$a-z]*[\u0400-\u04FF.!?]+')


def process_file(filepath: str, service_pool: TranslationServicePool, executor: ThreadPoolExecutor) -> None:
    """Sruff"""
    if not os.path.isfile(filepath):
        raise ValueError(f'No valid filepath: {filepath}')

    futures: Iterator[str]
    filetype: str = filepath.split('.')[len(filepath.split('.')) - 1]

    if filetype == 'txt':
        futures = []
        # with open(filepath, 'r', encoding='cp1251') as txt_file:
        #     for line in txt_file:
        #         # print(line, end='')
        #         pass

    elif filetype == 'yml':
        decoded_yaml_content = decode_yaml(filepath)
        futures = executor.map(
            lambda line: YAML_KEY_VAL_PATTERN.sub(
                rf'\1{translate_async(YAML_KEY_VAL_PATTERN.search(line), service_pool=service_pool)}\3', line
            ),
            decoded_yaml_content
        )

    else:
        raise ValueError(f"Filetype '{filetype}' not supported, skipping {filepath}")

    for result in futures:  # TODO save them
        print(result, end='')


def decode_yaml(filepath: str) -> Generator[str, any, None]:
    """Read a Russian Universalis YAML localisation file, which is displayed as cp1252 but encoded in cp1251,
       and yield its decoded contents line by line with UTF-8 encoding applied."""

    if not os.path.isfile(filepath) or filepath.split('.')[len(filepath.split('.')) - 1] != 'yml':
        raise ValueError(f'Not a YAML file: {filepath}')

    with open(filepath, 'r', encoding='utf-8-sig') as yaml_file:
        for line in yaml_file:
            yield YAML_KEY_VAL_PATTERN.sub(lambda match: match.group(0).encode('cp1252').decode('cp1251'), line)


def translate(match: re.Match, service: TranslationService, src_lang='ru', dest_lang='en') -> str:
    """Translates a matched value from a YAML key-value pair."""
    txt: str = match.group(2) if match is not None else ''
    return service.translate(txt, src_lang, dest_lang) if txt != '' else ''


def translate_async(match: re.Match, service_pool: TranslationServicePool, src_lang='ru', dest_lang='en') -> str:
    """Asynchronously translates a matched value from a YAML key-value pair."""
    service: TranslationService = service_pool.claim()
    translation: str = translate(match, service, src_lang, dest_lang)
    service_pool.stash(service)
    return translation
