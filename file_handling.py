import csv
import os


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


def update_text_files(related_links, set_of_links_to_be_completed):
    with open("film_completed.txt", "a") as films_done:
        for link in set_of_links_to_be_completed:
            films_done.write(link + "\n")

    with open("film_incompleted.txt", "w") as films_not_done:
        for related_link in related_links:
            films_not_done.write(related_link + "\n")
