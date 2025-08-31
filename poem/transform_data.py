import csv
import pandas as pd
import os

poezii_dir = "./data_web"
poezii_versuri_dir = "./data_web_versuri"

def main():
    for filename in os.listdir(poezii_dir):
        if filename.endswith('.csv'):
            filepath = os.path.join(poezii_dir, filename)
            df = pd.read_csv(filepath, header=None, names=['Autor', 'Titlu', 'Versuri'])
            df.columns = df.iloc[0]
            df = df[1:]

            versuri = []
            for _, row in df.iterrows():
                titlu = row['Titlu']
                verses = str(row['Versuri']).split('\n')
                for verse in verses:
                    if verse.strip():
                        versuri.append((titlu, verse.strip()))

            new_filename = os.path.join(poezii_versuri_dir, filename.replace('.csv', '_versuri.csv'))
            with open(new_filename, "w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Titlu", "Vers"])
                writer.writerows(versuri)


def main2():
    for filename in os.listdir(poezii_versuri_dir):
        if filename.endswith('_versuri.csv'):
            filepath = os.path.join(poezii_versuri_dir, filename)
            df = pd.read_csv(filepath, header=0, names=['Titlu', 'Vers'])

            print(df["Sentiment"].unique())


if __name__ == "__main__":
    main()
    # main2()