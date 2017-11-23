#!/usr/local/bin/python3

import sys
import re

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
        print('You did not provide the language to format for')
        sys.exit()
    if lang == 'en':
        for line in sys.stdin:
            line = re.sub(r'\|(.+?)\|', bcolors.HEADER + r'/\1/' + bcolors.ENDC, line)
            line = re.sub(r'▶', '\n\n ' + bcolors.FAIL + '▶ ' + bcolors.ENDC, line)
            line = re.sub(r'• ', '\n   ' + bcolors.OKGREEN + '• ' + bcolors.ENDC, line)
            line = re.sub(r'(‘|“)(.+?)(’|”)', bcolors.WARNING + r'“\2”' + bcolors.ENDC, line)
            print(line)
    if lang == 'ko':
        for line in sys.stdin:
            line = re.sub(r'\|(.+?)\|', bcolors.HEADER + r'/\1/' + bcolors.ENDC, line)
            line = re.sub(r'• ', '\n   ' + bcolors.OKGREEN + '• ' + bcolors.ENDC, line)
            line = re.sub(r'(\d+\.)《', '\n\n' + bcolors.FAIL + r'\1' + bcolors.ENDC + '《', line)
            line = re.sub(r'☞', bcolors.BOLD + '☞' + bcolors.ENDC, line)
            line = re.sub(r'(")(.+?)(")', bcolors.WARNING + r'“\2”' + bcolors.ENDC, line)
            line = re.sub(r'(「)(.+?)(」)', bcolors.OKGREEN + r'「\2」' + bcolors.ENDC, line)
            line = re.sub(r'(《)(.+?)(》)', bcolors.BOLD + r'《\2》' + bcolors.ENDC, line)
            print(line)
    if lang == 'zh':
        # TODO: color characters, pinyin and meaning differently. Probably requires HTML output.
        for line in sys.stdin:
            line = re.sub(r'\|(.+?)\|', bcolors.HEADER + r'/\1/' + bcolors.ENDC, line)
            # circled numbers
            line = re.sub(r'([\u2460-\u2473])', '\n\n' + bcolors.WARNING + r'\1' + bcolors.ENDC, line)
            line = re.sub(r'( [A-Z]\. )', '\n' + bcolors.OKGREEN + r'\1' + bcolors.ENDC, line)
            print(line)

if __name__ == '__main__':
    main()
