import subprocess
import sys
import re
from bs4 import BeautifulSoup


def read_input():
    """

    Yields a series of strings passed in to standard input
    """
    reading = True
    while reading:
        line = sys.stdin.readline()
        if not line:
            reading = False
        else:
            yield line


def preprocess_file(current_batch):
    """
    Preprocesses a list of strings so that Pandoc can handle them.

    :param current_batch: A list of strings, each representing a line
    of LaTeX code.
    :return: A list of strings, cleaned up for Pandoc.
    """

    # Links
    ref_pattern = r"(?P<whole_link>\\ref\{(?P<label>.*?)\})"

    # Tables
    p_column_pattern = re.compile(
        r"\\begin\{tabular\}\{(\|?p\{.*?\})+\|?\}"
    )
    rule_pattern = re.compile(r"\\toprule|\\midrule|\\bottomrule")
    box_pattern = re.compile(r"\\makebox\[\\textwidth\]")
    multicolumn_pattern = re.compile(r"(.*)\\multicolumn(.*)")
    cmidrule_pattern = re.compile(r"(.*)\\cmidrule(.*)")

    lines = []
    print_mode = False

    line_no = 0  # Not iterating over this to enable fiddling possibility
    for line in current_batch:

        # Optional printing for debugging purposes
        if line == "%pandoc_print_begin\n":
            print_mode = True
        if line == "%pandoc_print_end\n":
            print_mode = False

        # Skipping comments
        if line[0] == "%":
            continue

        # Handling internal links, turning them into http hyperlinks
        link_matches = re.findall(ref_pattern, line)
        for match in link_matches:
            internal_link, label = match
            hyperlink = "\{ ref \"" + label + "\" \}"
            line = line.replace(internal_link, hyperlink)

        # Handling basic tables
        table_match = p_column_pattern.match(line)
        if table_match:
            line = re.sub(r"\|?p\{.*?\}", "l", line)
        rule_match = rule_pattern.match(line)
        if rule_match:
            line = "\hline\n"
        box_match = box_pattern.match(line)
        multicolumn_match = multicolumn_pattern.match(line)
        cmidrule_match = cmidrule_pattern.match(line)
        if box_match or multicolumn_match or cmidrule_match:
            line = ""
        line = line.replace("tabular}}}", "tabular}")
        line = line.replace("tabular}}", "tabular}")

        if print_mode:
            sys.stdout.write(line)

        lines.append(line)
        line_no += 1

    return lines


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
    """

    :param input_html: A valid HTML-formatted string
    :return: A string more similar to an acceptable final template
    """

    # Fixing overeager ligatures from Pandoc (which still shouldn't be
    # disabled entirely
    input_html = input_html.replace("{ ref “", "{ ref \"")
    input_html = input_html.replace("” }", "\"}")

    soup = BeautifulSoup(input_html, "html.parser")

    return soup.prettify()


if __name__ == "__main__":
    tex_content_list = read_input()
    cleaner_tex = preprocess_file(tex_content_list)
    html_contents = call_pandoc("".join(cleaner_tex))
    print(prettify(html_contents))