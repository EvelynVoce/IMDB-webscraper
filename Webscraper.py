from bs4 import BeautifulSoup as Soup
import gc  # garbage collector - really useful for RAM management
import HTML_parsing
import time
import requests


def setup():
    with open("film_completed.txt", "r") as films_done:
        list_of_links_completed = films_done.read().splitlines()
    with open("film_incompleted.txt", "r") as films_not_done:
        list_of_links_to_be_completed = films_not_done.read().splitlines()
    return list_of_links_to_be_completed[0], list_of_links_to_be_completed, list_of_links_completed


def get_data(parse, page_soup):
    met_requirements = parse.get_amount_of_reviews(page_soup)
    if met_requirements:
        title, date = parse.get_title_and_date(page_soup)


def main():
    my_url, list_of_links_to_be_completed, list_of_links_completed = setup()

    while len(list_of_links_to_be_completed) > 0:
        t1 = time.perf_counter()

        # s = requests.Session()

        parse = HTML_parsing.HtmlParsing()
        continue_collecting_data, page_html = parse.request_html(my_url)

        if continue_collecting_data:
            page_soup = Soup(page_html, "lxml")
            get_data(parse, page_soup)

        else:  # The line below is neccessary (I want it to get a connection error and loop back and error again so I know it's not an internet issue)
            print("Connection error: ", my_url)

        print(time.perf_counter() - t1)


main()
