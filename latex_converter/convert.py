import subprocess
import sys
from bs4 import BeautifulSoup


def read_input():
    """

    :return: A concatenation of lines passed to standard input
    """
    reading = True
    lines = []
    while reading:
        line = sys.stdin.readline()
        if not line:
            reading = False
        else:
            lines.append(line)

    return "".join(lines)


def call_pandoc(input_string):
    """

    :param input_string: a string containing a .tex document.
    :return: the result of piping input_string to
    pandoc -f latex -t html
    """

    process = subprocess.Popen(
        ["pandoc -f latex -t html"],
        stdin=subprocess.PIPE,
        shell=True,
        stdout=subprocess.PIPE
    )
    out, err = process.communicate(bytes(input_string, "UTF-8"))

    return out.decode("UTF-8")


def prettify(input_html):
    soup = BeautifulSoup(input_html, "html.parser")
    return soup.prettify()

if __name__ == "__main__":
    tex_contents = read_input()
    html_contents = call_pandoc(tex_contents)
    print(prettify(html_contents))