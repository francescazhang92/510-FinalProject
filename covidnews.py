import requests

def get_news(from_date, to_date, language = "en", country = "US") -> float:
    url = "https://covid-19-news.p.rapidapi.com/v1/covid"
    querystring = {"from": f"{from_date}",
                   "to": f"{to_date}",
                   "lang": f"{language}",
                   "country":f"{country}"}
    headers = {
        "X-RapidAPI-Key": "e2708eb054msha687acae8d1d3c2p188ddfjsnf4d14e880bc2",
        "X-RapidAPI-Host": "covid-19-news.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    articles = response.json()["articles"]
    news = [(a["title"], a["summary"], a["published_date"]) for a in articles]
    return news

if __name__ == "__main__":
    print(get_news("2022/08/01", "2022/12/01"))