from bs4 import BeautifulSoup as Soup
import gc  # garbage collector - really useful for RAM management
import HTML_parsing
import time
from concurrent.futures import ThreadPoolExecutor

list_of_film_data = []


def setup():
    with open("film_completed.txt", "r") as films_done:
        list_of_links_completed = films_done.read().splitlines()
    with open("film_incompleted.txt", "r") as films_not_done:
        list_of_links_to_be_completed = films_not_done.read().splitlines()
    return list_of_links_to_be_completed, list_of_links_completed


def get_data(parse, page_soup):
    met_requirements = parse.has_met_requirements(page_soup)
    if met_requirements:
        parse.get_genre(page_soup)
        parse.get_title_and_date(page_soup)
        parse.get_writers_and_directors(page_soup)
        parse.get_cast(page_soup)
        parse.get_related_films(page_soup)
        parse.get_related_urls(page_soup)


def fetch(link):
    parse = HTML_parsing.HtmlParsing()
    continue_collecting_data, page_html = parse.request_html(link)

    if continue_collecting_data:
        page_soup = Soup(page_html, "lxml")
        get_data(parse, page_soup)

    else:  # The line below is neccessary (I want it to get a connection error and loop back and error again so I know it's not an internet issue)
        print("Connection error: ", link)

    list_of_film_data.append(parse)
    gc.collect()


def main():
    list_of_links_to_be_completed, list_of_links_completed = setup()
    my_url = list_of_links_to_be_completed[0]

    t1 = time.perf_counter()
    with ThreadPoolExecutor(10) as p:
        p.map(fetch, list_of_links_to_be_completed)
    print(time.perf_counter() - t1, "\n\n")

    for x in list_of_film_data:
        print(x.title)
        print(x.date)
        print(x.related_films, "\n")

    for checked_film in list_of_film_data:
        print(checked_film.links_to_related_films)
        

    # while len(list_of_links_to_be_completed) > 0:
    #     t1 = time.perf_counter()
    #
    #     parse = HTML_parsing.HtmlParsing()
    #     continue_collecting_data, page_html = parse.request_html(my_url, session)
    #
    #     if continue_collecting_data:
    #         page_soup = Soup(page_html, "lxml")
    #         get_data(parse, page_soup)
    #
    #     else:  # The line below is neccessary (I want it to get a connection error and loop back and error again so I know it's not an internet issue)
    #         print("Connection error: ", my_url)
    #
    #     print(time.perf_counter() - t1)
    #     list_of_links_to_be_completed.pop(0)
    #     my_url = list_of_links_to_be_completed[0]


if __name__ == '__main__':
    main()
