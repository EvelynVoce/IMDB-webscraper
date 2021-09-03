import csv


def write_film_data(title, date, rating, genres, directors, writers, cast,
                    related_films_string):  # title, date, review_score, genres_string, directors_string, writers_string, cast_names, list_of_related_films):
    with open('films_data.csv', 'a', newline='') as file:
        fieldnames = ['title', 'release date', 'rating', 'genres', 'directors', 'writers', 'cast_names',
                      'related films', 'score']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(
            {'title': title, 'release date': date, 'rating': rating, 'genres': genres, 'directors': directors,
             'writers': writers, 'cast_names': cast, 'related films': related_films_string, 'score': 0})


def update_text_files(list_of_film_data):
    with open("film_completed.txt", "a") as films_done:
        for link in list_of_film_data:
            films_done.write(link.my_url + "\n")

    with open("film_incompleted.txt", "w") as films_not_done:
        for film in list_of_film_data:
            for related_link in film.links_to_related_films:
                films_not_done.write(related_link + '\n')
