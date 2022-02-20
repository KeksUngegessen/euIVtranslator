import os.path


def process_file(filepath: str) -> None:
    if not os.path.isfile(filepath):
        raise ValueError(f'No valid filepath: {filepath}')

    filetype: str = filepath.split('.')[len(filepath.split('.')) - 1]

    if filetype == 'yml':
        with open(filepath, 'r', encoding='utf-8-sig') as yaml_file:
            for line in yaml_file:
                print(_decode_yaml(line), end='')

    if filetype == 'txt':
        with open(filepath, 'r', encoding='cp1251') as txt_file:
            for line in txt_file:
                # print(line, end='')
                pass


def _decode_yaml(line_content: str) -> str:
    """Reads a single line and returns its contents as a UTF-8 encoded string."""

    # the yaml file itself is encoded in utf-8 but the cyrillic inside in cp1251 and displayed as cp1252
    return line_content.encode('cp1252').decode('cp1251')
