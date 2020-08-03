# 01_create_your_own_datase.py
# reference implementation
# author: zoltan.varju@gmail.com
# last modified on 2020-08-03

import ndjson
import numpy as np
from imblearn.under_sampling import RandomUnderSampler

###############################################################################
#####                                Corpus                               #####
###############################################################################
#### keys
## all
#'overall', 'verified', 'reviewTime', 'reviewerID', 'asin', 'reviewerName',
# 'reviewText', 'summary', 'unixReviewTime'
## optional
# vote
ratings = []
reviews = []
summaries = []
with open("data/raw/Video_Games_5.json", "r") as infile:
    reader = ndjson.reader(infile)

    for review in reader:
        try:
            rating = review["overall"]
            rv = review["reviewText"]
            s = review["summary"]
        except Exception as e:
            continue
        if len(rv) > 0 and len(s) > 0:
            ratings.append(rating)
            reviews.append(rv)
            summaries.append(s)

###############################################################################
#####                     The distribution of stars                       #####
###############################################################################
from collections import Counter
import altair as alt
import pandas as pd

# let's see the distributions

# the distribution of review ratings
rating_counts = Counter(ratings)
data1 = pd.DataFrame(
    {
        "ratings": [str(e) for e in list(rating_counts.keys())],
        "counts": list(rating_counts.values()),
    }
)

chart1 = alt.Chart(data1).mark_bar().encode(x="ratings", y="counts")
chart1.save("plots/00/rating_counts.html")

###############################################################################
####                             Sampling                                 #####
###############################################################################
indices = list(range(len(reviews)))

# using the same seed (random_stat=42) you can get the same samples!
rus = RandomUnderSampler(
    sampling_strategy={1.0: 1500, 2.0: 500, 3.0: 500, 4.0: 500, 5.0: 1500},
    random_state=42,
)
indices_sample, ratings_sample = rus.fit_resample(
    np.array(indices).reshape(-1, 1), np.array(ratings).reshape(-1, 1)
)

indices_sample = np.ndarray.flatten(indices_sample)
indices_other = [i for i in list(range(len(reviews))) if i not in indices_sample]
reviews_sample = [reviews[i] + " " + summaries[i] for i in indices_sample]
reviews_other = [reviews[i] for i in indices_other]

np.random.seed(42)
big_sample = np.random.randint(len(reviews_other), size=(100000,))
reviews_to_be_saved = [reviews_other[i].replace("\n", " ") for i in big_sample]
reviews_to_be_saved = "\n".join(reviews_to_be_saved)

df = pd.DataFrame({"rating": ratings_sample, "review": reviews_sample})

with open("data/raw/review_corpus.tsv", "w") as outfile:
    outfile.write(df.to_csv(index=False, sep="\t"))

with open("data/raw/reviews_without_ratings.txt", "w") as outfile:
    outfile.write(reviews_to_be_saved)
