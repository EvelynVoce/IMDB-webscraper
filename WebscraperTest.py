import unittest
from HTML_parsing import HtmlParsing
from requests import Session

session = Session()

endgame_link = "https://www.imdb.com/title/tt4154796/"
parsed_endgame = HtmlParsing(endgame_link, session)

slender_man_link = "https://www.imdb.com/title/tt5690360/"
parsed_slender_man_film = HtmlParsing(slender_man_link, session)


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
        russian_link = "https://www.imdb.com/title/tt0386134/"
        parsed_russian_film = HtmlParsing(russian_link, session)
        self.assertEqual(False, parsed_russian_film.met_requirements)


class SetTitle(unittest.TestCase):
    def test_title_endgame(self):
        self.assertEqual('Avengers: Endgame', parsed_endgame.title)

    def test_title_slender_man(self):
        self.assertEqual("Slender Man", parsed_slender_man_film.title)


if __name__ == '__main__':
    unittest.main()
