import requests
import profiler

session = requests.Session()


class HtmlParsing:

    def __init__(self, my_url):
        self.my_url = my_url
        self.tv_series = False
        self.title = ""
        self.date = ""
        self.rating = 0
        self.genres = ""
        self.directors = ""
        self.writers = ""
        self.cast = ""
        self.related_films = ""
        self.links_to_related_films = []

    def request_html(self):
        page_html = session.get(self.my_url, stream=True).text
        return page_html

    @staticmethod
    def list_to_string(input_list):
        converted_string = str(input_list)
        for ch in ['[', ']', "'", '"']:
            if ch in converted_string:
                converted_string = converted_string.replace(ch, '')

        converted_string = converted_string.replace(',', ';')
        return converted_string

    @staticmethod
    def has_met_requirements(page_soup):
        amount_of_user_reviews_span = page_soup.find("span", {"class": "score"}).text

        if amount_of_user_reviews_span[-1] == "K":
            thousands_of_reviews = amount_of_user_reviews_span.strip("K")
            amount_of_user_reviews = int(float(thousands_of_reviews) * 1000)
        else:
            amount_of_user_reviews = int(amount_of_user_reviews_span)

        minimum_amount_user_reviews = 150
        return amount_of_user_reviews > minimum_amount_user_reviews

    def set_title(self, page_soup):
        title_div_tag = page_soup.find("div", {"class": "TitleBlock__TitleContainer-sc-1nlhx7j-1 jxsVNt"})
        self.title = title_div_tag.find("h1").text.strip()

    def set_date(self, page_soup):
        date_div = page_soup.find("div", {"class": "TitleBlock__TitleMetaDataContainer-sc-1nlhx7j-2 hWHMKr"})
        self.date = date_div.find("a").text.strip()

    def get_title_and_date(self, page_soup):
        self.set_title(page_soup)
        if not self.tv_series:
            self.set_date(page_soup)

    def get_rating(self, page_soup):
        required_class_string = "AggregateRatingButton__RatingScore-sc-1ll29m0-1 iTLWoV"
        self.rating = page_soup.find("span", {"class": required_class_string}).text

    def get_genre(self, page_soup):
        genre_div = page_soup.find("div", {"class": "ipc-chip-list GenresAndPlot__GenresChipList-cum89p-4 gtBDBL"})
        genres_a_tags = genre_div.findAll("a")
        genres_list = [genre.text for genre in genres_a_tags]

        tv_tag = page_soup.find("li", text="TV Series")
        tv_mini_tag = page_soup.find("li", text="TV Mini Series")
        if tv_tag or tv_mini_tag:
            self.tv_series = True
            genres_list.append("TV Series")

        self.genres = self.list_to_string(genres_list)

    @profiler.profile
    def get_writers_and_directors(self, page_soup):
        # Credits for directors and writers
        directors = []
        writers = []

        credit_divs = page_soup.findAll("div", {"class": "ipc-metadata-list-item__content-container"})
        for div in range(3):
            credit_div_a = credit_divs[div].findAll("a")
            for name in credit_div_a:
                if "more credit" not in name.text:
                    # Program only needs each credited name once
                    if div == 0 and name not in directors:
                        directors.append(name.text)
                    elif div == 1 and name not in writers:
                        writers.append(name.text)

        self.directors = self.list_to_string(directors)
        self.writers = self.list_to_string(writers)

    def get_cast(self, page_soup):
        cast_name_tags = page_soup.findAll("a", {"class": "StyledComponents__ActorName-y9ygcu-1 eyqFnv"})
        cast = [actor.text for actor in cast_name_tags]
        self.cast = self.list_to_string(cast)

    def get_related_films(self, page_soup):
        # Find related films and find new films to check
        liked_films_all_data = page_soup.findAll("span", {"data-testid": "title"})
        list_of_related_films = [film.text for film in liked_films_all_data]
        self.related_films = self.list_to_string(list_of_related_films)

    def get_related_urls(self, page_soup):
        root_link = "https://www.imdb.com"
        related_films_div = page_soup.findAll("div", {"class": "ipc-poster ipc-poster--base ipc-poster--dynamic-width ipc-poster-card__poster ipc-sub-grid-item ipc-sub-grid-item--span-2"})
        for div in related_films_div:
            related_film_a_tags = div.findAll("a", {"class": "ipc-lockup-overlay ipc-focusable"})
            for link in related_film_a_tags:
                important_link, _ = link['href'].split("?")
                new_link = root_link + important_link
                self.links_to_related_films.append(new_link)
