#!/usr/bin/env python
import click
from os import listdir
from os.path import isfile, join

dic_path = "/Users/nglenn/dic_lookups/"
delete_last_line = "\033[1A[\033[2K"

@click.group()
def tango():
    pass

@tango.command()
@click.argument('language')
def study(language):
    """Review the tango for the selected language. If 'all', review all tango for all languages"""
    if language == 'all':
        dic_files = [join(dic_path, f) for f in listdir(dic_path) if isfile(join(dic_path, f))]
    else:
        dic_files = [join(dic_path, language + '.txt')]
    for file in dic_files:
        with open(file) as f:
            for line in f:
                line = line.strip()
                click.echo(line)
                input("(press enter to go to next word)")
                print(delete_last_line)

if __name__ == '__main__':
    tango()
