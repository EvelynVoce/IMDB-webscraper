import pytest
from HTML_parsing import HtmlParsing
from requests import Session

session = Session()

endgame_link = "https://www.imdb.com/title/tt4154796/"
parsed_endgame = HtmlParsing(endgame_link, session)

slender_man_link = "https://www.imdb.com/title/tt5690360/"
parsed_slender_man_film = HtmlParsing(slender_man_link, session)

russian_link = "https://www.imdb.com/title/tt0386134/"
parsed_russian_film = HtmlParsing(russian_link, session)


@pytest.mark.parametrize("expected_answer, answer",
                         [("", parsed_endgame.set_to_string({})),
                          ("Ab1_$", parsed_endgame.set_to_string(["Ab1_$"])),
                          ("Ab1_$; B*", parsed_endgame.set_to_string(["Ab1_$", 'B*']))])
def test_set_to_string(expected_answer, answer):
    assert expected_answer == answer


@pytest.mark.parametrize("expected_answer, answer",
                         [(True, parsed_endgame.met_requirements), (False, parsed_russian_film.met_requirements)])
def test_met_requirements(expected_answer, answer):
    assert expected_answer == answer


@pytest.mark.parametrize("expected_answer, answer",
                         [("Avengers: Endgame", parsed_endgame.title), ("Slender Man", parsed_slender_man_film.title)])
def test_title(expected_answer, answer):
    assert expected_answer == answer


@pytest.mark.parametrize("expected_answer, answer",
                         [("2019", parsed_endgame.date), ("2018", parsed_slender_man_film.date)])
def test_date(expected_answer, answer):
    assert expected_answer == answer


@pytest.mark.parametrize("expected_answer, answer",
                         [("8.4", parsed_endgame.rating), ("3.2", parsed_slender_man_film.rating)])
def test_rating(expected_answer, answer):
    assert expected_answer == answer


@pytest.mark.parametrize("expected_answer, object_passed",
                         [({'Adventure', 'Action', 'Drama'}, parsed_endgame),
                          ({'Horror', 'Mystery', 'Thriller'}, parsed_slender_man_film)])
def test_genre(expected_answer, object_passed):
    actual_answer = object_passed.get_genre()
    assert expected_answer == actual_answer


@pytest.mark.parametrize("expected_answer, object_passed",
                         [({'Jeremy Renner', 'Karen Gillan', 'Don Cheadle', 'Tessa Thompson', 'Scarlett Johansson',
                            'Evangeline Lilly', 'Zoe Saldana', 'Chris Evans', 'Brie Larson', 'Mark Ruffalo',
                            'Paul Rudd', 'Chadwick Boseman', 'Robert Downey Jr.', 'Tom Holland', 'Benedict Cumberbatch',
                            'Chris Hemsworth', 'Rene Russo', 'Elizabeth Olsen'}, parsed_endgame),

                          ({"Damon D'Amico Jr.", 'Kris Sidberry', 'Annalise Basso', 'Jaz Sinclair',
                            'Joey King', 'Angela Hope Smith', 'Alex Fitzalan', 'Kevin Chapman', 'Jessica Blank',
                            'Javier Botet', 'Miguel Nascimento', 'Taylor Richardson', 'Eddie Frateschi', 'Marc Carver',
                            'Michael Reilly Burke', 'Julia Goldani Telles', 'Oscar Wahlberg', 'Danny Beaton'}
                           , parsed_slender_man_film)])
def test_cast(expected_answer, object_passed):
    actual_answer = object_passed.get_cast()
    assert expected_answer == actual_answer


# import unittest
# from HTML_parsing import HtmlParsing
# from requests import Session
#
# #
# session = Session()
#
# endgame_link = "https://www.imdb.com/title/tt4154796/"
# parsed_endgame = HtmlParsing(endgame_link, session)
#
# slender_man_link = "https://www.imdb.com/title/tt5690360/"
# parsed_slender_man_film = HtmlParsing(slender_man_link, session)
#
#
# class SetToString(unittest.TestCase):
#
#
#     def test_empty_set(self):
#         self.assertEqual(expected_answer, parsed_endgame.set_to_string({}))
#
#
#     def test_singular_element(self):
#         self.assertEqual("Ab1_$", parsed_endgame.set_to_string(["Ab1_$"]))
#
#     def test_changing_comma(self):  # Tests that commas are being replaced with semi-colons
#         self.assertEqual("Ab1_$; B*", parsed_endgame.set_to_string(["Ab1_$", 'B*']))
#
#
# class HasMetRequirements(unittest.TestCase):
#     def test_popular_film(self):
#         self.assertEqual(True, parsed_endgame.met_requirements)
#
#     def test_unpopular_film(self):
#         russian_link = "https://www.imdb.com/title/tt0386134/"
#         parsed_russian_film = HtmlParsing(russian_link, session)
#         self.assertEqual(False, parsed_russian_film.met_requirements)
#
#
#
# class SetTitle(unittest.TestCase):
#     def test_title_endgame(self):
#         self.assertEqual('Avengers: Endgame', parsed_endgame.title)
#
#     def test_title_slender_man(self):
#         self.assertEqual("Slender Man", parsed_slender_man_film.title)
#
#
# if __name__ == '__main__':
#     unittest.main()

