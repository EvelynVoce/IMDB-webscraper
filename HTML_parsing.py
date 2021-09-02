import requests

session = requests.Session()


class HtmlParsing:
    met_requirements = False
    title = ""
    date = ""

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
        print(self.title, flush=True)

    def set_date(self, page_soup):
        date_div = page_soup.find("div", {"class": "TitleBlock__TitleMetaDataContainer-sc-1nlhx7j-2 hWHMKr"})
        self.date = date_div.find("a").text.strip()

    def get_title_and_date(self, page_soup, tv_series=0):
        self.set_title(page_soup)
        if not tv_series:
            self.set_date(page_soup)

        else:
            self.date = ""  # TV shows come with date range which isn't required for this application

        # print(self.title, self.date)