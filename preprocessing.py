# Library for tokenize and labeling the data 'Review'
import nltk
import re
import gc
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob

# Library for modeling Random Forest Classifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, confusion_matrix

# library to convert matrix value to csc matrix format
from scipy.sparse import csc_matrix

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("punkt_tab")

file_path = (
    "../data/raw/wotakoi_reviews.csv"  # Variable that contain the raw data 'csv'
)
df = pd.read_csv(file_path)
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


def __data_to_text__(feature):  # function to get text feature from the csv
    texts = df[feature]
    return texts


def __remove_stopwords__(tokens):
    return [word for word in tokens if word.lower() not in stop_words]


def __lemmatize_tokens__(tokens):  # normalizing woken with lemmatization
    return [lemmatizer.lemmatize(token) for token in tokens]


def __tokenize__(text):
    text = re.sub(r"[^a-zA-Z\s]", "", text)  # Remove non-alphabet character
    tokens = word_tokenize(text.lower())  # Tokenization
    tokens = __remove_stopwords__(tokens)  # Reemoving stopwords
    tokens = __lemmatize_tokens__(tokens)  # Lemmatization
    return " ".join(tokens)  # convert back to string


def __labeling_sentiment__(
    text,
):  # label every row based on the polarity score with textblob
    blob = TextBlob(text)
    score = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    if score > 0:
        sentiment = "positive"
    elif score < 0:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    return pd.Series([sentiment, score, subjectivity])


df["clean_text"] = __data_to_text__("Review").apply(__tokenize__)
df[["sentiment", "polarity", "subjectivity"]] = df["clean_text"].apply(
    __labeling_sentiment__
)
print(df)
sentiment_distribution = df["sentiment"].value_counts()
print(sentiment_distribution)

train_data, test_data = train_test_split(df, test_size=0.20, random_state=42)
print("Size of train_data is :", train_data.shape)
print("Size of test_data is :", test_data.shape)

vectorizer = HashingVectorizer()
train_matrix = vectorizer.transform(train_data["clean_text"].values.astype("U"))
test_matrix = vectorizer.transform(test_data["clean_text"].values.astype("U"))
# Convert the matrix to csc matrix format
train_matrix_csc = csc_matrix(train_matrix)
test_matrix_csc = csc_matrix(test_matrix)
gc.collect()  # to make sure the garbage is collected even that was collect by python automatically

# Modeling
# I'm actually didnt know how to chooose model that fit to my data, so i just pick some algo that look mainstream so i can find many documentation and example of it
# In this project i'll use randomforest algo and i'll use one from sklearn library
clf = RandomForestClassifier()  # A variable to save the function
randForest = clf.fit(train_matrix_csc, train_data["sentiment"])

y_pred = randForest.predict(test_matrix_csc)
score = f1_score(test_data["sentiment"], y_pred, average="weighted")
print(f"F1 Score: {score}")

# metrics eval  with confusion matrix from sklearn library
confMatrix = confusion_matrix(test_data["sentiment"], y_pred)
print(confMatrix)

# export the output as feature engineering
# df.to_csv("../data/processed/processed.csv", index=False)
