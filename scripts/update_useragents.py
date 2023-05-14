#!/usr/bin/env python3

import json
from pathlib import Path
import re

from bs4 import BeautifulSoup
import httpx

OUR_ROOT = Path(__file__).parents[1].resolve()
OUT_FILE = OUR_ROOT / 'hyperar' / 'useragent.py'


def to_python(obj) -> str:
    lines = ['USER_AGENTS = [']

    for a in obj:
        lines.append('    {')
        lines.append(f"        'ua': {a['ua']!r},")
        lines.append(f"        'pct': {a['pct']!r},")
        lines.append('    },')

    lines.append(']')
    return '\n'.join(lines)


def update_useragents():
    r = httpx.get('https://www.useragents.me/')
    assert r.status_code == 200

    soup = BeautifulSoup(r.text, 'html5lib')
    textarea = soup.select_one('#most-common-desktop-useragents-json-csv textarea')
    assert textarea is not None

    useragents = json.loads(textarea.text)
    python = to_python(useragents)

    update = OUT_FILE.read_text(encoding='utf-8')
    update = re.sub(r'USER_AGENTS = \[.*?\]', python, update, flags=re.DOTALL)
    OUT_FILE.write_text(update, encoding='utf-8', newline='\n')


if __name__ == '__main__':
    update_useragents()
