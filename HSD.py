from nltk.util import pr
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

data = pd.read_csv("HSD_dataset.csv")
#print(data.head())

data["labels"] = data["class"].map({0: "Hate Speech", 1: "Offensive Language", 2: "No Hate and Offensive"})
#print(data.head())

data = data[["tweet", "labels"]]
#print(data.head())

import re
import nltk
stemmer = nltk.SnowballStemmer("english")
from nltk.corpus import stopwords
import string
stopword=set(stopwords.words('english'))

def clean(text):
    text = str(text).lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = [word for word in text.split(' ') if word not in stopword]
    text=" ".join(text)
    text = [stemmer.stem(word) for word in text.split(' ')]
    text=" ".join(text)
    return text
data["tweet"] = data["tweet"].apply(clean)
#print(data.head())

x = np.array(data["tweet"])
y = np.array(data["labels"])

cv = CountVectorizer()
X = cv.fit_transform(x) # Fit the Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.43, random_state=29)

clf = DecisionTreeClassifier()
clf.fit(X_train,y_train)
Accuracy = clf.score(X_test,y_test)
print("Accuracy :",Accuracy)


from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt



def hate_speech_detection():
    import streamlit as st
    st.title("Hate Speech Detection")
    user = st.text_input("Enter any Tweet: ","...")
    if(st.button('submit')):
        if len(user) < 1:
            st.write("  ")
        else:
            sample = user
            data = cv.transform([sample]).toarray()
            a = clf.predict(data)
            if(a=='No Hate and Offensive'):
                st.success(a)
            elif(a=='Offensive Language'):
                st.error(a)
            else:
                st.warning(a)
hate_speech_detection()