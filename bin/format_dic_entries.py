#!/usr/local/bin/python3

import re
import sys

ENTRY_SEP = '============== END ENTRY =============='


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def main():
    try:
        lang = sys.argv[1]
    except IndexError:
        print('You did not provide the language to format for (every dictionary is formatted differently)')
        sys.exit()
    if len(sys.argv) == 3:
        input_stream = open(sys.argv[2])
    else:
        input_stream = sys.stdin

    # output is entries separated by the string
    entry_text = ''
    for line in input_stream:
        if '============== END ENTRY ==============' in line:
            print_entry(lang, entry_text)
            entry_text = ''
            print()
            continue
        entry_text += line


def print_entry(lang, entry_text):
    if lang == 'en':
        for line in entry_text.splitlines():
            line = re.sub(r'\|(.+?)\|', bcolors.HEADER + r'/\1/' + bcolors.ENDC, line)
            line = re.sub(r'▶', '\n\n ' + bcolors.FAIL + '▶ ' + bcolors.ENDC, line)
            line = re.sub(r'• ', '\n   ' + bcolors.OKGREEN + '• ' + bcolors.ENDC, line)
            line = re.sub(r'([‘“])(.+?)([’”])', bcolors.WARNING + r'“\2”' + bcolors.ENDC, line)
            print(line)
    elif lang == 'ko':
        for line in entry_text.splitlines():
            line = re.sub(r'\|(.+?)\|', bcolors.HEADER + r'/\1/' + bcolors.ENDC, line)
            line = re.sub(r'• ', '\n   ' + bcolors.OKGREEN + '• ' + bcolors.ENDC, line)
            # circled numbers
            line = re.sub(r'([\u2460-\u2473])', '\n\n' + bcolors.HEADER + r'\1 ' + bcolors.ENDC, line)
            line = re.sub(r'(\d+\.)《', '\n\n' + bcolors.FAIL + r'\1' + bcolors.ENDC + '《', line)
            line = re.sub(r'☞', bcolors.BOLD + '☞' + bcolors.ENDC, line)
            line = re.sub(r'(")(.+?)(")', bcolors.WARNING + r'“\2”' + bcolors.ENDC, line)
            line = re.sub(r'(「)(.+?)(」)', bcolors.OKGREEN + r'「\2」' + bcolors.ENDC, line)
            line = re.sub(r'(《)(.+?)(》)', bcolors.BOLD + r'《\2》' + bcolors.ENDC, line)
            print(line)
    elif lang == 'zh':
        # requires HTML input
        from bs4 import BeautifulSoup
        try:
            soup = BeautifulSoup(entry_text, 'lxml')
        except Exception as e:
            print("Error parsing stdin in format_dic_entries.py; did you input text instead of HTML?")
            raise e

        body = soup.find("body")

        # simplest way to pretty print this is to edit text in selected nodes and then get text for the whole document

        # superscript numbers
        for super_el in body.find_all(class_="ty_hom"):
            super_el.string = _super_script(super_el.get_text().strip())
        # part of speech, category/tag
        for info in body.select('.ps, .lev'):
            info.string = bcolors.BOLD + info.get_text() + bcolors.ENDC
        # add extra spacing immediately after numbered bullets
        for info in body.select('.gramb > .semb > .lev'):  # would use :first-child if bs4 made it available
            info.string = ' ' + info.get_text().strip()
        # pronunciation key in pinyin and IPA/American respelling
        for pronunciation in body.select('.pr, .prx'):
            pronunciation.string = bcolors.WARNING + pronunciation.get_text() + bcolors.ENDC
        # links
        for label_el in body.select('a'):
            label_el.string = bcolors.OKBLUE + label_el.get_text() + bcolors.ENDC
        # italics (transliterated Chinese words in English example sentences)
        for label_el in body.select('.italic'):
            label_el.string = bcolors.UNDERLINE + label_el.get_text().strip() + bcolors.ENDC
        # Lettered headers
        for label_el in body.select('.tg_gramb.ty_label'):
            label_el.string = "\n" + bcolors.HEADER + label_el.get_text() + bcolors.ENDC
        # sub-sub list items
        for label_el in body.select('.semb .semb .tg_semb.ty_label'):
            label_el.string = "  " + bcolors.OKBLUE + bcolors.UNDERLINE + label_el.get_text() + bcolors.ENDC + bcolors.ENDC
        # list sub items
        for label_el in body.select('.tg_semb.ty_label'):
            label_el.string = "\n  " + bcolors.FAIL + label_el.get_text() + bcolors.ENDC
        # synonyms in parentheses
        for label_el in body.select('.ind'):
            label_el.string = bcolors.OKGREEN + label_el.get_text() + bcolors.ENDC
        # example sentences
        for label_el in body.select('.gramb > .semb > .exg'):
            label_el.string = "\n   ▸ " + label_el.get_text()
        # example sentences in sub-sub items
        for label_el in body.select('.gramb > .semb > .semb .exg'):
            label_el.string = "\n     ▸ " + label_el.get_text()
        print(body.get_text())


TWO_THREE_BASE = int('0xB0', 16)
OTHERS_BASE = int('0x2070', 16)


def _super_script(number_string):
    """Converts an input string of (ascii) numbers into unicode superscript characters"""
    if len(number_string) > 1:
        return ''.join([_super_script(c) for c in number_string])
    number = int(number_string)
    if number == 1:
        return '\u00B9'
    base = TWO_THREE_BASE if number in [2, 3] else OTHERS_BASE
    code = base + number
    return chr(code)


if __name__ == '__main__':
    main()