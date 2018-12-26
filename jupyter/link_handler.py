from os import listdir, path, makedirs
from os.path import isfile, join, isdir
import re, string

class linkHandler(object):

    def __init__(self, list_path):
        self.ignorelist = ["wikiovw.sli"]
        self.link_dict = self.create_dict(list_path)


    def get_link_dict(self):
        return self.link_dict

    def get_ignorelist(self):
        return self.ignorelist

    def create_dict(self, list_path):
        wikifiles = [f for f in listdir(list_path) if isfile(join(list_path, f))]
        wikifiles.sort()
        links = {}
        for wiki in wikifiles:
            if wiki not in self.get_ignorelist():
                print("evaluating links in " + wiki + "... ")
                with open(list_path + wiki, 'r', encoding="utf8") as wiki_file:
                    title_list = self.parse_path(wiki_file.readline())
                    title_key = "/".join(title_list)
                    title_value = "/".join(title_list[:-1])
                    if title_value == "":
                        title_value = "index"
                    links[title_key] = title_value
                print("done.")
        return links



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

        if match_link == title_value:
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
