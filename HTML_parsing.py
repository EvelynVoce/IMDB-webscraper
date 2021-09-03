import requests

session = requests.Session()


class HtmlParsing:

    def __init__(self):
        self.met_requirements = False
        self.title = ""
        self.date = ""
        self.genres = ""
        self.directors = ""
        self.writers = ""
        self.cast = ""

    def print_stats(self):
        print(self.title, self.directors, self.writers, self.cast)

    @staticmethod
    def request_html(my_url):
        continue_collecting_data = True
        page_html = None
        # try:
        page_html = session.get(my_url, stream=True).text

        # except:
            # continue_collecting_data = False
            # print("CONNECTION ERROR")
        return continue_collecting_data, page_html

    @staticmethod
    def list_to_string(input_list):
        converted_string = str(input_list)
        for ch in ['[', ']', "'", '"']:
            if ch in converted_string:
                converted_string = converted_string.replace(ch, '')
        return converted_string

    def has_met_requirements(self, page_soup):
        amount_of_user_reviews_span = page_soup.find("span", {"class": "score"}).text

        if amount_of_user_reviews_span[-1] == "K":
            thousands_of_reviews = amount_of_user_reviews_span.strip("K")
            amount_of_user_reviews = int(float(thousands_of_reviews) * 1000)
        else:
            amount_of_user_reviews = int(amount_of_user_reviews_span)

        # print("User reviews", amount_of_user_reviews)

        if amount_of_user_reviews > 250:
            self.met_requirements = True

        return self.met_requirements

    def set_title(self, page_soup):
        title_div_tag = page_soup.find("div", {"class": "TitleBlock__TitleContainer-sc-1nlhx7j-1 jxsVNt"})
        self.title = title_div_tag.find("h1").text.strip()

    def set_date(self, page_soup):
        date_div = page_soup.find("div", {"class": "TitleBlock__TitleMetaDataContainer-sc-1nlhx7j-2 hWHMKr"})
        self.date = date_div.find("a").text.strip()

    def get_title_and_date(self, page_soup, tv_series=0):
        self.set_title(page_soup)
        if not tv_series:
            self.set_date(page_soup)

    def get_genre(self, page_soup):
        genre_div = page_soup.find("div", {"class": "ipc-chip-list GenresAndPlot__GenresChipList-cum89p-4 gtBDBL"})
        genres_a_tags = genre_div.findAll("a")
        genres_list = [genre.text for genre in genres_a_tags]
        self.genres = self.list_to_string(genres_list)

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
        cast = []
        cast_name_tags = page_soup.findAll("a", {"class": "StyledComponents__ActorName-y9ygcu-1 eyqFnv"})
        for actor in cast_name_tags:
            cast.append(actor.text)
        self.cast = self.list_to_string(cast)