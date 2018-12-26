


def parse_path(self, wiki):
    filename = re.match('.*\+\+\W(.*)', wiki)
    if filename:
        title = filename.group(1)
        title = title.split('/')
        return title
    else:
        print("Error:")
        print(wiki)

def parse_links(self, cell_lines, title):
    # When the links list for a page is passed in it uses replace link and
    # returns new text for the cell.
    pattern = re.compile("(\[//.*?\])", re.I)
    final_text = []
    for match in re.findall(pattern, line):
        ext_replacement, int_replacement = self.replace_link(match)
        if self.isinternal_link(title, match):
            line = line.replace(match, int_replacement)
        else:
            line = line.replace(match, ext_replacement)
    final_text.append(line)
    return final_text
