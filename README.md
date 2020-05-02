# Growth Hacking with NLP and Sentiment Analysis

## Install the dependencies
Make a virtual environment and install the dependencies:
```shell script
pip install -r requirements.txt
```
Download data needed for the dictionary based sentiment.
Start Python in your virtual environment.
```Python
import nltk
nltk.download("opinion_lexicon")
nltk.download("stopwords")
nltk.download("punkt")
```
Having downloaded the data required by nltk, you can exit
your virtual environment.

## Using Jupyter Notebooks
Make a new environment, install the requirements.
Install notebook.
```shell script
pip install notebook
ipython kernel install --user --name=name-of-your-virtualenv
```
now you can start Jupyter.
```shell script
jupyter notebook
```
Don't forget to set your kernel as the picture shows
below.
![A picture showing how to set your kernel in Jupyter Notebooks](imgs/notebook.png "How to kernel")

Now, you are ready to work through the project! Happy hacking!

## Using Colab
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/crow-intelligence/growth-hacking-sentiment/blob/master/Colab_growth_hacking_example.ipynb)
Click on the badge above to open our notebook in Colab.

Save it to your Google Drive. 
![Save2drive](imgs/save2drive.png "How to save")

First of all, set the runtime to GPU

![Colab01](imgs/colab01.png "How to GPU")
![Colab02](imgs/colab02.png "How to GPU 2")
![Colab03](imgs/colab03.png "How to GPU3")

