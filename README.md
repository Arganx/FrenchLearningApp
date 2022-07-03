# The French Conjugaison App
## About the app
The app was created as a tool to practice the conjugation of verbs in French. It allows to practice conjugation skills on random verbs or chose a specific verb and practice on it.
Currently supported times:
* le présent
* le passé composé 
* l’imparfait
* le passé simple
* le plus-que-parfait
* le passé antérieur
* le futur proche
* le futur simple
* futur antérieur
## How to run
Requirements: Python3
The app runs on: Windows, Linux, and Mac
1. Clone the repository
2. (optional) Create a virtual environment for the app and activate it
```bash
python3 -m venv ./env
source env/bin/activate
```
3. Install the required packages
```bash
pip install -r requirements.txt
```
4. Run the app
```bash
python3 learningApp.py
```
## How to use
![alt text](https://github.com/Arganx/FrenchLearningApp/blob/master/ImagesForReadMe/Pasted%20image%2020220703172335.png?raw=true)
1. On the top right 2 buttons allow to either choose a new random word or select a specific word.
    ![alt text](https://github.com/Arganx/FrenchLearningApp/blob/master/ImagesForReadMe/Pasted%20image%2020220703172728.png?raw=true)
2. The selected word shows in the top left corner with translation into 2 languages
    ![alt text](https://github.com/Arganx/FrenchLearningApp/blob/master/ImagesForReadMe/Pasted%20image%2020220703172749.png?raw=true)
3. Below it's possible to choose which time the user wants to practice with the verb
    ![alt text](https://github.com/Arganx/FrenchLearningApp/blob/master/ImagesForReadMe/Pasted%20image%2020220703172809.png?raw=true)
4.  In the practice window the user enters his answers
    ![alt text](https://github.com/Arganx/FrenchLearningApp/blob/master/ImagesForReadMe/Pasted%20image%2020220703172948.png?raw=true)
   5. After clicking on "Vérifiez" the correct answers show up. Next to the user's answer, a square appears indicating if the answer was correct.
    ![alt text](https://github.com/Arganx/FrenchLearningApp/blob/master/ImagesForReadMe/Pasted%20image%2020220703173211.png?raw=true)
## Add translation to your language
By default, the app provides the translation of the French verb into English and Polish. It is possible to change the translation from Polish into another language. To do that go into the file and change the line:
```
verb_pl = str(blob.translate(from_lang='fr',to='pl'))
```
The list of available languages:

![alt text](https://github.com/Arganx/FrenchLearningApp/blob/master/ImagesForReadMe/Pasted%20image%2020220703171123.png?raw=true)
