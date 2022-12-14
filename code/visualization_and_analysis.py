#!/usr/bin/env python3

import statsmodels.api as sm
from code import covid_tweets as tw
import pandas as pd
from textblob import TextBlob
from matplotlib import pyplot as plt
import seaborn as sns
import covid_stats as st


news_data = pd.read_csv("../data/covid_news_recent.csv")
news_data = news_data.dropna()
tweets_data = pd.read_csv("../data/covid_tweets.csv")
tweets_blobs = tweets_data["text"].apply(lambda x: TextBlob(x))
news_blobs = news_data["summary"].apply(lambda x: TextBlob(x))
tweets_data["cleaned_tweets"] = tweets_data["text"].apply(tw.clean_tweets)

tweets_data["text_polarity"] = tweets_blobs.apply(lambda x: x.polarity)
tweets_data["text_subjectivity"] = tweets_blobs.apply(lambda x: x.subjectivity)
tweets_data["created_date"] = pd.to_datetime(tweets_data["created_at"])

news_data["summary_polarity"] = news_blobs.apply(lambda x: x.polarity)
news_data["summary_subjectivity"] = news_blobs.apply(lambda x: x.subjectivity)


stats_data = pd.DataFrame(st.get_recent_stats(), columns=st.STAT_COLUMNS)
stats_data["date"] = pd.to_datetime(stats_data.date)
#tweets_data_binned = tweets_data
fig1, (ax1_1, ax1_2) = plt.subplots(1, 2, sharey=True)
fig1.suptitle("Polarity and subjectivity of twitter texts under COVID tag")
tweets_data["text_polarity"].plot.hist(ax=ax1_1)
tweets_data["text_subjectivity"].plot.hist(ax=ax1_2)
ax1_1.set_xlabel("polarity")
ax1_2.set_xlabel("subjectivity")

fig4, (ax4_1, ax4_2) = plt.subplots(1, 2, sharey=True)
fig4.suptitle("Polarity and subjectivity of news summary regarding COVID")
news_data["summary_polarity"].plot.hist(ax=ax4_1)
news_data["summary_subjectivity"].plot.hist(ax=ax4_2)
ax4_1.set_xlabel("polarity")
ax4_2.set_xlabel("subjectivity")

fig2, ax2 = plt.subplots()
fig2.suptitle("Scatter plot of recent twitter text polarity to text subjectivity under COVID tag")
ax2.scatter(tweets_data["text_polarity"], tweets_data["text_subjectivity"])
ax2.set_xlabel("text_polarity")
ax2.set_ylabel("text_subjectivity")

fig3, (ax3_1, ax3_2, ax3_3, ax3_4 )= plt.subplots(4,1,sharex=True)
sns.lineplot(ax=ax3_2, x=stats_data["date"],
             y=stats_data.deaths_diff, linewidth=0.5)
sns.lineplot(ax=ax3_1, x=tweets_data.created_date.dt.date,
             y=tweets_data.text_polarity, linewidth=0.5)
sns.lineplot(ax=ax3_4, x=stats_data["date"],
             y=stats_data.confirmed_diff, linewidth=0.5)
sns.lineplot(ax=ax3_3, x=tweets_data.created_date.dt.date,
             y=tweets_data.text_subjectivity, linewidth=0.5)
plt.xticks(rotation=45)

stats_by_day = stats_data.groupby(stats_data['date'].dt.date).mean()
tweets_by_day = tweets_data.groupby(tweets_data['created_date'].dt.date).mean()
fig4 = plt.figure(figsize = (8, 6))
sns.regplot(x = stats_by_day.deaths_diff,
            y =tweets_by_day.text_polarity)
plt.title('Death diff vs. tweet polarity ', weight='bold', fontsize = 15)

print("-- Cross validation results --")
print("deaths by polarity: ")
print(sm.tsa.stattools.ccf(stats_by_day["deaths_diff"], tweets_by_day["text_polarity"], adjusted=False))
print("deaths by subjectivity: ")
print(sm.tsa.stattools.ccf(stats_by_day["deaths_diff"], tweets_by_day["text_subjectivity"], adjusted=False))
print("confirmed by polarity: ")
print(sm.tsa.stattools.ccf(stats_by_day["confirmed_diff"], tweets_by_day["text_polarity"], adjusted=False))
print("confirmed by subjectivity: ")
print(sm.tsa.stattools.ccf(stats_by_day["confirmed_diff"], tweets_by_day["text_subjectivity"], adjusted=False))
plt.show()

