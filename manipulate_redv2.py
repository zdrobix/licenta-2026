import ast
import pandas as pd

from sklearn import neural_network
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

from transformers import AutoTokenizer

import joblib
import re
import os

from train_model import clean_data
from run_model import load_model

emotions = ['Sadness', 'Surprise', 'Fear', 'Anger', 'Neutral', 'Trust', 'Joy']

def save_model(model, vectorizer, accuracy):
    filename = os.path.join('./models/' + str(accuracy).replace('.', '-') + '_ann_emotion_ro_model.pkl')
    joblib.dump((model, vectorizer), filename)



def train_ann():
    df = pd.read_csv('./red v2 data/testtrain.csv')
    vectorizer = TfidfVectorizer(max_features=10000, tokenizer=AutoTokenizer.from_pretrained("dumitrescustefan/bert-base-romanian-cased-v1").tokenize)

    df['procentual_labels'] = df['procentual_labels'].apply(ast.literal_eval)
    df['label'] = df['procentual_labels'].apply(lambda x: emotions[x.index(max(x))])

    x_train, x_test, y_train, y_test = train_test_split(df['text'], df['label'], test_size=0.2)

    x_train = vectorizer.fit_transform(x_train)
    x_test = vectorizer.transform(x_test)

    ann = make_pipeline(
        StandardScaler(),
        neural_network.MLPClassifier(
            hidden_layer_sizes=(512, 256, 128), 
            max_iter=25, 
            activation='relu', 
            random_state=1, 
            learning_rate='adaptive', 
            learning_rate_init=0.001,
        )
    ) 
    for i in range(ann.named_steps['mlpclassifier'].max_iter):
        ann.named_steps['mlpclassifier'].partial_fit(x_train, y_train, classes=df['label'].unique())
        print(f"Epoch {i+1}, Loss: {ann.named_steps['mlpclassifier'].loss_}")
    score = ann.named_steps['mlpclassifier'].score(x_test, y_test)  
    print(f"Test accuracy: {score}")
    print(confusion_matrix(y_test, ann.named_steps['mlpclassifier'].predict(x_test)))
    print(classification_report(y_test, ann.named_steps['mlpclassifier'].predict(x_test)))
    save_model(ann.named_steps['mlpclassifier'], vectorizer, f"{score:.2f}")


if __name__ == "__main__":
    train_ann()

    # model, vect = load_model('./models/0-50_ann_emotion_ro_model.pkl')
    # while True:
    #     phrase = input(f'Enter phrase (/stop):   ')
    #     if phrase.lower() == 'stop':
    #         break
    #     new_data = pd.DataFrame({'text': [phrase]})
    #     new_data['text'] = new_data['text'].apply(clean_data)

    #     X_new = vect.transform(new_data['text'])

    #     predictions = model.predict(X_new)

    #     print("Predicted emotion: ", predictions[0])
    



"""
0 -> hidden layer 30 30 30 
0.37 -> 90 90 90 
0.50 -> 90 90 90 + label instead of procentual
 -> 
"""