import pandas as pd
import re
import joblib
import datetime
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

vectorizer = TfidfVectorizer(max_features=1000)
emotions = ['sadness', 'joy', 'love', 'anger', 'fear', 'surprise']

def read_dataset():
    df = pd.read_csv("./text.csv")
    return df

def clean_data(review):
    if isinstance(review, str):
        no_punc = re.sub(r'[^\w\s]', '', review)
        return ''.join([i for i in no_punc if not i.isdigit()])
    return ''

def save_model(model, vectorizer, accuracy):
    filename = os.path.join('./models/' + str(accuracy).replace('.', '-') + '_logistic_regression_model.pkl')
    joblib.dump((model, vectorizer), filename)


def get_logistic_regression():
    dataset = read_dataset()
    vectorizer = TfidfVectorizer(max_features=1000)

    X_train, X_test, y_train, y_test = train_test_split(dataset['text'], dataset['label'])

    X_train = vectorizer.fit_transform(X_train)
    X_test = vectorizer.transform(X_test)

    logisticRegression = LogisticRegression(solver='liblinear')
    logisticRegression.fit(X_train, y_train)

    predictions = logisticRegression.predict(X_test)
    
    matrix = confusion_matrix(y_test, predictions)
    matrix_df = pd.DataFrame(matrix, index=emotions, columns=emotions)
    print(matrix_df)

    accuracy = accuracy_score(predictions, y_test)
    return logisticRegression, vectorizer, accuracy


def get_bayes_naive():
    dataset = read_dataset()

    X_train, X_test, y_train, y_test = train_test_split(dataset['text'], dataset['label'])
    


def generate_models():
    while True:
        logisticRegression, vectorizer, accuracy = get_logistic_regression()
        print('Accuracy: ', '{:.2f}'.format(accuracy * 100), '%')
        save_model(logisticRegression, vectorizer, accuracy * 100)
        # if accuracy > 0.85:
        #     save_model(logisticRegression, vectorizer, accuracy * 100)
        #     print(datetime.datetime.now())
        break


if __name__ == "__main__":
    generate_models()