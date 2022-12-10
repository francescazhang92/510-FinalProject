 # 510-FinalProject
 
## How to run this project:
Download all the files in a folder. Recommended to download the csv files as well, because they, especially covid_news_recent, requires a lot of time to retrieve from the api. 

Dependencies are listed in the requirements.txt. To use it, type pip install -r requirements.txt in the command line in the same directory.

Before running the visualization code, make sure covid_news_recent.csv and covid_tweets.csv are in the same directory. Then, simply run "python3 ./visualization.py" to generate the visualizations. 
### visualization.py 
routine that can generate the visualization to the data
### covidnews.py 
covid_news.py is a script that can retrieve news related to COVID given a time period into csv file as commandline argument (yyyy/mm/dd). Due to the limit in access rate, this script requires about 30 minutes to retrieve 10000 sample. Because of this, a sample file contains 10000 line of news is given as covid_news.csv 
### covid_tweets.py
it is a script that can collect the tweets from the recent week into csv file, given an argument on the maximum number of tweets.
### covid_stats.py
a module that collects the statistics of COVID in the recent week