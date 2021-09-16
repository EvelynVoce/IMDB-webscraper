import csv
import os


def read_file(file_name):
    with open(file_name, "r") as text_file:
        return text_file.read().splitlines()


def write_film_data(list_of_film_data):
    fieldnames = ['title', 'release date', 'rating', 'genres', 'directors', 'writers', 'cast_names', 'related films']
    file_exists = os.path.isfile('films_data.csv')

    with open('films_data.csv', 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()

        for film_data in list_of_film_data:
            writer.writerow(
                {'title': film_data.title, 'release date': film_data.date, 'rating': film_data.rating,
                 'genres': film_data.genres, 'directors': film_data.directors,
                 'writers': film_data.writers, 'cast_names': film_data.cast, 'related films': film_data.related_films})


def update_text_file(file_name, array_to_iterate_over, file_mode):
    with open(file_name, file_mode) as text_file:
        for link in array_to_iterate_over:
            text_file.write(link + "\n")
