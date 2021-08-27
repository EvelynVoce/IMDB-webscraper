import requests


class HtmlParsing:

    @staticmethod
    def request_html(my_url):
        continue_collecting_data = True
        page_html = None
        # try:
        page_html = requests.get(my_url, stream=True).text

        # except:
            # continue_collecting_data = False
            # print("CONNECTION ERROR")
        return continue_collecting_data, page_html

    @staticmethod
    def get_amount_of_reviews(page_soup) -> bool:
        amount_of_user_reviews_span = page_soup.find("span", {"class": "score"}).text
        met_requirements = False

        if amount_of_user_reviews_span[-1] == "K":
            thousands_of_reviews = amount_of_user_reviews_span.strip("K")
            amount_of_user_reviews = int(float(thousands_of_reviews) * 1000)
        else:
            amount_of_user_reviews = int(amount_of_user_reviews_span)

        print("User reviews", amount_of_user_reviews)

        if amount_of_user_reviews > 250:
            met_requirements = True

        return met_requirements

    @staticmethod
    def get_title_and_date(page_soup, tv_series=0):
        if not tv_series:
            title_div_tag = page_soup.find("div", {"class": "TitleBlock__TitleContainer-sc-1nlhx7j-1 jxsVNt"})
            title = title_div_tag.find("h1").text

            date_div = page_soup.find("div", {"class": "TitleBlock__TitleMetaDataContainer-sc-1nlhx7j-2 hWHMKr"})
            date = date_div.find("a").text

        else:
            title_div_tag = page_soup.find("div", {"class": "TitleBlock__TitleContainer-sc-1nlhx7j-1 jxsVNt"})
            title = title_div_tag.find("h1").text
            date = "" # TV shows come with date range which isn't required for this application

        title = title.strip()
        date = date.strip()
        print(title, date)
        return title, date
