from time import perf_counter
from profiler import profile
from requests import Session
from concurrent.futures import ThreadPoolExecutor
import HTML_parsing
import file_handling

list_of_film_data = []
LINKS_SCRAPED_FILE = "films_completed.txt"


def get_data(parse):
    parse.get_genre()
    parse.get_title_and_date()
    parse.get_rating()
    parse.get_writers_and_directors()
    parse.get_cast()
    parse.get_related_films()
    parse.get_related_urls()


# @profile
def fetch(link, session):
    parse = HTML_parsing.HtmlParsing(link, session)
    if parse.met_requirements:
        get_data(parse)
        list_of_film_data.append(parse)


def main():
    links_to_be_completed = file_handling.retrieve_file(file_handling.LINKS_TO_SCRAPE_FILE)
    if len(links_to_be_completed) == 0:
        exit()
    list_of_links_completed = file_handling.retrieve_file(LINKS_SCRAPED_FILE)
    set_of_links_to_be_completed = {link for link in links_to_be_completed if link not in list_of_links_completed}

    t1 = perf_counter()
    with ThreadPoolExecutor(max_workers=20) as p:
        with Session() as session:
            p.map(fetch, set_of_links_to_be_completed, [session] * len(set_of_links_to_be_completed))
    print(perf_counter() - t1, "\n")

    file_handling.write_film_data(list_of_film_data)

    links_to_write = {rel_film for film in list_of_film_data for rel_film in film.links_to_related_films}
    file_handling.update_text_file(LINKS_SCRAPED_FILE, set_of_links_to_be_completed, "a")
    file_handling.update_text_file(file_handling.LINKS_TO_SCRAPE_FILE, links_to_write, "w")

    list_of_film_data.clear()

    print("Iteration complete")


if __name__ == "__main__":
    while True:
        main()
