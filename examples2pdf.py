#!/usr/bin/env python3
"""Extract the examples from tikzircuit.tex and compile them to a pdf
document

License:
Copyright (C) 2013, 2014 Sönke Carstens-Behrens
(carstens-behrens AT rheinahrcampus.de)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses."""


import os


def writeexample(outfile, example):
    """Write code of tikzircuit example that will be compiled.
    :outfile: fileptr to LaTeX file
    :example: lines of example code
    :returns: no returns
    """
    outfile.write('\\begin{minipage}{0.19\\textwidth}\n')
    outfile.write('\\begin{{tikzpicture}}\n{0}\n\\end{{tikzpicture}}\n'.format(
        example))
    outfile.write('\\end{minipage}\n')


def writelatex(outfile, texline, state):
    """Parse and write LaTeX line to LaTeX file.
    :outfile: fileptr to LaTeX file
    :texline: line to be parsed and written
    :state: type of text: section, subsection, definition, text, example or
            code
    :returns: (new) state
    """
    if texline.startswith('%%'):
        return None
    if texline.startswith('%'):
        outfile.write('\n' + '\\section{{{0}}}'.format(
            texline[2:-1]) + '\n')
        newstate = 'section'
    else:
        texline = texline.strip()[2:]
        if state == 'section' or state == 'code':
            outfile.write('\n' + '\\subsection{{{0}}}'.format(
                texline) + '\n\n')
            newstate = 'subsection'
        elif state == 'subsection':
            outfile.write(
                    '\\begin{{verbatim}}\n{0}\n\\end{{verbatim}}\n'.format(
                        texline))
            newstate = 'definition'
        elif state == 'text' or state == 'definition':
            if texline.startswith('example') or texline.startswith('Example'):
                outfile.write('\nExample:\\\\\n')
                outfile.write('\\begin{minipage}{0.8\\textwidth}\n')
                outfile.write('\\begin{verbatim}\n')
                newstate = 'example'
            else:
                outfile.write(texline + '\n')
                newstate = 'text'
        else:  # state == 'example'
            outfile.write(texline.strip() + '\n')
            newstate = 'example'
    return newstate


def main():
    """Main function..."""
    with open('tikzircuit-examples.tex', 'w') as outfile:
        outfile.write('\\documentclass[parskip=full]{scrartcl}\n')
        outfile.write('\\usepackage{tikz}\n')
        outfile.write('\\usepackage{xcolor}\n')
        outfile.write('\\usepackage{siunitx}\n')
        outfile.write('\\usepackage{verbatim}\n')
        outfile.write('\\usepackage[linktoc=all,colorlinks=false]{hyperref}\n')
        outfile.write('\\hypersetup{allbordercolors=white}\n')
        outfile.write('\\input{tikzircuit}\n')
        outfile.write('\\title{Components and Examples of tikzircuit}\n')
        outfile.write('\n\\begin{document}\n')
        outfile.write('\\maketitle\n')
        outfile.write('\\tableofcontents\n')
        outfile.write('\\newpage\n')
        outfile.write('\\input{introExamples}\n')
    with open('tikzircuit.tex', 'r') as infile, \
            open('tikzircuit-examples.tex', 'a') as outfile:
        state = None
        example = ''
        for line in infile:
            oldstate = state
            if line.strip().startswith('%'):
                state = writelatex(outfile, line, state)
                if state == 'example' and oldstate == 'example':
                    example += line.strip()[2:] + '\n'
            else:
                state = 'code'
            if oldstate == 'example' and not state == 'example':
                outfile.write('\\end{verbatim}\n')
                outfile.write('\\end{minipage}\n')
                writeexample(outfile, example)
                example = ''
    with open('tikzircuit-examples.tex', 'a') as outfile:
        outfile.write('\n\\end{document}')
    os.system('rubber --pdf tikzircuit-examples.tex')
    os.system('rubber --clean tikzircuit-examples.tex')

if __name__ == '__main__':
    main()
