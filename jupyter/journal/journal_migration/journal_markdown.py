import re

class journalMarkdown(object):

    def __init__(self, line, old_text, type, location):
        self.line = line
        self.old_text = old_text
        self.type = type
        self.location = location
        self.new_text = self.generate_new_text()

    def get_line_number(self):
        return self.line

    def get_old_text(self):
        return self.old_text

    def get_type(self):
        return self.type

    def get_location(self):
        return self.location

    def get_new_text(self):
        return self.new_text

    def generate_new_text(self):
        # For performance tweaks I can put the dict outside the function.
        return {
        'heading1': self.convert_heading1(),
        'heading2': self.convert_heading2(),
        'heading3': self.convert_heading3(),
        'heading4': self.convert_heading4(),
        'bold': self.convert_bold_text(),
        'bullet': self.convert_bulleted_text(),
        'number': self.convert_numbered_text(),
        'no_format': self.convert_no_formated_text()
        }[self.type]

    def convert_heading1(self):
        pattern = re.compile(r'\+', re.I)
        new_text = re.sub(pattern, r'#', self.old_text)
        return new_text

    def convert_heading2(self):
        pattern = re.compile(r'\+\+', re.I)
        new_text = re.sub(pattern, r'##', self.old_text)
        return new_text

    def convert_heading3(self):
        pattern = re.compile(r'\+\+\+', re.I)
        new_text = re.sub(pattern, r'###', self.old_text)
        return new_text

    def convert_heading4(self):
        pattern = re.compile(r'\+\+\+\+', re.I)
        new_text = re.sub(pattern, r'####', self.old_text)
        return new_text

    def convert_bold_text(self):
        return self.old_text

    def convert_bulleted_text(self):
        pattern = re.compile(r'(\W*)\*(\W(.+))', re.I)
        new_text = re.sub(pattern, r'\1-\2', self.old_text)
        return new_text

    def convert_numbered_text(self):
        # I can do better later
        split_text = self.old_text.split("\n")
        last_ = 1
        depths = []
        if len(split_text) == 1:
            return split_text[0].replace('#', '1.')
        # else split text has more elements
        for i in range(len(split_text)):
            depths.append(self.find_col_count(split_text[i], 4))
        trail = [1]
        left = 0
        for j in range(len(depths)-1):
            if depths[j+1] > depths[j]:
                trail.append(1)
                left = j
            if depths[j+1] == depths[j]:
                trail.append(trail[-1] + 1)
            if depths[j+1] < depths[j]:
                trail.append(trail[left] + 1)
        new_text = []
        for k in range(len(trail)):
            new_text.append(split_text[k].replace('#', str(trail[k]) + "."))
        return "\n".join(new_text)

    def find_col_count(self, segment, length_tab):
        col_length = 1
        col_count = 0
        for char in list(segment):
            if char == ' ':
                col_length = col_length + 1
            if char == '\t':
                col_count = col_count + 1
                col_length = 0
            if col_length >= length_tab:
                col_count = col_count + 1
                col_length = 0
            if char == '#':
                return col_count
        return 0

    def convert_no_formated_text(self):
        pattern = re.compile(r'<(.+)>')
        new_text = re.sub(pattern, r'<\1>', self.old_text)
        return new_text
