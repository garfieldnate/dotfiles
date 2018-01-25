#!/usr/local/bin/python3

import re
import sys

from bs4 import BeautifulSoup

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
    BLACK_ON_GRAY = '\033[1;30;47m'
    WHITE_ON_RED = '\033[1;37;41m'
    DARK_GRAY = '\033[1;30;40m'


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
        try:
            soup = BeautifulSoup(entry_text, 'lxml')
        except Exception as e:
            print("Error parsing stdin in format_dic_entries.py; did you input text instead of HTML?")
            raise e
        body = soup.find("body")

        # superscript numbers
        for super_el in body.find_all(class_="ty_hom"):
            super_el.string = _super_script(super_el.get_text().strip())
        # links
        for anchor in body.select('a'):
            anchor.string = bcolors.OKBLUE + anchor.get_text() + bcolors.ENDC
        # pronunciation keys
        for pronunciation in body.select('.pr, .prx'):
            pronunciation.string = bcolors.WARNING + pronunciation.get_text() + bcolors.ENDC
        # grammar notes
        for gg in body.select('.gg'):
            gg.string = bcolors.DARK_GRAY + gg.get_text() + bcolors.ENDC
        # part of speech
        for gg in body.select('.tg_pos'):
            gg.string = bcolors.BOLD + gg.get_text() + bcolors.ENDC
        # bullets and section headers
        for subsense in body.select('.tg_subsense'):
            bullet = subsense.contents[0]
        for label in body.select('.ty_label.tg_se2'):
            label.string = bcolors.OKGREEN + bcolors.BOLD + label.get_text() + bcolors.ENDC
        for header in body.select('.subEntry > .l'):
            header.string = '\n' + bcolors.WARNING + header.get_text() + bcolors.ENDC
        for header in body.select('.ty_label.tg_etym'):
            header.string = '\n\n' + bcolors.WHITE_ON_RED + header.get_text().strip() + bcolors.ENDC + "\n\n"
        # sections
        for section in body.select('.se2, .subEntry'):
            section.string = '\n' + section.get_text()

        text = body.get_text()
        # print(body.get_text())
        for line in text.splitlines():
            line = re.sub(r'▶', '\n\n ' + bcolors.FAIL + '▶ ' + bcolors.ENDC, line)
            line = re.sub(r'• ', '\n   ' + bcolors.OKBLUE + '• ' + bcolors.ENDC, line)
            # line = re.sub(r'([‘“])(.+?)([’”])', bcolors.WARNING + r'“\2”' + bcolors.ENDC, line)
            print(line)
    elif lang == 'ko':
        # requires HTML input
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
        # pronunciation keys
        for pronunciation in body.select('.pr, .prx'):
            pronunciation.string = bcolors.WARNING + pronunciation.get_text() + bcolors.ENDC
        # usage notes
        for oup in body.select('.oup_label'):
            oup.string = bcolors.OKGREEN + oup.get_text() + bcolors.ENDC
        # translations of example sentences
        for trg in body.select('.exg .trg'):
            trg.string = '\n      ' + trg.get_text()
        # example sentences
        for exg in body.select('.exg'):
            exg.string = "\n   ▸ " + exg.get_text()
        # italics (marks headword in example sentences)
        for italic in body.select('.italic'):
            italic.string = bcolors.UNDERLINE + italic.get_text().strip() + bcolors.ENDC
        # bullet numbers
        for sn_el in body.select('.gramb > .semb > .sn'):
            sn_el.string = '\n\n' + bcolors.WARNING + sn_el.get_text() + bcolors.ENDC
        for sn_el in body.select('.semb .semb .sn'):
            sn_el.string = '\n' + bcolors.FAIL + sn_el.get_text() + ' ' + bcolors.ENDC
        for sn_el in body.select('.idmsec .sn'):
            sn_el.string = '\n ' + bcolors.FAIL + sn_el.get_text() + ' ' + bcolors.ENDC
        # links
        for anchor in body.select('a'):
            anchor.string = bcolors.OKBLUE + anchor.get_text() + bcolors.ENDC
        # italic styling inside boxes unfortunately ends the box styling, so we have to restart it. TODO: color stack
        for italic in body.select('.box .italic'):
            italic.string = italic.get_text() + bcolors.BLACK_ON_GRAY
        # boxes
        for box in body.select('.box'):
            box.string = '\n\n' + bcolors.BLACK_ON_GRAY + box.get_text() + bcolors.ENDC
        # phrases
        for label in body.select('.idmGrp .t_label'):
            label.string = '\n\n' + bcolors.WHITE_ON_RED + label.get_text().strip() + bcolors.ENDC
        # same problem as with box; TODO: color stack
        for italic in body.select('.idm .italic'):
            italic.string = italic.get_text() + bcolors.WARNING
        for idm in body.select('.idm'):
            idm.string = '\n\n' +  bcolors.WARNING + idm.get_text() + bcolors.ENDC
        for semb in body.select('.idmsec > .semb'):
            if 'idm' in semb.previous_sibling['class']:
                semb.string = '\n' + semb.get_text()

        print(body.get_text())
    elif lang == 'zh':
        # requires HTML input
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
    elif lang == 'th':
        # requires HTML input
        try:
            soup = BeautifulSoup(entry_text, 'lxml')
        except Exception as e:
            print("Error parsing stdin in format_dic_entries.py; did you input text instead of HTML?")
            raise e

        indent = '  '

        for sequence in soup.select(".sequence-number"):
            sequence.string = _super_script(sequence.string)
        for li in soup.find_all('li'):
            li.string = indent + '•' + li.string.strip()
        for syn_header in soup.select('.syns-header'):
            header_string = syn_header.string.strip()
            syn_header.string = indent + bcolors.OKGREEN + header_string + bcolors.ENDC + ' '
        for syn_header in soup.select('.ants-header'):
            header_string = syn_header.string.strip()
            syn_header.string = indent + bcolors.FAIL + header_string + bcolors.ENDC + ' '
        for syn_header in soup.select('.trans-label'):
            header_string = syn_header.string.strip()
            syn_header.string = indent + bcolors.UNDERLINE + header_string + bcolors.ENDC + ' '

        # simplest way to pretty print this is to edit text in selected nodes and then get text for the whole document
        for entry in soup.select(".entry-container"):
            header = entry.select('.header')[0]
            header_string = bcolors.HEADER + bcolors.UNDERLINE + header.get_text() + bcolors.ENDC

            cat = entry.select('.category')
            classifier = entry.select('.classifier')
            if cat or classifier:
                cat_string = bcolors.WARNING
                if cat:
                    cat_string += cat[0].string
                    cat[0].decompose()
                if classifier:
                    cat_string += ' (' + classifier[0].string + ')'
                    classifier[0].decompose()
                cat_string += bcolors.ENDC
                header_string += ' ' + cat_string
            header.string = header_string

            text = entry.get_text().strip()
            text = re.sub('\n{3,}', '\n\n', text)
            print(text)


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
