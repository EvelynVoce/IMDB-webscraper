from csv import DictWriter
from os import path

FILMS_CSV_FILE = "films_data.csv"
LINKS_TO_SCRAPE_FILE = "films_not_completed.txt"


def retrieve_file(file_name):
    links_to_scrape_exists = path.isfile(file_name)
    if not links_to_scrape_exists:
        initiate_files(file_name)
    return read_file(file_name)


def initiate_files(file_name):
    endgame_link = "https://www.imdb.com/title/tt4154796/"
    with open(file_name, "w") as text_file:
        text_file.write(endgame_link) if file_name == LINKS_TO_SCRAPE_FILE else text_file.write("")


def read_file(file_name):
    with open(file_name, "r") as text_file:
        return text_file.read().splitlines()


def write_film_data(list_of_film_data):
    fieldnames = ["title", "release date", "rating", "genres", "directors", "writers", "cast_names", "related films"]
    file_exists = path.isfile(FILMS_CSV_FILE)

    with open(FILMS_CSV_FILE, "a", newline="") as file:
        writer = DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()

        for film_data in list_of_film_data:
            writer.writerow(
                {"title": film_data.title,  "release date": film_data.date, "rating": film_data.rating,
                 "genres": film_data.genres, "directors": film_data.directors,  "writers": film_data.writers,
                 "cast_names": film_data.cast,  "related films": film_data.related_films})


def update_text_file(file_name, array_to_iterate_over, file_mode):
    completed_films = read_file("films_completed.txt")
    with open(file_name, file_mode) as text_file:
        for link in array_to_iterate_over:
            if link not in completed_films:
                text_file.write(link + "\n")