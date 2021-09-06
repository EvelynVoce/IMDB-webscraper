from bs4 import BeautifulSoup as Soup
import gc  # garbage collector - really useful for RAM management
import HTML_parsing
import time
from concurrent.futures import ThreadPoolExecutor
import file_handling

list_of_film_data = []


def setup():
    with open("film_completed.txt", "r") as films_done:
        list_of_links_completed = films_done.read().splitlines()
    with open("film_incompleted.txt", "r") as films_not_done:
        list_of_links_to_be_completed = films_not_done.read().splitlines()
    return list_of_links_to_be_completed, list_of_links_completed


def get_data(parse, page_soup):
    parse.get_genre(page_soup)
    parse.get_title_and_date(page_soup)
    parse.get_rating(page_soup)
    parse.get_writers_and_directors(page_soup)
    parse.get_cast(page_soup)
    parse.get_related_films(page_soup)
    parse.get_related_urls(page_soup)


def fetch(link):
    parse = HTML_parsing.HtmlParsing(link)
    continue_collecting_data, page_html = parse.request_html()

    if continue_collecting_data:
        page_soup = Soup(page_html, "lxml")
        get_data(parse, page_soup)
        met_requirements = parse.has_met_requirements(page_soup)
        if met_requirements:
            list_of_film_data.append(parse)
            gc.collect()


def main():
    while 1:
        list_of_film_data.clear()
        list_of_links_to_be_completed, list_of_links_completed = setup()
        list_of_links_to_be_completed[:] = [x for x in list_of_links_to_be_completed if x not in list_of_links_completed]
        set_of_links_to_be_completed = set(list_of_links_to_be_completed)

        t1 = time.perf_counter()
        with ThreadPoolExecutor(10) as p:
            p.map(fetch, set_of_links_to_be_completed)
        print(time.perf_counter() - t1, "\n\n")

        for x in list_of_film_data:
            if x.rating == 0:
                print(x.my_url)

        file_handling.write_film_data(list_of_film_data)
        file_handling.update_text_files(list_of_film_data, set_of_links_to_be_completed)


if __name__ == '__main__':
    main()
