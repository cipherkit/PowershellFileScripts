import unittest, os, shutil
from migration import Migration
import nbformat as nbf
import time

class TestMigration(unittest.TestCase):

    def setUp(self):
        self.m = Migration("./testin", "./tmp")
        self.xpctd_out = os.path.abspath("./xpctdout")
        self.prefix = os.path.abspath("./tmp")
        if os.path.exists(self.prefix):
            shutil.rmtree(self.prefix)
        while not os.path.exists(self.prefix):
            os.makedirs(self.prefix)

    def tearDown(self):
        while os.path.exists(self.prefix):
            shutil.rmtree(self.prefix)

    def test_parse_path(self):
        input = [
        "++ Date/2018/March/12th",
        "++ python",
        "++ Al-Qaeda",
        "++ 10 program projects",
        ]
        output = []
        xpctd_out = [
        ["Date", "2018", "March", "12th"],
        ["python"],
        ["Al-Qaeda"],
        ["10 program projects"],
        ]
        for i in input:
            output.append(self.m.parse_path(i))

        for ndx in range(len(output)):
            self.assertEqual(xpctd_out[ndx], output[ndx],
            "Expected output %s did not match actual output %s".format(
            xpctd_out[ndx], output[ndx]))

    # def test_happy_path(self):
    #     old_dir = self.m.get_old_journal_dir()
    #     input = [f for f in os.listdir(old_dir) if os.path.isfile(os.path.join(old_dir, f))]
    #     output = []
    #     for i in input:
    #         with open(old_dir + "/" + i, 'r', encoding="utf8") as in_file:
    #             book_uri, new_text = self.m.parse_page(in_file)
    #             cell = [nbf.v4.new_markdown_cell(new_text)]
    #             self.m.add_cell(book_uri, cell)
    #     new_dir = self.m.get_new_journal_dir()
    #     xpctd_out = [f for f in os.listdir(self.xpctd_out) if
    #                         os.path.isfile(os.path.join(self.xpctd_out, f))]
    #     out = [f for f in os.listdir(new_dir) if os.path.isfile(os.path.join(new_dir, f))]
    #     print(xpctd_out)
    #     print(out)

    def test_create_new_book(self):
        title_input = [
        self.prefix + "/Date/2018/March/12th.ipynb",
        self.prefix + "/index.ipynb"
        ]
        output = []
        xpctd_out = [
            os.path.join(self.prefix + "/Date/2018/March/12th.ipynb"),
            os.path.join(self.prefix + "/index.ipynb")
        ]
        test_cell = []
        test_cell.append(nbf.v4.new_markdown_cell("test"))
        for i in title_input:
            self.m.create_new_book(i, test_cell)
        for xo in xpctd_out:
            self.assertTrue(os.path.exists(xo), xo)

    def test_extend_book(self):
        xpctd_out = [
        nbf.v4.new_markdown_cell("Test"),
        nbf.v4.new_markdown_cell("Test2"),
        nbf.v4.new_markdown_cell("Test3"),
        nbf.v4.new_markdown_cell("Test4"),
        nbf.v4.new_markdown_cell("Test5")
        ]
        nb_path = os.path.join(self.prefix + "/extend_cell.ipynb")
        nb = nbf.v4.new_notebook()
        cells = [
        nbf.v4.new_markdown_cell("Test"),
        nbf.v4.new_markdown_cell("Test2"),
        nbf.v4.new_markdown_cell("Test3")
        ]
        nb['cells'] = cells

        with open(nb_path, 'w', encoding='utf8') as f:
            nbf.write(nb, f)
        self.m.extend_book(nb_path, [nbf.v4.new_markdown_cell("Test4"),
                                    nbf.v4.new_markdown_cell("Test5")])
        open_book = nbf.read(nb_path, as_version=4)
        self.assertEqual(xpctd_out, open_book['cells'],
            "%s does not equal %s".format(xpctd_out, open_book['cells']))

    def test_extend_book_empty(self):
        xpctd_out = [
        nbf.v4.new_markdown_cell("Test4"),
        nbf.v4.new_markdown_cell("Test5")
        ]
        nb_path = os.path.join(self.prefix + "/extend_cell.ipynb")
        nb = nbf.v4.new_notebook()
        with open(nb_path, 'w', encoding='utf8') as f:
            nbf.write(nb, f)
        self.m.extend_book(nb_path, [nbf.v4.new_markdown_cell("Test4"),
                                    nbf.v4.new_markdown_cell("Test5")])
        open_book = nbf.read(nb_path, as_version=4)
        self.assertEqual(xpctd_out, open_book['cells'],
            "%s does not equal %s".format(xpctd_out, open_book['cells']))

    def test_create_footer_tag(self):
        input = [
        ["Date", "2018", "March", "12th"],
        ["python"],
        ["Al-Qaeda"],
        ["10 program projects"],
        ]
        xpctd_out = [
        "<a id=" + "Date/2018/March/12th" + "></a>",
        "<a id=" + "python" + "></a>",
        "<a id=" + "Al-Qaeda" + "></a>",
        "<a id=" + "10_program_projects" + "></a>",
        ]

        output = []
        for i in input:
            output.append(self.m.create_footer_tag(i))
        for ndx in range(len(xpctd_out)):
            self.assertEqual(xpctd_out[ndx], output[ndx])

    def test_create_folder(self):
        input = [
        ["Date", "2018", "March", "12th"],
        ["python"],
        ["Al-Qaeda"],
        ["10 program projects"],
        ]
        xpctd_out = [
        os.path.join(self.prefix + "/Date/2018/March/12th"),
        os.path.join(self.prefix + "/python"),
        os.path.join(self.prefix + "/Al-Qaeda"),
        os.path.join(self.prefix + "/10 program projects"),
        ]

        for i in input:
            self.m.create_folder(i, self.prefix)
        for xo in xpctd_out:
            self.assertTrue(os.path.exists(xo), xo)

    def test_parse_links(self):
        input =[
        "Hello [//world]",
        ["can a [//list] coexist?"],
        "Hello [//my/world] you are [//great]",
        "[//test] [//test2] [//test3]",
        ["Err me Gawd", "This is my journal", "it's the best!"]
        ]
        output = []
        xpctd_out = [
        ["Hello [world](#world)"],
        ['can a [list](#list) coexist?'],
        ["Hello [my/world](#my/world) you are " +\
        "[great](#great)"],
        ["[test](#test) " +\
        "[test2](#test2) " +\
        "[test3](#test3)"],
        ["Err me Gawd", "This is my journal", "it's the best!"],
        ["Hello [world](" + "\"" + self.m.get_new_journal_dir() + "/" + "index.ipynb\")"],
        ['can a [list]("' + self.m.get_new_journal_dir() + '/index.ipynb") coexist?'],
        ["Hello [my/world](\"" + self.m.get_new_journal_dir() + "/my.ipynb\") you are " +\
        "[great](\"" + self.m.get_new_journal_dir() + "/index.ipynb\")"],
        ["[test](\"" + self.m.get_new_journal_dir() + "/index.ipynb\") " +\
        "[test2](\"" + self.m.get_new_journal_dir() + "/index.ipynb\") " +\
        "[test3](\"" + self.m.get_new_journal_dir() + "/index.ipynb\")"],
        ["Err me Gawd", "This is my journal", "it's the best!"]
        ]
        for i in input:
            output.append(self.m.parse_links(i, internal_flag=True))
            output.append(self.m.parse_links(i, internal_flag=False))
        output.sort()
        xpctd_out.sort()
        for ndx in range(len(xpctd_out)):
            self.assertEqual(xpctd_out[ndx], output[ndx], "Mismatch")

    def test_replace_links(self):
        input = [
        "[//abc]",
        "[//123 spaceman]",
        "[//dir/tree/list]"
        ]
        output = []
        xpctd_out = [
        ("[abc](\"" + self.m.get_new_journal_dir() + "/index.ipynb\")", "[abc](#abc)"),
        ("[123 spaceman](\"" + self.m.get_new_journal_dir() + "/index.ipynb\")", "[123 spaceman](#123_spaceman)"),
        ("[dir/tree/list](\"" + self.m.get_new_journal_dir() + "/dir/tree.ipynb\")", "[dir/tree/list](#dir/tree/list)")
        ]
        for i in input:
            output.append(self.m.replace_link(i))
        for ndx in range(len(xpctd_out)):
            self.assertEqual(xpctd_out[ndx], output[ndx], "Mismatch")

    def test_parse_page(self):
        input = [
        "unittest/testin.wiki",
        "unittest/test2in.wiki",
        "unittest/test3in.wiki"
        ]
        output = [
        "unittest/testout.wiki",
        "unittest/test2out.wiki",
        "unittest/test3out.wiki"
        ]
        outcell = ""
        pass


if __name__ == '__main__':
    unittest.main()
