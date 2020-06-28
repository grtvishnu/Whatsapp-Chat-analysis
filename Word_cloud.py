import pandas as pd
import nltk
import matplotlib.pyplot as plt
from wordcloud import WordCloud


df = pd.read_csv("chat_py.csv")

new_df = df[(df.text != '<Media omitted>')]
new_df = new_df.dropna()


raw = []
for word in new_df.text:
    token = nltk.word_tokenize(str(word).lower())
    raw.extend(token)

fdist = nltk.FreqDist(raw)


stopwords = set(['ahhh', 'hmm', 'kk', 'k', 'aa', 'Aa', 'Ehh', 'aahhh', 'enn', 'nee', 'aaà', 'aaa', 'njn', 'ee', 'avide',
                 'eyy', 'avide', 'apo', 'appo', 'ipo', 'okey', 'oru', 'nale', 'ath', 'ind', 'oke', 'onnum', 'aahh', 'pole', 'nthaa', 'illaa',
                 'athe', 'ivide', 'poyi', 'ini', 'nalla', 'alla', 'alle', 'https', 'oo', 'the', 'enik', 'inne', 'ithe', 'inn', 'ippo', 'good', 'onnum', 'and'])


words_for_wordcloud = ' '.join([w[0] for w in fdist.most_common(100)])
wordcloud = WordCloud(width=800, height=800,
                      background_color='white',
                      stopwords=stopwords, min_font_size=12).generate(words_for_wordcloud)
# plot the WordCloud image
plt.figure(figsize=(8, 8), facecolor=None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)
plt.show()
