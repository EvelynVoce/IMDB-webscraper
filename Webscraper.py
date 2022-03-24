from requests import Session
from concurrent.futures import ThreadPoolExecutor
from HTML_parsing import HtmlParsing
import file_handling
from time import perf_counter

from analysis import make_plot, run_analysis

film_data: list[HtmlParsing] = []


def fetch(link, session):
    parse: HtmlParsing = HtmlParsing(link, session)
    if parse.met_requirements:
        film_data.append(parse)


def main():
    links_scraped_file: str = "films_completed.txt"
    links_to_be_completed: set[str] = file_handling.retrieve_file(file_handling.LINKS_TO_SCRAPE_FILE)
    t1: float = perf_counter()
    while links_to_be_completed:
        with ThreadPoolExecutor(max_workers=20) as p, Session() as session:
            p.map(fetch, links_to_be_completed, [session] * len(links_to_be_completed))

        file_handling.write_film_data(film_data)
        links_found: set[str] = {rel_film for film in film_data for rel_film in film.links_to_related_films}
        film_data.clear()
        file_handling.update_text_file(links_scraped_file, links_to_be_completed, "a")
        file_handling.update_text_file(file_handling.LINKS_TO_SCRAPE_FILE, links_found, "w")
        links_to_be_completed: set[str] = file_handling.retrieve_file(file_handling.LINKS_TO_SCRAPE_FILE)

        run_analysis(t1)
    make_plot()


if __name__ == "__main__":
    main()
