from util import parse_path
import re


class journalLink(object):

    def __init__(self, line_number, old_link, location):
        self.location = location
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

    def concatonate_uri(self, old_link_text):
        # replaces link with jupyter link to appropriate notebook.
        # Old link [//Link/ext/ext2] goes to [link,ext,ext2]
        name = self.render_name(old_link_text)
        if len(name) == 1:
            return "[" + name[0] + "]" + "(\"" + self.location + "index.ipynb#" + self.replace_specials(name[0]) + "\")"
        else:
            return "[" + "/".join(name)+ "]" + "(\"" + self.location + "/".join(name[:-1]) + ".ipynb#" + self.replace_specials(name[-1]) + "\")"

    def concatonate_anchor(self, old_link_text):
        # replaces link with jupyter link to appropriate notebook.
        # Uses the form [//link/ext/ext2]
        name = self.render_name(old_link_text)
        if len(name) == 1:
            return "[" + name[0] + "]" + "(#" + self.replace_specials(name[0]) + ")"
        else:
            name = "/".join(name)
            return "[" + name + "]" + "(#" + self.replace_specials(name) + ")"

    def replace_specials(self, name):
        for match in re.findall(r'[\'\"\%\*\!\@\^\&\#\$<>]', name):
            name = name.replace(match, "", 1)
        name = name.replace(" ", "-")
        return name

    def render_name(self, old_link_text):
        # replaces link with jupyter link to appropriate notebook.
        # Uses the form [//link/ext/ext2] to /link/ext/ext2
        olt = old_link_text.split("/")
        olt[-1] = olt[-1].strip("]")
        return olt[2:]
