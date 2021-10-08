import unittest
from HTML_parsing import HtmlParsing
from requests import Session

session = Session()
endgame_link = "https://www.imdb.com/title/tt4154796/"
parse = HtmlParsing(endgame_link, session)


class SetToString(unittest.TestCase):
    def test_empty_set(self):
        self.assertEqual("", parse.set_to_string({}))

    def test_singular_element(self):
        self.assertEqual("Ab1_$", parse.set_to_string(["Ab1_$"]))

    def test_changing_comma(self):  # Tests that commas are being replaced with semi-colons
        self.assertEqual("Ab1_$; B*", parse.set_to_string(["Ab1_$", 'B*']))


def suite():
    test_suite = unittest.TestSuite
    test_suite.addTest(unittest.makeSuite(SetToString))
    return test_suite


if __name__ == '__main__':
    suite = suite()
    unit_test_runner = unittest.TextTestRunner()
    unit_test_runner.run(suite)

