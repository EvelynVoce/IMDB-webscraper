from pytest import mark
from HTML_parsing import HtmlParsing
from requests import Session

session = Session()

endgame_link: str = "https://www.imdb.com/title/tt4154796/"
parsed_endgame = HtmlParsing(endgame_link, session)

slender_man_link: str = "https://www.imdb.com/title/tt5690360/"
parsed_slender_man_film = HtmlParsing(slender_man_link, session)

russian_link: str = "https://www.imdb.com/title/tt0386134/"
parsed_russian_film = HtmlParsing(russian_link, session)

doctor_who_link: str = "https://www.imdb.com/title/tt0436992/"
parsed_dr_who_show = HtmlParsing(doctor_who_link, session)


@mark.parametrize("expected_answer, answer",
                  [("", parsed_endgame.set_to_string({})),
                   ("Ab1_$", parsed_endgame.set_to_string(["Ab1_$"])),
                   ("Ab1_$; B*", parsed_endgame.set_to_string(["Ab1_$", 'B*']))])
def test_set_to_string(expected_answer, answer):
    assert expected_answer == answer


@mark.parametrize("expected_answer, answer",
                  [(True, parsed_endgame.met_requirements), (False, parsed_russian_film.met_requirements)])
def test_met_requirements(expected_answer, answer):
    assert expected_answer == answer


@mark.parametrize("expected_answer, answer",
                  [("Avengers: Endgame", parsed_endgame.title), ("Slender Man", parsed_slender_man_film.title)])
def test_title(expected_answer, answer):
    assert expected_answer == answer


@mark.parametrize("expected_answer, answer", [(parsed_endgame.date, "2019"), (parsed_slender_man_film.date, "2018"),
                                              (parsed_dr_who_show.date, "2005")])
def test_date(expected_answer, answer):
    assert expected_answer == answer


@mark.parametrize("expected_answer, answer", [("8.4", parsed_endgame.rating), ("3.2", parsed_slender_man_film.rating)])
def test_rating(expected_answer, answer):
    assert expected_answer == answer


@mark.parametrize("expected_answer, object_passed",
                  [({'Adventure', 'Action', 'Drama'}, parsed_endgame),
                   ({'Horror', 'Mystery', 'Thriller'}, parsed_slender_man_film)])
def test_genre(expected_answer, object_passed):
    actual_answer = object_passed.get_genre()
    assert actual_answer == expected_answer


@mark.parametrize("expected_answer, object_passed",
                  [({'Stan Lee', 'Christopher Markus', 'Stephen McFeely'}, parsed_endgame),
                   ({'David Birke', 'Victor Surge'}, parsed_slender_man_film)])
def test_writers(expected_answer, object_passed):
    expected_result_list = object_passed.writers.split(';')
    actual_answer: set[str] = {x.strip() for x in expected_result_list}
    assert actual_answer == expected_answer


@mark.parametrize("expected_answer, object_passed",
                  [({'Anthony Russo', 'Joe Russo'}, parsed_endgame),
                   ({'Sylvain White'}, parsed_slender_man_film)])
def test_directors(expected_answer, object_passed):
    expected_result_list = object_passed.directors.split(';')
    set_results = {x.strip() for x in expected_result_list}
    assert set_results == expected_answer


@mark.parametrize("expected_answer, object_passed",
                  [({'Jeremy Renner', 'Karen Gillan', 'Don Cheadle', 'Tessa Thompson', 'Scarlett Johansson',
                     'Evangeline Lilly', 'Zoe Saldana', 'Chris Evans', 'Brie Larson', 'Mark Ruffalo',
                     'Paul Rudd', 'Chadwick Boseman', 'Robert Downey Jr.', 'Tom Holland', 'Benedict Cumberbatch',
                     'Chris Hemsworth', 'Rene Russo', 'Elizabeth Olsen'}, parsed_endgame),
                   ({"Damon D'Amico Jr.", 'Kris Sidberry', 'Annalise Basso', 'Jaz Sinclair',
                     'Joey King', 'Angela Hope Smith', 'Alex Fitzalan', 'Kevin Chapman', 'Jessica Blank',
                     'Javier Botet', 'Miguel Nascimento', 'Taylor Richardson', 'Eddie Frateschi', 'Marc Carver',
                     'Michael Reilly Burke', 'Julia Goldani Telles', 'Oscar Wahlberg', 'Danny Beaton'},
                    parsed_slender_man_film)])
def test_cast(expected_answer, object_passed):
    actual_answer = object_passed.get_cast()
    assert expected_answer == actual_answer


# This test worked at the time it was created, it suffers from the fact that IMDBs related films can change
@mark.parametrize("expected_answer, object_passed",
                  [({'https://www.imdb.com/title/tt4154756/', 'https://www.imdb.com/title/tt0848228/',
                     'https://www.imdb.com/title/tt2395427/', 'https://www.imdb.com/title/tt3501632/',
                     'https://www.imdb.com/title/tt7286456/', 'https://www.imdb.com/title/tt3498820/',
                     'https://www.imdb.com/title/tt0468569/', 'https://www.imdb.com/title/tt0816692/',
                     'https://www.imdb.com/title/tt1375666/', 'https://www.imdb.com/title/tt1825683/',
                     'https://www.imdb.com/title/tt1211837/', 'https://www.imdb.com/title/tt1843866/'},
                    parsed_endgame),
                   ({'https://www.imdb.com/title/tt4030600/', 'https://www.imdb.com/title/tt1204977/',
                    'https://www.imdb.com/title/tt5814060/', 'https://www.imdb.com/title/tt4913966/',
                    'https://www.imdb.com/title/tt8350360/', 'https://www.imdb.com/title/tt5734576/',
                    'https://www.imdb.com/title/tt3322940/', 'https://www.imdb.com/title/tt0837563/',
                    'https://www.imdb.com/title/tt10551346/', 'https://www.imdb.com/title/tt6772950/',
                    'https://www.imdb.com/title/tt3317158/', 'https://www.imdb.com/title/tt5726086/'},
                    parsed_slender_man_film)])
def test_related_films(expected_answer, object_passed):
    actual_answer: set = set(object_passed.get_related_urls())
    assert expected_answer == actual_answer
