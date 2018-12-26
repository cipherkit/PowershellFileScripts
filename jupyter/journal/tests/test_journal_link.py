import unittest, os
import nbformat as nbf
import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../journal_migration/')
sys.path.insert(0, myPath + '/../util/')
from journal_link import journalLink

class testJournalLink(unittest.TestCase):

    """docstring for testLinkHandler(unittest.TestCase)"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_concatonate_uri(self):
        input_keys = ['jl', 'jl2', 'jl3', 'jl4']
        input_dict = {
        'jl': journalLink(0, "[//test]", "./tmp/"),
        'jl2': journalLink(0, "[//test/test1/test2/test3]", "./tmp/"),
        'jl3': journalLink(0, "[//stuff/stuff]", "./tmp/"),
        'jl4': journalLink(0, "[//abc 123!]", "./tmp/"),
        }
        output = {}
        xpctdout = {
        'jl': '[test]("./tmp/index.ipynb#test")',
        'jl2': '[test/test1/test2/test3]("./tmp/test/test1/test2.ipynb#test3")',
        'jl3': '[stuff/stuff]("./tmp/stuff.ipynb#stuff")',
        'jl4': '[abc 123!]("./tmp/index.ipynb#abc-123")'
        }
        for i in input_keys:
            output[i] = input_dict[i].get_external_link()
        for key in input_keys:
            self.assertEqual(xpctdout[key], output[key], 'not equal')

    def test_concatonate_anchor(self):
        input_keys = ['jl', 'jl2', 'jl3', 'jl4']
        input_dict = {
        'jl': journalLink(0, "[//test]", "./tmp"),
        'jl2': journalLink(0, "[//test/test1/test2/test3]", "./tmp"),
        'jl3': journalLink(0, "[//stuff/stuff]", "./tmp"),
        'jl4': journalLink(0, "[//abc 123!]", "./tmp"),
        }
        output = {}
        xpctdout = {
        'jl': '[test](#test)',
        'jl2': '[test/test1/test2/test3](#test/test1/test2/test3)',
        'jl3': '[stuff/stuff](#stuff/stuff)',
        'jl4': '[abc 123!](#abc-123)'
        }
        for i in input_keys:
            output[i] = input_dict[i].get_internal_link()
        for key in input_keys:
            self.assertEqual(xpctdout[key], output[key], 'not equal')


    def test_replace_specials(self):
        jl = journalLink(0, "[//dummy]", "./tmp")
        input = [
            "This isn't good!",
            "'N@r is this'",
            "\"Th^s is right out*\"",
            "'!@#$%^&*<>'"
        ]
        output = []
        xpctdout = [
        "This-isnt-good",
        "Nr-is-this",
        "Ths-is-right-out",
        ""
        ]
        for i in input:
            output.append(jl.replace_specials(i))
        for ndx in range(len(xpctdout)):
            self.assertEqual(xpctdout[ndx], output[ndx], 'Not equal')

    def test_render_name(self):
        jl = journalLink(0, "[//dummy]", "./tmp")
        input =[
        "[//world]",
        "[//list]",
        "[//my/world]",
        "[//great/test/test2/test3]",
        ]
        output = []
        xpctd_out = [
        ["world"],
        ["list"],
        ["my", "world"],
        ["great", "test", "test2", "test3"]
        ]
        for i in input:
            output.append(jl.render_name(i))
        for ndx in range(len(xpctd_out)):
            self.assertEqual(xpctd_out[ndx], output[ndx], "Not Equal")


    # def test_create_dict(self):
    #     link_dict = self.lh.get_link_dict()
    #     xpctdout = {
    #     'Scratch Pad': 'index',
    #     'multipage/one': 'multipage',
    #     'multipage/two': 'multipage',
    #     'multipage/three': 'multipage',
    #     'single page': 'index',
    #     'Test Wiki': 'index'
    #     }
    #     for key, value in link_dict.items():
    #         self.assertEqual(xpctdout[key], value, 'not equal')

if __name__ == '__main__':
    unittest.main()
