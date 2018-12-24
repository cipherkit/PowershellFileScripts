from os import listdir, path, makedirs
from os.path import isfile, join, isdir
from IPython.display import display, Markdown, Latex
import nbformat as nbf
import re, string


class Migration(object):

    def __init__(self, old_journal_dir, new_journal_dir):
        self.set_old_journal_dir(old_journal_dir)
        self.set_new_journal_dir(new_journal_dir)
        self.link_dict = self.create_dict(old_journal_dir)

    def set_old_journal_dir(self, old_journal_dir):
        self.old_journal_dir = old_journal_dir

    def get_old_journal_dir(self):
        return self.old_journal_dir

    def set_new_journal_dir(self, new_journal_dir):
        self.new_journal_dir = new_journal_dir

    def get_new_journal_dir(self):
        return self.new_journal_dir

    def get_link_dict(self):
        return self.link_dict

    def create_dict(self, old_journal_dir):
        wikifiles = [f for f in listdir(old_journal_dir) if isfile(join(old_journal_dir, f))]
        wikifiles.sort()
        links = {}
        for wiki in wikifiles:
            print("evaluating links in " + wiki + "... ")
            with open(old_journal_dir + wiki, 'r', encoding="utf8") as wiki_file:
                title_list = self.parse_path(wiki_file.readline())
                title_key = "/".join(title_list)
                title_value = "/".join(title_list[:-1])
                if title_value == "":
                    title_value = "index"
                links[title_key] = title_value
        print("done.")
        return links

    def parse_path(self, wiki):
        filename = re.match('.*\+\+\W(.*)', wiki)
        if filename:
            title = filename.group(1)
            title = title.split('/')
            return title
        else:
            print("Error:")
            print(wiki)

    def add_cell(self, book_uri, cells):
        print(book_uri)
        if isfile(book_uri):
            self.extend_book(book_uri, cells)
        else:
            self.create_new_book(book_uri, cells)

    def create_new_book(self, book_uri, cells):
        nb = nbf.v4.new_notebook()
        nb['cells'] = cells
        split_uri = book_uri.split("/")
        if not isdir("/".join(split_uri[:-1])):
            makedirs("/".join(split_uri[:-1]))
        try:
            with open(book_uri, 'w', encoding='utf8') as f:
                nbf.write(nb, f)
                f.close()
        except Exception as e:
            print(e)

    def extend_book(self, book_uri, cells):
        try:
            with open(book_uri, 'r', encoding='utf8') as f:
                nb = nbf.read(f, as_version=4)
            f.close()
        except Exception as e:
            print(e)
        if nb['cells']:
            nb['cells'].extend(cells)
        else:
            nb['cells'] = cells
        try:
            with open(book_uri, 'w', encoding='utf8') as f:
                nbf.write(nb, f)
            f.close()
        except Exception as e:
            print(e)

    def create_folder(self, title, prefix):
        path_to_book = prefix
        for segment in title:
            path_to_book = path.join(path_to_book, segment)
        if not path.exists(path_to_book):
            makedirs(path_to_book)
        return path.abspath(path_to_book)

    def get_book_uri(self, title):
        if len(title) == 1:
            return self.get_new_journal_dir() + "/index.ipynb"
        else:
            return self.get_new_journal_dir() + "/" + "/".join(title[:-1]) + ".ipynb"

    def create_footer_tag(self, title):
        if isinstance(title, list):
            title = "/".join(title)
        no_space_title = title.replace(' ', '_')
        footer_tag = "\n<a id=" + no_space_title + "></a>"
        return footer_tag

    def parse_page(self, wiki_file):
        # returns path and new cell_text
        lines = wiki_file.readlines()
        title = self.parse_path(lines[0])
        text_body_lines = self.parse_links(lines, title)
        final_title = "    ### " + "/".join(title) + "\n"
        text_body_lines.insert(0, final_title)
        text_body_lines.append("\n" + self.create_footer_tag(title[-1]))
        book_uri = self.get_book_uri(title)
        return book_uri, text_body_lines

    def parse_links(self, cell_lines, title):
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
                ext_replacement, int_replacement = self.replace_link(match)
                if self.isinternal_link(title, match):
                    line = line.replace(match, int_replacement)
                else:
                    line = line.replace(match, ext_replacement)
            final_text.append(line)
        return final_text

    def isinternal_link(self, title, match):
        title_key = "/".join(title)
        parent_book = "/".join(title[:-1])
        title_value = self.link_dict[title_key] # the book that the cell is in
        match_link = "/".join(match.split("/")[2:])
        if len(match_link) == 1:
            match_link = "index"
        print (title_value)
        if "/".join(match_link[:-1]) == title_value:
            return True  # Both exist in the same bookself.
        else:
            return False

    def replace_link(self, old_link_text):
        # replaces link with jupyter link to appropriate notebook.
        # Uses the form [//link/ext/ext2]
        prefix = "(\"" + self.get_new_journal_dir() + "/"
        olt = old_link_text.split("/")
        cell = olt[-1].strip("]")
        if olt[-2] == "":
            return "[" + cell + "]" + prefix + "index.ipynb\")", "[" + cell + "]" + "(#" + cell.replace(' ', '_') + ")"
        else:
            return "[" + "/".join(olt[2:]) + prefix + "/".join(olt[2:-1]) + ".ipynb\")", "[" + "/".join(olt[2:-1]) + "/" + cell + "]" + "(#" + "/".join(olt[2:-1]) + "/" + cell.replace(' ', '_') + ")"


if __name__ == "__main__":
    m = Migration("Z:/data/", "Z:/jupyter/new_journal")
    wikifiles = [f for f in listdir(m.get_old_journal_dir()) if isfile(join(m.get_old_journal_dir(), f))]
    wikifiles.sort()
    for wiki in wikifiles:
        with open(m.get_old_journal_dir() + wiki, 'r', encoding="utf8") as wiki_file:
            print("Working on " + wiki + "...")
            book_uri, new_text = m.parse_page(wiki_file)
            cell = [nbf.v4.new_markdown_cell(new_text)]
        wiki_file.close()
        m.add_cell(book_uri, cell)
    print("Done.")
