import regex as re
import pandas as pd
import matplotlib.pyplot as plt
import emoji
import numpy as np
from tabulate import tabulate
import plotly.express as px
from plotly.subplots import make_subplots
from tabulate import tabulate
from datetime import datetime
from collections import Counter
import mplcairo
import matplotlib
from matplotlib.font_manager import FontProperties
from plotly.subplots import make_subplots
import seaborn as sns
from wordcloud import WordCloud

df = pd.read_csv('conversation_Apolline.csv')

df = df.dropna(how='all')
df.drop(['3'], axis=1, inplace=True)
df.rename(columns={"0": "Date", "1": "name", "2": "message"}, inplace=True)
df = df.dropna()  # Drop empty values

df['date'] = pd.to_datetime(df['Date'], format='%d-%m-%y %H:%M:%S')
df['hour'] = df['date'].dt.hour
df['weekday'] = df['date'].dt.weekday
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
# print(tabulate(df[50:100], headers='keys', tablefmt='psql'))
df = df.set_index(pd.DatetimeIndex(df['Date']))

# -------------------------- Heat map ------------------------------
df1 = df.groupby(["month", "year"]).count().reset_index()
hm = df1.pivot("month", "year", "message")
ax = sns.heatmap(hm, cmap=sns.cm.rocket_r)
plt.show()

#  ----------------------- Word Frequency --------------------------

df['characters_nb'] = df.message.apply(len)
df['words_nb'] = df.message.apply(lambda x: len(x.split()))

# print(df.groupby('name').mean().sort_values('characters_nb').round(2))
# print(df.head())
# print(df.message.value_counts().head(20)) #most common messages

words = ''
for i in df.message.values:
    words += '{} '.format(i.lower())  # make all words lowercase

wd = pd.DataFrame(Counter(words.split()).most_common(200),
                  columns=['word', 'frequency'])
wd = wd.iloc[101:]

data = dict(zip(wd['word'].tolist(), wd['frequency'].tolist()))

del(data["mes"])
del(data["ta"])
del(data["se"])
del(data["j’ai"])
del(data["comme"])
del(data["coup"])
del(data["être"])
del(data["sont"])


wc = WordCloud(stopwords=["de", "ta", "️j’ai", "j'ai", "peu", "il", "plus", "en", "pas", "du", "un", "ai", "est",
                          "je", "le", "et", "la", "audio ", "j'ai"], width=800, height=400, max_words=200).generate_from_frequencies(data)
plt.figure(figsize=(10, 10))
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
# plt.show()

# ------------ Plot message frequency over days -------------------

day_freq = df.resample('M').count()
day_freq.drop(day_freq.columns[0], axis=1, inplace=True)
day_freq = day_freq.reset_index()

# Plot number 1 --------- Over whole period ----------------
# fig = px.line(day_freq, x="Date", y="message")
# fig.show()

# Plot number 2 ------------ Hour and weekday ----------------

subfig = make_subplots(rows=1, cols=2,
                       specs=[[{"type": "xy"}, {"type": "xy"}]])

df1 = df.groupby(["hour"]).count().reset_index()
y1 = pd.Series(df1['weekday'])

fig = subfig.add_bar(row=1, col=1, y=y1, x=["1am", "2am", "3am", "4am", "5am", "6am", "7am", "8am", "9am",
                                            "10am", "11am", "12am", "1pm", "2pm", "3pm", "4pm", "5pm", "6pm",
                                            "7pm", "8pm", "9pm", "10pm", "11pm", "12pm"])
df2 = df.groupby(["weekday"]).count().reset_index()
y2 = pd.Series(df2['hour'])
fig = subfig.add_bar(row=1, col=2, y=y2, x=[
                     "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
# fig.show()

df3 = df.groupby(["hour"]).count().reset_index()
pl1 = pd.DataFrame(dict(
    r=df3['message'],
    theta=["1am", "2am", "3am", "4am", "5am", "6am", "7am", "8am", "9am",
           "10am", "11am", "12am", "1pm", "2pm", "3pm", "4pm", "5pm", "6pm",
           "7pm", "8pm", "9pm", "10pm", "11pm", "12pm"]))
fig = px.line_polar(pl1, r='r', theta='theta', line_close=True,
                    color_discrete_sequence=px.colors.sequential.Plotly3)
fig.update_traces(fill='toself')
# fig.show()

df4 = df.groupby(["weekday"]).count().reset_index()
pl2 = pd.DataFrame(dict(
    r=df4["message"],
    theta=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]))
fig = px.line_polar(pl2, r='r', theta='theta', line_close=True,
                    color_discrete_sequence=px.colors.diverging.Spectral)
fig.update_traces(fill='toself')
# fig.show()

# -------------------- Who sends more messages ------------------
df2 = df.groupby(["name"]).count().reset_index()

fig = px.bar(df2,
             y=df.groupby(["name"]).size(),
             x=["Me", "Her"],
             color='name')
# fig.show()
# ------------------------------- Emojis ---------------------------
Alex = df[df['name'] == " Alex "]
Apolline = df[df['name'] == " Apolline "]


emojis_Alex = []
for string in Alex['message']:
    my_str = str(string)
    for each in my_str:
        if each in emoji.UNICODE_EMOJI:
            emojis_Alex.append(each)

emojis_Apolline = []
for string in Apolline['message']:
    my_str = str(string)
    for each in my_str:
        if each in emoji.UNICODE_EMOJI:
            emojis_Apolline.append(each)

# This is a dictionary
freq_Alex = dict(Counter(i for sub in emojis_Alex for i in set(sub)))
sort_orders1 = sorted(freq_Alex.items(), key=lambda x: x[1], reverse=True)

# This is a dictionary
freq_Apolline = dict(Counter(i for sub in emojis_Apolline for i in set(sub)))
sort_orders2 = sorted(freq_Apolline.items(), key=lambda x: x[1], reverse=True)

res_alex = sort_orders1[0:11]
res_apo = sort_orders2[0:10]
# print(res_alex)
# print(res_apo)
labels, ys = zip(*res_alex)
xs = np.arange(len(labels))
p1 = plt.bar(xs, ys, 0.8, color="lightblue")
# plt.show()
