import datetime as dt
import requests

STAT_COLUMNS = ["date", "confirmed_diff", "deaths_diff", "fatality_rate"]

def get_recent_stats() -> float:
    days_to_retrieve = 7
    url = "https://covid-19-statistics.p.rapidapi.com/reports/total"

    headers = {
        "X-RapidAPI-Key": "e2708eb054msha687acae8d1d3c2p188ddfjsnf4d14e880bc2",
        "X-RapidAPI-Host": "covid-19-statistics.p.rapidapi.com"
    }
    stat = []
    for i in range(1, days_to_retrieve+1):
        querystring = {"date": str(dt.date.today() - dt.timedelta(days=i))}
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()["data"]
        stat += [(data[STAT_COLUMNS[0]], data[STAT_COLUMNS[1]], data[STAT_COLUMNS[2]],data[STAT_COLUMNS[3]])]
    return stat

if __name__ == "__main__":
    print(get_recent_stats())