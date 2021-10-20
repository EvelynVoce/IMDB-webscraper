from requests import Session
from time import perf_counter
from concurrent.futures import ThreadPoolExecutor
from HTML_parsing import HtmlParsing
import file_handling

list_of_film_data = []


def fetch(link, session):
    parse = HtmlParsing(link, session)
    if parse.met_requirements:
        list_of_film_data.append(parse)


def main():
    links_scraped_file = "films_completed.txt"
    links_to_be_completed = file_handling.retrieve_file(file_handling.LINKS_TO_SCRAPE_FILE)
    while links_to_be_completed:
        list_of_links_completed = file_handling.retrieve_file(links_scraped_file)
        set_of_links_to_be_completed = {link for link in links_to_be_completed if link not in list_of_links_completed}
        t1 = perf_counter()

        with ThreadPoolExecutor(max_workers=30) as p, Session() as session:
            p.map(fetch, set_of_links_to_be_completed, [session] * len(set_of_links_to_be_completed))
        print("Iteration complete", perf_counter() - t1)

        file_handling.write_film_data(list_of_film_data)
        links_found = {rel_film for film in list_of_film_data for rel_film in film.links_to_related_films}
        list_of_film_data.clear()
        file_handling.update_text_file(links_scraped_file, set_of_links_to_be_completed, "a")
        file_handling.update_text_file(file_handling.LINKS_TO_SCRAPE_FILE, links_found, "w")
        links_to_be_completed = file_handling.retrieve_file(file_handling.LINKS_TO_SCRAPE_FILE)


if __name__ == "__main__":
    main()
