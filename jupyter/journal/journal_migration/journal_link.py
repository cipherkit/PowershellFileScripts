from util import parse_path
import re


class journalLink(object):

    def __init__(self, line_number, old_link, root_location):
        self.root_location = root_location
        self.link_location = self.set_location(old_link)
        self.line_number = line_number
        self.old_link = old_link
        self.internal_link = self.concatonate_anchor(old_link)
        self.external_link = self.concatonate_uri(old_link)

    def get_line_number(self):
        return self.line_number

    def get_old_link(self):
        return self.old_link

    def get_internal_link(self):
        return self.internal_link

    def get_external_link(self):
        return self.external_link

    def get_location(self):
        return self.link_location

    def concatonate_uri(self, old_link_text):
        # replaces link with jupyter link to appropriate notebook.
        # Old link [//Link/ext/ext2] goes to [link,ext,ext2]
        name = self.render_name(old_link_text)
        if len(name) == 1:
            return "[" + name[0] + "]" + "(\"" + self.root_location + "index.ipynb#" + self.replace_specials(name[0]) + "\")"
        else:
            return "[" + "/".join(name)+ "]" + "(\"" + self.root_location + "/".join(name[:-1]) + ".ipynb#" + self.replace_specials(name[-1]) + "\")"

    def concatonate_anchor(self, old_link_text):
        # replaces link with jupyter link to appropriate notebook.
        # Uses the form [//link/ext/ext2]
        name = self.render_name(old_link_text)
        if len(name) == 1:
            return "[" + name[0] + "]" + "(#" + self.replace_specials(name[0]) + ")"
        else:
            name = "/".join(name)
            return "[" + name + "]" + "(#" + self.replace_specials(name) + ")"

    def set_location(self, old_link):
        list = self.render_name(old_link)
        list = list[:-1]
        if list:
            return self.root_location + "/".join(list)
        else:
            return self.root_location

    def replace_specials(self, name):
        for match in re.findall(r'[\'\"\%\*\!\@\^\&\#\$<>]', name):
            name = name.replace(match, "", 1)
        name = name.replace(" ", "-")
        return name

    def render_name(self, old_link_text):
        segments = old_link_text.split("/")
        list = []
        for segment in segments:
            if segment == "[" or segment == "":
                continue
            list.append(segment)
        list[-1] = list[-1].replace(']', '')
        list[-1] = list[-1].replace('[', '')
        return list
