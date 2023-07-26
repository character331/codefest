from newsapi.newsapi_client import NewsApiClient
import datetime

class NewsAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.newsapi = NewsApiClient(api_key=self.api_key)

    def search_articles(self, location=None, keyword=None, time=None):
        if not time:
            time = (datetime.date.today() - datetime.timedelta(days=25)).strftime("%Y-%m-%d")
        if isinstance(time, tuple):
            from_date, to_date = time
            from_param = from_date.strftime("%Y-%m-%d")
            to_param = to_date.strftime("%Y-%m-%d")
        else:
            from_param = to_param = time
            
        if location:
            keyword += f" {location}"
        response = self.newsapi.get_everything(q=keyword, from_param=from_param, to=to_param, language="en", sort_by="publishedAt")
        if response["status"] == "ok":
            articles = response["articles"]
            urls = []
            for article in articles:
                url = article["url"]
                urls.append(url)
                # print(url)
            return urls
        else:
            print("Error: API request failed.")


import requests
import datetime


class NYTAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"

    def search_articles(self, query):
        # Calculate the date range for the most recent month
        today = datetime.date.today()
        week_ago = today - datetime.timedelta(days=30)

        # Set the search parameters
        params = {
            "q": query,
            "api-key": self.api_key,
            "begin_date": week_ago.strftime("%Y%m%d"),
            "end_date": today.strftime("%Y%m%d"),
            "sort": "newest"
        }

        # Send the request to the API
        response = requests.get(self.base_url, params=params).json()

        # Extract the article URLs from the API response
        urls = []
        for article in response["response"]["docs"]:
            urls.append(article["web_url"])

        return urls[:10]


