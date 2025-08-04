# Analiza sentimentelor in versuri

## Introducere
Aplicatia permite utilizatorilor sa caute melodii dupa titlu, artist sau gen, si sa analizeze emotia transmisa prin versuri.
Proiectul are la baza doua componente principale:
- Modelul de sentiment analysis
- Un api pentru versuri

### Model sentiment analysis
Pentru inceput, am antrenat un model utilizand un dataset cu comentarii de pe twitter si emotia transmisa (foarte _ghetto_, stiu).
Emotiile incluse in dataset sunt urmatoarele: sadness😔, joy😃, love 💌, anger 😡, fear 😨, surprise 😲. Sunt putine, dar pentru o rampa de lansare sunt ok.

[Link catre dataset](https://www.kaggle.com/code/shtrausslearning/twitter-emotion-classification/input)

Folosind regresia logistica, cu ajutorul bibliotecii sk-learn, am ajuns la o acuratete de 85%.
Am impartit setul de date in:
- 75% pentru antrenarea modelului
- 25% pentru testarea

#### Matricea de confuzie
Pe diagonala principala sunt emotiile prezise corect, conform setului de testare.
|            | Sadness | Joy   | Love  | Anger | Fear  | Surprise |
|------------|---------|------|------|------|------|----------|
| **Sadness**  | ✅ 27361 | 1728 | 123 | 725  | 413  | 63  |
| **Joy**      |  828   | ✅ 32673 | 1196 | 224  | 207  | 197  |
| **Love**     |  224   | 2039 | ✅ 6149 | 92  | 20  | 19  |
| **Anger**    | 1092   | 1436 | 82  | ✅ 11266 | 442  | 31  |
| **Fear**     |  816   | 1023 | 45  | 352  | ✅ 9189 | 454  |
| **Surprise** |  121   | 425  | 18  | 29   | 590  | ✅ 2511  |

Dupa cum se poate observa setul de date nu este unul echilibrat, deci urmeaza sa concatenez mai multe date pentru a ajunge la o solutie mai balansata.

---

#### Scenarii de rulare


Pentru propozitii/ fraze simple algoritmul functioneaza bine.
``` bash
Enter phrase:   you make me angry
Predicted emotion:  anger
Enter phrase:   i am afraid of you
Predicted emotion:  fear
```
Dar pentru propozitii/ fraze mai complicate, cu figuri de stil (de exemplu), algoritmul nu se descurca asa de bine. Luam versurile melodiilor _Nelly Furtado - Say it right_ si _Instant Crush - Daft Punk_.
Ambele fiind piese cu sentimente profunde de dezamagire, ar trebui sa primim ca output *sadness*, *anger*, sau chiar *surprise* 
``` bash
Enter phrase:   Oh, you dont mean nothing at all to me (hey, oh-oh, hey)
Predicted emotion:  joy
Enter phrase:   I listened to your problems, now listen to mine I didnt want to anymore, oh
Predicted emotion:  joy
```
Modelul nu e chiar asa de praf, intrucat pentru alte versuri ale piesei, detecteaza emotia corecta.
```
Enter phrase:   Kinda counted on you being a friend Can I give it up or give it away?
Predicted emotion:  sadness


## Web scraping