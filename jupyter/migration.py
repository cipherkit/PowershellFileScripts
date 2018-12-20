from os import listdir, path, makedirs
from os.path import isfile, join
from IPython.display import display, Markdown, Latex
import nbformat as nbf
import re, string


class Migration(object):

    def parse_path(self, wiki):
        filename = re.match('.*\+\+\W(.*)', wiki)
        if filename:
            title = filename.group(1)
            title = title.split('/')
            return title
        else:
            print("Error:")
            print(wiki)

    def create_new_book(self, title, cells, prefix):
        if len(title) == 1:
            nb = nbf.v4.new_notebook()
            nb['cells'] = cells
            fname = prefix + "/" + title[0] + ".ipynb"
            with open(fname, 'w', encoding='utf8') as f:
                nbf.write(nb, f)
        elif len(title) > 1:
            pre = self.create_folder(title[0:-1], prefix)
            self.create_new_book([title[-1]], cells, pre)

    def extend_book(self, book_uri, cells):
        nb = nbf.read(book_uri, as_version=4)
        if nb['cells']:
            nb['cells'].extend(cells)
        else:
            nb['cells'] = cells
        with open(book_uri, 'w', encoding='utf8') as f:
            nbf.write(nb, f)

    def create_folder(self, title, prefix):
        path_to_book = prefix
        for segment in title:
            path_to_book = path.join(path_to_book, segment)
        if not path.exists(path_to_book):
            makedirs(path_to_book)
        return path.abspath(path_to_book)

    # def parse_minutia(self, cell_text):
    #     # bullets
    #     single_pattern = re.compile("^\w*\*", re.I)

    def parse_page(self, wiki_file):
        # returns path and new cell_text
        lines = wiki_file.readlines()
        title = self.parse_path(lines[0])
        text_body_lines = self.parse_links(lines[1:])
        final_title = "    ##" + "/".join(title) + "\n"
        text_body_lines.insert(0, final_title)
        return title, text_body_lines

    def parse_links(self, cell_lines):
        # When the links list for a page is passed in it uses replace link and
        # returns new text for the cell.
        pattern = re.compile("(\[//.*?\])", re.I)
        final_text = []
        if isinstance(cell_lines, str):
            lines = [cell_lines]
        elif isinstance(cell_lines, list):
            lines = cell_lines
        for line in lines:
            for match in re.findall(pattern, line):
                replacement = self.replace_link(match)
                line = line.replace(match, replacement)
            final_text.append(line)
        return final_text

    def replace_link(self, old_link_text):
        # replaces link with jupyter link to appropriate notebook.
        # Uses the form [//link/ext/ext2]
        prefix = "(http://localhost:8888/notebooks/"
        olt = old_link_text.split("/")
        cell = olt[-1]
        if olt[-2] == "":
            return "[" + cell + prefix + "index.ipynb)"
        else:
            return "[" + "/".join(olt[2:]) + prefix + "/".join(olt[2:-1]) + ".ipynb)"

if __name__ == "__main__":
    old_journal_dir = "Z:/data/"
    new_journal_dir = "Z:/jupyter/new_journal/"
    m = Migration()
    wikifiles = [f for f in listdir(old_journal_dir) if isfile(join(old_journal_dir, f))]
    wikifiles.sort()
    for wiki in wikifiles:
        with open(old_journal_dir + wiki, 'r', encoding="utf8") as wiki_file:
            print("Working on " + wiki + "...")
            title, new_text = m.parse_page(wiki_file)
            cell = [nbf.v4.new_markdown_cell(new_text)]
            m.create_new_book(title, cell, new_journal_dir)
    print("Done.")
