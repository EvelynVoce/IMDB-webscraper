from requests import Session
from bs4 import BeautifulSoup as Soup


class HtmlParsing:
    session = Session()

    def __init__(self, my_url):
        self.my_url = my_url

        page_html = self.request_html()
        self.page_soup = Soup(page_html, "lxml")
        self.met_requirements = self.has_met_requirements()

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

    @staticmethod
    def list_to_string(input_list):
        converted_string = str(input_list)
        for ch in [('[', ''), (']', ''), ('{', ''), ('}', ''), ("'", ''), ('"', ''), (',', ';')]:
            if ch[0] in converted_string:
                converted_string = converted_string.replace(ch[0], ch[1])
        return converted_string

    def request_html(self):
        return self.session.get(self.my_url, stream=True).text

    def has_met_requirements(self):
        amount_of_user_reviews_span = self.page_soup.find("span", {"class": "score"}).text

        if amount_of_user_reviews_span[-1] == "K":
            thousands_of_reviews = amount_of_user_reviews_span.strip("K")
            amount_of_user_reviews = int(float(thousands_of_reviews) * 1000)
        else:
            amount_of_user_reviews = int(amount_of_user_reviews_span)

        minimum_amount_user_reviews = 150
        return amount_of_user_reviews > minimum_amount_user_reviews

    def set_title(self):
        title_div_tag = self.page_soup.find("div", {"class": "TitleBlock__TitleContainer-sc-1nlhx7j-1 jxsVNt"})
        self.title = title_div_tag.find("h1").text.strip()

    def set_date(self):
        date_div = self.page_soup.find("div", {"class": "TitleBlock__TitleMetaDataContainer-sc-1nlhx7j-2 hWHMKr"})
        self.date = date_div.find("a").text.strip()

    def get_title_and_date(self):
        self.set_title()
        if not self.tv_series:
            self.set_date()
        else:
            self.date = 0

    def get_rating(self):
        required_class_string = "AggregateRatingButton__RatingScore-sc-1ll29m0-1 iTLWoV"
        self.rating = self.page_soup.find("span", {"class": required_class_string}).text

    def get_genre(self):
        genre_div = self.page_soup.find("div", {"class": "ipc-chip-list GenresAndPlot__GenresChipList-cum89p-4 gtBDBL"})
        genres_a_tags = genre_div.findAll("a")
        genres_list = [genre.text for genre in genres_a_tags]

        tv_tag = self.page_soup.find("li", text="TV Series")
        tv_mini_tag = self.page_soup.find("li", text="TV Mini Series")

        if tv_tag or tv_mini_tag:
            self.tv_series = True
            genres_list.append("TV Series")

        self.genres = self.list_to_string(genres_list)

    def get_writers_and_directors(self):
        credit_divs = self.page_soup.findAll("div", {"class": "ipc-metadata-list-item__content-container"})
        for index, div in enumerate(credit_divs[:2]):
            credit_div_a = div.findAll("a")
            temporary_set = {name.text for name in credit_div_a if "more credit" not in name.text}

            if index == 0:
                self.directors = self.list_to_string(temporary_set)
            elif index == 1:
                self.writers = self.list_to_string(temporary_set)

    def get_cast(self):
        cast_name_tags = self.page_soup.findAll("a", {"class": "StyledComponents__ActorName-y9ygcu-1 eyqFnv"})
        cast = [actor.text for actor in cast_name_tags]
        self.cast = self.list_to_string(cast)

    def get_related_films(self):  # Find related films
        liked_films_all_data = self.page_soup.findAll("span", {"data-testid": "title"})
        list_of_related_films = [film.text for film in liked_films_all_data]
        self.related_films = self.list_to_string(list_of_related_films)

    def get_related_urls(self):
        root_link = "https://www.imdb.com"
        related_films_div = self.page_soup.findAll("div", {"class": "ipc-poster ipc-poster--base ipc-poster--dynamic"
                                                                    "-width ipc-poster-card__poster ipc-sub-grid-item"
                                                                    " ipc-sub-grid-item--span-2"})
        for div in related_films_div:
            link = div.find("a", {"class": "ipc-lockup-overlay ipc-focusable"})
            important_link, _ = link['href'].split("?")
            new_link = root_link + important_link
            self.links_to_related_films.append(new_link)
