#!/usr/bin/env python3
from datetime import datetime
import covid_tweets as tw
import pandas as pd
from textblob import TextBlob
from matplotlib import pyplot as plt
import seaborn as sns
import covid_stats as st

stats_data = pd.DataFrame(st.get_recent_stats(), columns= st.STAT_COLUMNS)
news_data = pd.read_csv("covid_news_recent.csv")
news_data = news_data.dropna()
tweets_data = pd.read_csv("covid_tweets.csv")
tweets_blobs = tweets_data["text"].apply(lambda x: TextBlob(x))
news_blobs = news_data["summary"].apply(lambda x: TextBlob(x))
tweets_data["cleaned_tweets"] = tweets_data["text"].apply(tw.clean_tweets)
news_data["summary_polarity"] = news_blobs.apply(lambda x: x.polarity)
news_data["summary_subjectivity"] = news_blobs.apply(lambda x: x.subjectivity)
tweets_data["text_polarity"] = tweets_blobs.apply(lambda x: x.polarity)
tweets_data["text_subjectivity"] = tweets_blobs.apply(lambda x: x.subjectivity)
tweets_data["created_date"] = pd.to_datetime(tweets_data["created_at"])

fig1, (ax1_1, ax1_2) = plt.subplots(1, 2, sharey=True)
fig1.suptitle("Polarity and subjectivity of twitter texts under COVID tag")
tweets_data["text_polarity"].plot.hist(ax=ax1_1)
tweets_data["text_subjectivity"].plot.hist(ax=ax1_2)
ax1_1.set_xlabel("polarity")
ax1_2.set_xlabel("subjectivity")

fig2, ax2 = plt.subplots()
fig2.suptitle("Scatter plot of recent twitter text polarity to text subjectivity under COVID tag")
ax2.scatter(tweets_data["text_polarity"], tweets_data["text_subjectivity"])
ax2.set_xlabel("text_polarity")
ax2.set_ylabel("text_subjectivity")

fig3, (ax3_1, ax3_2 )= plt.subplots(2,1,sharex=True)
sns.lineplot(ax=ax3_2, x=stats_data["date"].apply(lambda x: datetime.strptime(x, '%Y-%m-%d')),
             y=stats_data.deaths_diff, linewidth=0.5)
sns.lineplot(ax=ax3_1, x=tweets_data.created_date.dt.date,
             y=tweets_data.text_polarity, linewidth=0.5)
plt.xticks(rotation=45)

plt.show()

