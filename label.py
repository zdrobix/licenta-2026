import re
import pandas as pd
from run_model import load_model
from train_model import clean_data


def clean_verse(verse):
    verse = verse.lower()
    verse = re.sub(r'\s+', ' ', verse)  
    verse = verse.strip()
    return verse

def run(): 
    df = pd.read_csv('./melodii_versuri_genius_unic.csv')
    model, vect = load_model('./models/0-50_ann_emotion_ro_model.pkl')

    with open('./melodii_versuri_genius_unic_etichetat.csv', 'a', encoding='utf-8') as f:
        for vers in df['Line']:
            new_data = pd.DataFrame({'text': [vers]})
            new_data['text'] = new_data['text'].apply(clean_data)

            X_new = vect.transform(new_data['text'])
            prediction = model.predict(X_new)
            f.write(f'"{vers}","{prediction[0]}"\n')



if __name__ == "__main__":
    run()