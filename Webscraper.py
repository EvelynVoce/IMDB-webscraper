from time import perf_counter
from concurrent.futures import ThreadPoolExecutor
from profiler import profile
import HTML_parsing
import file_handling

list_of_film_data = []


def setup():
    with open("film_completed.txt", "r") as films_done:
        list_of_links_completed = films_done.read().splitlines()
    with open("film_incompleted.txt", "r") as films_not_done:
        list_of_links_to_be_completed = films_not_done.read().splitlines()
    return list_of_links_to_be_completed, list_of_links_completed


@profile
def get_data(parse):
    parse.get_genre()
    parse.get_title_and_date()
    parse.get_rating()
    parse.get_writers_and_directors()
    parse.get_cast()
    parse.get_related_films()
    parse.get_related_urls()


def fetch(link):
    parse = HTML_parsing.HtmlParsing(link)
    if parse.met_requirements:
        get_data(parse)
        list_of_film_data.append(parse)


def main():
    while 1:
        list_of_film_data.clear()
        links_to_be_completed, list_of_links_completed = setup()
        set_of_links_to_be_completed = {link for link in links_to_be_completed if link not in list_of_links_completed}

        t1 = perf_counter()
        with ThreadPoolExecutor(10) as p:
            p.map(fetch, set_of_links_to_be_completed)
        print(perf_counter() - t1, "\n\n")

        file_handling.write_film_data(list_of_film_data)

        list_of_links_to_write = [rel_film for film in list_of_film_data for rel_film in film.links_to_related_films]
        file_handling.update_text_files(list_of_links_to_write, set_of_links_to_be_completed)
        print("Iteration complete")


if __name__ == '__main__':
    main()
