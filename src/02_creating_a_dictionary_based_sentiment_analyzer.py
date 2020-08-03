# 02_creating_a_dictionary_based_sentiment_analyzer.py
# reference implementation
# author: zoltan.varju@gmail.com
# last modified on 2020-08-03

import pandas as pd

df = pd.read_csv("data/raw/review_corpus.tsv", sep="\t")

ratings = list(df["rating"])
reviews = list(df["review"])

###############################################################################
#####                   Dictionary based sentiment analysis               #####
###############################################################################
from nltk.corpus import opinion_lexicon
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize

positive_wds = set(opinion_lexicon.positive())
negative_wds = set(opinion_lexicon.negative())
# lists are NOT lemmatized so we only have to tokenize the text and count
# positive and negative words


def score_sent(sent):
    """Returns a score btw -1 and 1"""
    sent = [e.lower() for e in sent if e.isalnum()]
    total = len(sent)
    pos = len([e for e in sent if e in positive_wds])
    neg = len([e for e in sent if e in negative_wds])
    if total > 0:
        return (pos - neg) / total
    else:
        return 0


def score_review(review):
    sentiment_scores = []
    sents = sent_tokenize(review)
    for sent in sents:
        wds = word_tokenize(sent)
        sent_scores = score_sent(wds)
        sentiment_scores.append(sent_scores)
    return sum(sentiment_scores) / len(sentiment_scores)


review_sentiments = [score_review(e) for e in reviews]

df = pd.DataFrame(
    {
        "rating": ratings,
        "review": reviews,
        "review dictionary based sentiment": review_sentiments,
    }
)

with open("data/processed/dictionary_based_sentiment.tsv", "w") as outfile:
    outfile.write(df.to_csv(index=False, sep="\t"))
###############################################################################
#####                       Exploratory Data Analysis                     #####
###############################################################################
# plot score vs dict_sents
from collections import Counter

import altair as alt
import numpy as np
import pandas as pd

# let's see the distributions

# the distribution of review scores
rating_counts = Counter(ratings)
data1 = pd.DataFrame(
    {
        "ratings": [str(e) for e in list(rating_counts.keys())],
        "counts": list(rating_counts.values()),
    }
)

chart1 = alt.Chart(data1).mark_bar().encode(x="ratings", y="counts")
chart1.save("plots/01/rating_counts.html")
# we have a majority class !

# the distribution of sentiment scores
hist, bin_edges = np.histogram(review_sentiments, density=True)
labels = list(zip(bin_edges, bin_edges[1:]))
labels = [(str(e[0]), str(e[1])) for e in labels]
labels = [" ".join(e) for e in labels]


data2 = pd.DataFrame({"sentiment scores": labels, "counts": hist})

chart2 = (
    alt.Chart(data2)
    .mark_bar()
    .encode(x=alt.X("sentiment scores", sort=labels), y="counts")
)
chart2.save("plots/01/review_sentiments.html")
# (0.0, 0.20000000000000018) -> neutral is the majority


# is there any relationship btw review scores and sentiments?
source = pd.DataFrame(
    {"ratings": [str(e) for e in ratings], "sentiments": review_sentiments}
)


chart4 = (
    alt.Chart(source)
    .mark_circle(size=60)
    .encode(
        x="ratings", y="sentiments", color="ratings", tooltip=["ratings", "sentiments"]
    )
    .interactive()
)
chart4.save("plots/01/reviews_ratings_vs_sentiment.html")


###############################################################################
#####                             Correlation                             #####
###############################################################################
# test correlation
from scipy.stats import pearsonr, spearmanr

corr1, _ = pearsonr(ratings, review_sentiments)
print(corr1)
# 0.5484025893803234

# Spearman rank correlation says there's weak correlation btw review score
# and sentiment
scor1, _ = spearmanr(ratings, review_sentiments)

print(scor1)
# 0.6248595756447616

###############################################################################
######                          Let's see the data                       ######
###############################################################################
# for i in range(len(reviews)):
#     sc = ratings[i]
#     rs = review_sentiments[i]
#     # ss = summary_sentiments[i]
#     t = reviews[i]
#     if sc == 5 and rs < -0.2:
#         print(t)
#     if sc == 1 and rs > 0.3:
#         print(t)

### Problem with reviews like
# no issues
# no complains
# Doesn't work.
# Didn't like it.


from nltk.sentiment.util import mark_negation


t = "I received these on time and no problems. No damages battlfield never fails"
print(mark_negation(t.split()))


###############################################################################
####                       Let's handle negation                          #####
###############################################################################
positive_wds = set(opinion_lexicon.positive())
negative_wds = set(opinion_lexicon.negative())

positive_wds_with_negation = positive_wds.union({wd + "_NEG" for wd in negative_wds})
negative_wds_with_negation = negative_wds.union({wd + "_NEG" for wd in positive_wds})


def score_sent(sent):
    """Returns a score btw -1 and 1"""
    sent = [e.lower() for e in sent if e.isalnum()]
    total = len(sent)
    pos = len([e for e in sent if e in positive_wds_with_negation])
    neg = len([e for e in sent if e in negative_wds_with_negation])
    if total > 0:
        return (pos - neg) / total
    else:
        return 0


def score_review(review):
    sentiment_scores = []
    sents = sent_tokenize(review)
    for sent in sents:
        wds = word_tokenize(sent)
        wds = mark_negation(wds)
        sent_scores = score_sent(wds)
        sentiment_scores.append(sent_scores)
    return sum(sentiment_scores) / len(sentiment_scores)


review_sentiments = [score_review(e) for e in reviews]


df = pd.DataFrame(
    {"rating": ratings, "review": reviews, "review sentiment": review_sentiments,}
)

with open("data/processed/rule_based_sentiment.tsv", "w") as outfile:
    outfile.write(df.to_csv(index=False, sep="\t"))

scor1, _ = spearmanr(ratings, review_sentiments)
print(scor1)
# 0.6614342442109357

###############################################################################
#####                 Let's see the distributions                         #####
###############################################################################
# the distribution of sentiment scores
hist, bin_edges = np.histogram(review_sentiments, density=True)
labels = list(zip(bin_edges, bin_edges[1:]))
labels = [(str(e[0]), str(e[1])) for e in labels]
labels = [" ".join(e) for e in labels]


data2 = pd.DataFrame({"sentiment scores": labels, "counts": hist})

chart2 = (
    alt.Chart(data2)
    .mark_bar()
    .encode(x=alt.X("sentiment scores", sort=labels), y="counts")
)
chart2.save("plots/02/review_sentiments.html")
# (0.0, 0.20000000000000018) -> neutral is the majority

# is there any relationship btw review scores and sentiments?
source = pd.DataFrame(
    {"ratings": [str(e) for e in ratings], "sentiments": review_sentiments}
)

chart4 = (
    alt.Chart(source)
    .mark_circle(size=60)
    .encode(
        x="ratings", y="sentiments", color="ratings", tooltip=["ratings", "sentiments"]
    )
    .interactive()
)
chart4.save("plots/02/reviews_raings_vs_sentiment.html")
