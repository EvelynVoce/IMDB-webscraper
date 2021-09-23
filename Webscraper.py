from requests import Session
from time import perf_counter
from concurrent.futures import ThreadPoolExecutor
import HTML_parsing
import file_handling

list_of_film_data = []
LINKS_SCRAPED_FILE = "films_completed.txt"


def fetch(link, session):
    parse = HTML_parsing.HtmlParsing(link, session)
    if parse.met_requirements:
        list_of_film_data.append(parse)


def main():
    links_to_be_completed = file_handling.retrieve_file(file_handling.LINKS_TO_SCRAPE_FILE)
    if len(links_to_be_completed) == 0:
        exit()
    list_of_links_completed = file_handling.retrieve_file(LINKS_SCRAPED_FILE)
    set_of_links_to_be_completed = {link for link in links_to_be_completed if link not in list_of_links_completed}

    t1 = perf_counter()
    with ThreadPoolExecutor(max_workers=10) as p:
        with Session() as session:
            p.map(fetch, set_of_links_to_be_completed, [session] * len(set_of_links_to_be_completed))
    print(perf_counter() - t1)
    file_handling.write_film_data(list_of_film_data)

    links_found = {rel_film for film in list_of_film_data for rel_film in film.links_to_related_films}
    file_handling.update_text_file(LINKS_SCRAPED_FILE, set_of_links_to_be_completed, "a")
    file_handling.update_text_file(file_handling.LINKS_TO_SCRAPE_FILE, links_found, "w")

    list_of_film_data.clear()

    print("Iteration complete")


if __name__ == "__main__":
    while True:
        main()
