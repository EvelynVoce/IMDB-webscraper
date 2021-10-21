from bs4 import BeautifulSoup as Soup


class HtmlParsing:
    __slots__ = ['page_soup', 'met_requirements', 'title', 'date', 'rating', 'genres', 'directors',
                 'writers', 'cast', 'related_films', 'links_to_related_films']

    def __init__(self, my_url, session):
        page_html = session.get(my_url, stream=True).text
        self.page_soup = Soup(page_html, "lxml")
        self.met_requirements: bool = self.has_met_requirements()
        if self.met_requirements:
            self.title: str = self.set_title()
            self.date: str = self.set_date()
            self.rating: str = self.get_rating()
            self.genres: str = self.set_to_string(self.get_genre())
            self.directors: str = ""
            self.writers: str = ""
            self.get_writers_and_directors()
            self.cast: str = self.set_to_string(self.get_cast())
            self.related_films: str = self.set_to_string(self.get_related_films())
            self.links_to_related_films: list = self.get_related_urls()

    @staticmethod
    def set_to_string(input_list) -> str:
        converted_string: str = str(input_list)
        for ch in [("[", ""), ("]", ""), ("{", ""), ("}", ""), ('"', ""), ("'", ""), (",", ";")]:
            converted_string: str = converted_string.replace(ch[0], ch[1])
        return converted_string

    def has_met_requirements(self) -> bool:
        amount_of_user_reviews_span: str = self.page_soup.find("span", {"class": "score"}).text
        if amount_of_user_reviews_span[-1] == "K":
            amount_of_user_reviews: float = float(amount_of_user_reviews_span[:-1]) * 1000
        else:
            amount_of_user_reviews: int = int(amount_of_user_reviews_span)

        minimum_amount_user_reviews: int = 125
        return amount_of_user_reviews > minimum_amount_user_reviews

    def set_title(self) -> str:
        title_div_tag = self.page_soup.find("div", {"class": "TitleBlock__TitleContainer-sc-1nlhx7j-1 jxsVNt"})
        return title_div_tag.find("h1").text.strip()

    def set_date(self) -> str:
        date_div = self.page_soup.find("div", {"class": "TitleBlock__TitleMetaDataContainer-sc-1nlhx7j-2 hWHMKr"})
        found_date: str = date_div.find("a").text.strip()
        return found_date.split("–")[0]

    def get_rating(self) -> str:
        return self.page_soup.find("span", {"class": "AggregateRatingButton__RatingScore-sc-1ll29m0-1 iTLWoV"}).text

    def get_genre(self) -> set:
        genre_div = self.page_soup.find("div", {"class": "ipc-chip-list GenresAndPlot__GenresChipList-cum89p-4 gtBDBL"})
        genres_a_tags = genre_div.findAll("a")
        genres_set: set = {genre.text for genre in genres_a_tags}

        tv_tag = self.page_soup.find("li", text="TV Series")
        tv_mini_tag = self.page_soup.find("li", text="TV Mini Series")
        if tv_tag or tv_mini_tag:
            genres_set.add("TV Series")
        return genres_set

    def get_writers_and_directors(self):
        credit_divs = self.page_soup.findAll("div", {"class": "ipc-metadata-list-item__content-container"})
        for index, div in enumerate(credit_divs[:2]):
            credit_div_a = div.findAll("a")
            temporary_set: set = {name.text for name in credit_div_a}
            if index == 0:
                self.directors = self.set_to_string(temporary_set)
            else:
                self.writers = self.set_to_string(temporary_set)

    def get_cast(self) -> set:
        cast_name_tags = self.page_soup.findAll("a", {"class": "StyledComponents__ActorName-y9ygcu-1 eyqFnv"})
        return {actor.text for actor in cast_name_tags}

    def get_related_films(self) -> set:  # Find related films
        liked_films_all_data = self.page_soup.findAll("span", {"data-testid": "title"})
        return {film.text for film in liked_films_all_data}

    def get_related_urls(self) -> list:
        root_link: str = "https://www.imdb.com"
        related_films_div = self.page_soup.findAll("div", {"class": "ipc-poster ipc-poster--base ipc-poster--dynamic"
                                                                    "-width ipc-poster-card__poster ipc-sub-grid-item"
                                                                    " ipc-sub-grid-item--span-2"})
        return [root_link + div.find("a")["href"].split("?")[0] for div in related_films_div]
