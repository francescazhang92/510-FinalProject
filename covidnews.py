import requests
import time
import sys
import csv


# The api limits the data access rate by 10 request per minute.
# Therefore, to retrieve all the data, hang this
# script with parameter "2020/03/01", "2022/12/01" in a process
# for about 20 minutes to retrieve all the data in a csv file.
def get_news(from_date, to_date, language = "en", country = "US") -> float:
    page_num = 1
    url = "https://covid-19-news.p.rapidapi.com/v1/covid"
    querystring = {"from": f"{from_date}",
                   "to": f"{to_date}",
                   "lang": f"{language}",
                   "country": f"{country}",
                   "page": f"{page_num}"}
    headers = {
        "X-RapidAPI-Key": "e2708eb054msha687acae8d1d3c2p188ddfjsnf4d14e880bc2",
        "X-RapidAPI-Host": "covid-19-news.p.rapidapi.com"
    }

    fstres = requests.get(url, headers=headers, params=querystring)
    total_pages = fstres.json()["total_pages"]

    print(f"total {total_pages} pages, retrieving all the data...")
    news = []
    last_retrieved_page = 1
    for i in range(1, total_pages):
        page_num = i
        querystring = {"from": f"{from_date}",
                       "to": f"{to_date}",
                       "lang": f"{language}",
                       "country": f"{country}",
                       "page": f"{page_num}"}
        res = requests.get(url, headers=headers, params=querystring)
        while res.status_code != 200:
            print(f"attempting to retrieve data from page {last_retrieved_page + 1}... waiting for access")
            time.sleep(80)
            res = requests.get(url, headers=headers, params=querystring)
        articles = res.json()["articles"]
        news += [(a["title"], a["summary"], a["published_date"]) for a in articles]
        last_retrieved_page = i
        print(f"retrieved page {i}. Continuing")
    return news




if __name__ == "__main__":
    news_data = get_news(sys.argv[2], sys.argv[3])
    with open(sys.argv[1], 'w') as out:
        fw = csv.writer(out)
        fw.writerow(['title','summary','published_date'])
        for row in news_data:
            fw.writerow(row)