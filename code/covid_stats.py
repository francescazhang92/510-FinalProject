import datetime as dt
import requests

STAT_COLUMNS = ["date", "confirmed_diff", "deaths_diff", "fatality_rate"]
STAT_COLUMNS1 = ["case_total", "death_total", "time"]
def get_recent_stats():
    days_to_retrieve = 7
    url = "https://covid-19-statistics.p.rapidapi.com/reports/total"

    headers = {
        "X-RapidAPI-Key": "e2708eb054msha687acae8d1d3c2p188ddfjsnf4d14e880bc2",
        "X-RapidAPI-Host": "covid-19-statistics.p.rapidapi.com"
    }
    stat = []
    for i in range(0, days_to_retrieve+1):
        querystring = {"date": str(dt.date(2022, 12, 10) - dt.timedelta(days=i))}
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()["data"]
        stat += [(data[STAT_COLUMNS[0]], data[STAT_COLUMNS[1]], data[STAT_COLUMNS[2]],data[STAT_COLUMNS[3]])]
    return stat

def get_recent_stats1():
    days_to_retrieve = 7
    url = "https://covid-193.p.rapidapi.com/history"


    headers = {
        "X-RapidAPI-Key": "e2708eb054msha687acae8d1d3c2p188ddfjsnf4d14e880bc2",
        "X-RapidAPI-Host": "covid-193.p.rapidapi.com"
    }
    stat = []
    for i in range(0, days_to_retrieve+1):
        querystring = {"country":"usa", "day": str(dt.date(2022, 12, 10) - dt.timedelta(days=i))}
        response = requests.get(url, headers=headers, params=querystring)

        data = response.json()["response"]
        stat += [(timepoint["cases"]["total"], timepoint["deaths"]["total"], timepoint["time"]) for timepoint in data]
    return stat

if __name__ == "__main__":
    print(get_recent_stats1())