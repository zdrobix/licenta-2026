import pandas as pd
import joblib
from train_model import clean_data

emotions = ['sadness', 'joy', 'love', 'anger', 'fear', 'surprise']

def load_model(filename):
    model, vectorizer = joblib.load(filename)
    # print(f'Model loaded from {filename}')
    return model, vectorizer

def run_model(model, vectorizer):
    while True:
        phrase = input(f'Enter phrase (/stop):   ')
        if phrase.lower() == 'stop':
            break
        new_data = pd.DataFrame({'text': [phrase]})
        new_data['text'] = new_data['text'].apply(clean_data)

        X_new = vectorizer.transform(new_data['text'])

        predictions = model.predict(X_new)

        print("Predicted emotion: ", emotions[predictions[0]])

def run_model_verse(text):
    model, vectorizer = load_model('./models/85-62_logistic_regression_model.pkl')
    new_data = pd.DataFrame({'text': [clean_data(line.strip()) for line in text]})

    X_new = vectorizer.transform(new_data['text'])
    predictions = model.predict(X_new)

    prediction_counts = pd.Series(predictions).value_counts()

    for val, percent in (prediction_counts / prediction_counts.sum() * 100).items():
        print(f"{emotions[val]:<10}: ", '{:.2f}%'.format(percent))




# if __name__ == "__main__":
#    run_model_verse("for example im happy")