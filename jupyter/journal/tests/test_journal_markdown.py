import unittest, os
import nbformat as nbf
import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../journal_migration/')
sys.path.insert(0, myPath + '/../util/')
from journal_markdown import journalMarkdown

class testJournalMarkdown(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # def test_generate_new_text(self):
    #     input_keys = ['jm', 'jm2', 'jm3', 'jm4']
    #     input_dict = {
    #     'jm': journalMarkdown(0, "++ test", 'heading2', "./tmp/"),
    #     'jm2': journalMarkdown(0, "*test*", 'bold', "./tmp/"),
    #     'jm3': journalMarkdown(0, "* test", 'bullet', "./tmp/"),
    #     'jm4': journalMarkdown(0, "# test\n# test2\n# test3", 'number', "./tmp/"),
    #     'jm5': journalMarkdown(0, "+ test", 'heading1', "./tmp/"),
    #     'jm6': journalMarkdown(0, "+++ test", 'heading3', "./tmp/"),
    #     'jm7': journalMarkdown(0, "++++ test", 'heading4', "./tmp/"),
    #     'jm8': journalMarkdown(0, "<<*test*>>", 'no_format', "./tmp/"),
    #     }
    #     output = {}
    #     xpctdout = {
    #     'jm': '## test',
    #     'jm2': '*test*',
    #     'jm3': '- test',
    #     'jm4': '1. test\n2. test2\n3. test3',
    #     'jm5': '# test',
    #     'jm6': '### test',
    #     'jm7': '#### test',
    #     'jm8': 'test'
    #     }
    #     for i in input_keys:
    #         output[i] = input_dict[i].get_new_text()
    #     for key in input_keys:
    #         self.assertEqual(xpctdout[key], output[key], 'not equal')

    def test_convert_heading1(self):
        input = [
        '+ test\n',
        '+ test/test2/test3\n',
        '+ test the testing testers\n'
        ]
        output = []
        xpctdout = [
        '# test',
        '# test/test2/test3',
        '# test the testing testers'
        ]
        for i in input:
            output.append(journalMarkdown(0, i, 'heading1', "./tmp/").get_new_text())
        for ndx in range(len(xpctdout)):
            self.assertEqual(xpctdout[ndx], output[ndx], 'not equal')

    def test_convert_heading2(self):
        input = [
        '++ test\n',
        '++ test/test2/test3\n',
        '++ test the testing testers\n'
        ]
        output = []
        xpctdout = [
        '## test',
        '## test/test2/test3',
        '## test the testing testers'
        ]
        for i in input:
            output.append(journalMarkdown(0, i, 'heading2', "./tmp/").get_new_text())
        for ndx in range(len(xpctdout)):
            self.assertEqual(xpctdout[ndx], output[ndx], 'not equal')

    def test_convert_heading3(self):
        input = [
        '+++ test\n',
        '+++ test/test2/test3\n',
        '+++ test the testing testers\n'
        ]
        output = []
        xpctdout = [
        '### test',
        '### test/test2/test3',
        '### test the testing testers'
        ]
        for i in input:
            output.append(journalMarkdown(0, i, 'heading3', "./tmp/").get_new_text())
        for ndx in range(len(xpctdout)):
            self.assertEqual(xpctdout[ndx], output[ndx], 'not equal')

    def test_convert_heading4(self):
        input = [
        '++++ test\n',
        '++++ test/test2/test3\n',
        '++++ test the testing testers\n'
        ]
        output = []
        xpctdout = [
        '#### test',
        '#### test/test2/test3',
        '#### test the testing testers'
        ]
        for i in input:
            output.append(journalMarkdown(0, i, 'heading4', "./tmp/").get_new_text())
        for ndx in range(len(xpctdout)):
            self.assertEqual(xpctdout[ndx], output[ndx], 'not equal')

    def test_convert_bold_text(self):
        input = [
        '*test*',
        '*test/test2/test3*',
        '*test the testing testers*'
        ]
        output = []
        xpctdout = [
        '*test*',
        '*test/test2/test3*',
        '*test the testing testers*'
        ]
        for i in input:
            output.append(journalMarkdown(0, i, 'bold', "./tmp/").get_new_text())
        for ndx in range(len(xpctdout)):
            self.assertEqual(xpctdout[ndx], output[ndx], 'not equal')

    def test_convert_bulleted_text(self):
        input = [
        '* test',
        '* test/test2/test3',
        '* test the testing testers'
        ]
        output = []
        xpctdout = [
        '- test',
        '- test/test2/test3',
        '- test the testing testers'
        ]
        for i in input:
            output.append(journalMarkdown(0, i, 'bullet', "./tmp/").get_new_text())
        for ndx in range(len(xpctdout)):
            self.assertEqual(xpctdout[ndx], output[ndx], 'not equal')

    def test_convert_numbered_text(self):
        input = [
        '    # test\n',
        '    # test\n    # test2\n    # test3\n',
        '    # test\n        # the\n        # testing\n        # testers\n    # test2\n'
        ]
        output = []
        xpctdout = [
        '    1. test\n',
        '    1. test\n    2. test2\n    3. test3\n',
        '    1. test\n        1. the\n        2. testing\n        3. testers\n    2. test2\n'
        ]
        for i in input:
            output.append(journalMarkdown(0, i, 'number', "./tmp/").get_new_text())
        for ndx in range(len(xpctdout)):
            self.assertEqual(xpctdout[ndx], output[ndx], 'not equal')

    def test_find_col_count(self):
        input = [
        '    #',
        '        #',
        '            #',
        '               #',
        '\t\t\t#',
        '\t #'
        ]
        output = []
        xpctdout = [
        1,
        2,
        3,
        4,
        3,
        1
        ]
        for i in input:
            output.append(journalMarkdown(0, i, 'bullet', "./tmp/").find_col_count(i, 4))
        for ndx in range(len(xpctdout)):
            self.assertEqual(xpctdout[ndx], output[ndx], str(ndx) + ' not equal')

    def test_convert_no_formatted_text(self):
        input = [
        '<test>',
        '<test/test2/test3>',
        '<test the testing testers>'
        ]
        output = []
        xpctdout = [
        'test',
        'test/test2/test3',
        'test the testing testers'
        ]
        for i in input:
            output.append(journalMarkdown(0, i, 'no_format', "./tmp/").get_new_text())
        for ndx in range(len(xpctdout)):
            self.assertEqual(xpctdout[ndx], output[ndx], 'not equal')


if __name__ == '__main__':
    unittest.main()
