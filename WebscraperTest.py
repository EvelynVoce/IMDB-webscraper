import unittest
from HTML_parsing import HtmlParsing
from requests import Session

session = Session()

endgame_link = "https://www.imdb.com/title/tt4154796/"
parsed_endgame = HtmlParsing(endgame_link, session)

russian_link = "https://www.imdb.com/title/tt0386134/?ref_=adv_li_tt"
parsed_russian_film = HtmlParsing(russian_link, session)


class SetToString(unittest.TestCase):
    def test_empty_set(self):
        self.assertEqual("", parsed_endgame.set_to_string({}))

    def test_singular_element(self):
        self.assertEqual("Ab1_$", parsed_endgame.set_to_string(["Ab1_$"]))

    def test_changing_comma(self):  # Tests that commas are being replaced with semi-colons
        self.assertEqual("Ab1_$; B*", parsed_endgame.set_to_string(["Ab1_$", 'B*']))


class HasMetRequirements(unittest.TestCase):
    def test_popular_film(self):
        self.assertEqual(True, parsed_endgame.met_requirements)

    def test_unpopular_film(self):
        self.assertEqual(False, parsed_russian_film.met_requirements)


def suite():
    test_suite = unittest.TestSuite
    test_suite.addTest(unittest.makeSuite(SetToString))
    return test_suite


if __name__ == '__main__':
    suite = suite()
    unit_test_runner = unittest.TextTestRunner()
    unit_test_runner.run(suite)

