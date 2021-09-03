import csv


def read_files():
    with open("film_completed.txt", "r") as films_done:
        list_of_links_completed = films_done.read().splitlines()  # Gets all the links that have been found but not registered
    with open("film_incompleted.txt", "r") as films_not_done:
        list_of_links_to_be_completed = films_not_done.read().splitlines()
    return list_of_links_to_be_completed[0], list_of_links_to_be_completed, list_of_links_completed


def write_film_data(title, date, rating, genres, directors, writers, cast,
                    related_films_string):  # title, date, review_score, genres_string, directors_string, writers_string, cast_names, list_of_related_films):
    with open('films_data.csv', 'a', newline='') as file:
        fieldnames = ['title', 'release date', 'rating', 'genres', 'directors', 'writers', 'cast_names',
                      'related films', 'score']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(
            {'title': title, 'release date': date, 'rating': rating, 'genres': genres, 'directors': directors,
             'writers': writers, 'cast_names': cast, 'related films': related_films_string, 'score': 0})


def update_text_files(my_url, list_of_links_to_be_completed):
    with open("film_completed.txt", "a") as films_done:
        films_done.write(my_url + "\n")

    # These are outside if statement because if the film fails it will always fail therefore it's considered completeS
    with open("film_incompleted.txt", "w") as films_not_done:
        for film in list_of_links_to_be_completed:
            films_not_done.write(film + '\n')