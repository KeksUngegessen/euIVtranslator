import re
import os.path


# catches valid YAML key-value pairs
# the first capture group catches any values between 2 quote marks
YAML_REGEX = r'^(?!#).[A-z0-9._]+:[0-9]{0,1} "([^#]*)"'

# catches 2 or more cyrillic characters - without EU4 specific formatting characters - that are between 2 quote marks
CYRILLIC_REGEX = r'[\u0400-\u04FF]+[^["}§£$[a-z]*]*]*[\u0400-\u04FF.!?]+'

YAML_PATTERN = re.compile(YAML_REGEX)
CYRILLIC_PATTERN = re.compile(CYRILLIC_REGEX)


def process_file(filepath: str) -> None:
    if not os.path.isfile(filepath):
        raise ValueError(f'No valid filepath: {filepath}')

    filetype: str = filepath.split('.')[len(filepath.split('.')) - 1]

    """if filetype == 'txt':
        with open(filepath, 'r', encoding='cp1251') as txt_file:
            for line in txt_file:
                # print(line, end='')
                pass"""

    if filetype == 'yml':
        _process_yaml(filepath)


def _process_yaml(filepath: str) -> None:
    """Read lines, which are displayed as cp1252 but encoded in cp1251, and get their contents with UTF-8 encoding."""

    with open(filepath, 'r', encoding='utf-8-sig') as yaml_file:
        counter: int = -1
        for line in yaml_file:
            counter += 1
            match: re.Match = YAML_PATTERN.search(line)
            if match is not None:
                gibberish: str = match.group(1)  # the text that needs decoding
                gibberish.encode('cp1252').decode('cp1251')
                # TODO
