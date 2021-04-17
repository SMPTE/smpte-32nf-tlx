#!/usr/bin/env python
#
# Script for publishing markdown documents in various formats

from datetime import date
import subprocess
import json
import yaml
import os
import re


# Microsoft Word template derived from the SMPTE template and modified for use with pandoc
pandoc_template = 'AG04-1-2016-SMPTE-ST-RP-Template-2016-08-29(pandoc).dotx'

# List of directories that may contain the pandoc template
template_locations = ['.', '../../Templates']

# Set the default value for the template if it is not found
refdoc = None

for directory in template_locations:
    pathname = os.path.join(directory, pandoc_template)
    if os.path.isfile(pathname):
        refdoc = pathname

# Locations for finding the default configuration file
config_locations = ['.']


def read_config(filename):
    """Read document information from the specified configuration file"""
    filetype = os.path.splitext(filename)[1][1:]
    if filetype == 'json':
        with open(filename) as file:
            config = json.load(file)
            #config = Configuration(file)
            #print(config)
            return config
    elif filetype == 'yaml':
        with open(filename) as file:
            config = yaml.load(file, Loader=yaml.SafeLoader)
            #print(config)
            return config
    else:
        return None


def read_default_config():
    """Read the document information from the default configuration file."""
    for directory in config_locations:
        if os.path.isdir(directory):
            for filetype in ['json', 'yaml']:
                pathname = os.path.join(directory, f'config.{filetype}')
                if os.path.isfile(pathname):
                    return read_config(pathname)
                    
    # Could not find a configuration file
    return None


def output_filename(source, config=None, date=None, format=None):
    """Generate the output document filename."""

    #print("Config: %s" % config)

    if config:
        # Use the document configuration to form the output filename
        #group = config.get("group", "")
        #config = config.get("state", "WD")
        #title = config.get("title", os.path.splitext(source)[0])

        #filename_parts = [re.sub(r'\s+', r'-', str(config[item])) for item in ['group', 'state', 'type', 'number', 'part', 'project']]
        #filename_parts.append(re.sub(r'\s+', r'-', config['title'].strip()))
        filename_parts = [str(config[key]) for key in ['group', 'state', 'type', 'number', 'part', 'project'] if key in config]
        filename_parts.append(re.sub(r'\s+', r'-', config['title'].strip()))
        #print(filename_parts)
        filename = '-'.join(filename_parts)
        #print("Document basename: %s" % filename)

        # Append the date
        if date: filename += ("-%s" % date)

        # Append the note if the document has a note
        note = config.get('note', None)
        if note:
            #print("Document note: %s" % note)
            filename += ("(%s)" % note)

        # Append the filename extension
        if not format: format = config['format']
        filename += (".%s" % format)
    else:
        # Use the source filename to form the output filename
        basename = os.path.splitext(source)[0]
        if date: basename += ("-%s" % date)
        if not format: format = 'docx'
        filename = f'{basename}.{format}'

    # Replace spaces with hyphens (per SMPTE AG-02:2018)
    #filename = re.sub("\s+", "-", filename.strip())

    return filename


def append_filename_date(filename, date):
    """Append the date to the filename."""
    #print("Append: %s, date: %s" % (filename, date))
    (filename, extension) = os.path.splitext(filename)
    filename += ("-%s" % date)
    return (filename + extension)


def pandoc_command(source, output, refdoc=None):
    """Generate the pandoc command for the specified output file"""

    format = os.path.splitext(output)[1][1:]

    if format == 'docx':
        #pandoc = ['pandoc', '--reference-doc', refdoc, '-o', output, source]
        pandoc = ['pandoc', '--reference-doc', refdoc, '--filter', 'pandoc-citeproc', '-o', output, source]
    elif format == 'html':
        #pandoc = ['pandoc', '-s', '-H', 'pandoc.css', '-o', output, source]
        pandoc = ['pandoc', '-s', '-H', 'pandoc.css', '--filter', 'pandoc-citeproc', '-o', output, source]
    elif format == 'pdf':
        #pandoc = ['pandoc', '-o', output, source]
        pandoc = ['pandoc', '-s', '-N', '--pdf-engine=xelatex', '--toc', '--filter', 'pandoc-citeproc', '-o', output, source]
    else:
        return None

    return pandoc


def print_command(command):
    """Print a command list as a string."""
    print(' '.join(command))


if __name__ == '__main__':

    from argparse import ArgumentParser

    parser = ArgumentParser('Generate the output document from the markdown document')
    parser.add_argument('source', help='source document in markdown format')
    parser.add_argument('-o', '--output', help='output document filename (extension overrides format)')
    parser.add_argument('-f', '--format', default='docx', help='output file format')
    parser.add_argument('-d', '--date', action='store_true', help='append date to the output filename')
    parser.add_argument('-c', '--config', help='read the document parameters from the specified file')
    parser.add_argument('-t', '--template', default=refdoc, help='output document template')
    parser.add_argument('-v', '--verbose', action='store_true', help='enable verbose output')
    #parser.add_argument('-q', '--quiet', action='store_true', help='suppress all output to the terminal window')
    parser.add_argument('-e', '--echo', action='store_true', help='echo the pandoc command to the terminal window')
    args = parser.parse_args()

    # Set the document configuration information
    if args.config:
        # Read the document configuration from the specified file
        config = read_config(args.config)
    else:
        # Use the default document configuration
        config = read_default_config()

    if args.verbose: print("Source document: %s" % args.source)

    if args.output:
        output = args.output
        if args.date:
            output = append_filename_date(output, date.today())
        format = os.path.splitext(output)[1][1:]
    else:
        filedate = date.today() if args.date else None
        output = output_filename(args.source, config, filedate, args.format)
    if args.verbose: print("Output document: %s" % output)

    # Get the command for generating the output document from markdown
    pandoc = pandoc_command(args.source, output, args.template)
    if args.echo: print_command(pandoc)

    process = subprocess.Popen(pandoc, stdout=subprocess.PIPE)

    # Run the command
    stdout = process.communicate()[0]

    #if args.verbose: print("Output document: %s" % output)

