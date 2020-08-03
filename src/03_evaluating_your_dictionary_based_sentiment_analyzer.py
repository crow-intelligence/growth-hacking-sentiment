# 03_evaluating_your_dictionary_based_sentiment_analyzer.py
# reference implementation
# author: zoltan.varju@gmail.com
# last modified on 2020-08-03

import pandas as pd

###############################################################################
#####                              Corpus                                 #####
###############################################################################
df = pd.read_csv("data/processed/sentiment_with_lemmas.tsv", sep="\t")

ratings = list(df["rating"])
reviews = list(df["review"])
reviews = [str(e) for e in reviews]
sentiment = list(df["sentiment"])

###############################################################################
#####               Sentiment values instead of scores                    #####
###############################################################################


def get_rating_class(rating):
    if rating > 4:
        return 2
    elif 2 <= rating <= 4:
        return 1
    else:
        return 0


def get_sentiment_value(sentiment):
    if sentiment > 0.2:
        return 2
    elif -0.2 <= sentiment <= 0.2:
        return 1
    else:
        return 0


def check_status(e):
    if e[0] == e[1]:
        return "OK"
    else:
        return "CHECK"


rating_classes = [get_rating_class(e) for e in ratings]
sentiment_values = [get_sentiment_value(e) for e in sentiment]

###############################################################################
#####                       Evaluation                                    #####
###############################################################################
# evaluation
from sklearn.metrics import accuracy_score

acc = accuracy_score(rating_classes, sentiment_values)
print(acc)
# 0.4315555555555556

from sklearn.metrics import classification_report

target_names = ["negative", "neutral", "positive"]
print(
    classification_report(rating_classes, sentiment_values, target_names=target_names)
)

#                 precision    recall  f1-score   support
#     negative       0.80      0.08      0.14      1500
#      neutral       0.36      0.93      0.52      1500
#     positive       0.82      0.29      0.43      1500
#     accuracy                           0.43      4500
#    macro avg       0.66      0.43      0.36      4500
# weighted avg       0.66      0.43      0.36      4500

import altair as alt
import numpy as np
from sklearn.metrics import confusion_matrix

x, y = np.meshgrid(range(0, 3), range(0, 3))
cm = confusion_matrix(rating_classes, sentiment_values, labels=[0, 1, 2])

source = pd.DataFrame({"true": x.ravel(), "predicted": y.ravel(), "number": cm.ravel()})

chart = (
    alt.Chart(source)
    .mark_rect()
    .encode(x="true:O", y="predicted:O", color="number:Q", tooltip=["number"])
    .interactive()
    .properties(width=800, height=500)
)
chart.save("plots/05/confusion_matrix.html")
