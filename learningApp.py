from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty
from kivy.uix.tabbedpanel import TabbedPanelItem, TabbedPanel
import obtenirVerb
import codecs
import unidecode
import random
from threading import Thread
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.clock import mainthread
from textblob import TextBlob
from textblob.exceptions import NotTranslated

global data
global verbs
global verb_eng
global verb_pl

def assignTranslation(blob):
    global verb_eng
    global verb_pl
    try:
        verb_eng = str(blob.translate(from_lang='fr',to='en'))
    except NotTranslated:
        verb_eng = "-"
    try:
        verb_pl = str(blob.translate(from_lang='fr',to='pl'))
    except NotTranslated:
        verb_pl = "-"

class WindowManager(ScreenManager):
    pass

class StartScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        global verbs
        with codecs.open("french verbs.txt", encoding='utf-8') as f:
            verbs = f.readlines()
        verbs = [unidecode.unidecode(verb.replace("\n","").replace("\r","").replace("\'","_").replace(" ","_")) for verb in verbs]
    def searchAVerb(self):
        global data
        global verb_eng
        global verb_pl
        verb = self.ids.verbInput.text
        blob = TextBlob(verb)
        verb = verb.replace(" ","_")
        data = obtenirVerb.obtenirVerb(verb)
        assignTranslation(blob)
        self.manager.transition.direction = "up"
        self.manager.current = "IndicativePresent"
    def searchRandomVerb(self):
        global data
        global verbs
        global verb_eng
        global verb_pl
        verb = random.choice(verbs)
        data = obtenirVerb.obtenirVerb(verb)
        blob = TextBlob(data.verb)
        assignTranslation(blob)
        self.manager.transition.direction = "up"
        self.manager.current = "IndicativePresent"

class MyTabbedPanelItem(TabbedPanelItem):
    def checkInput(self):
        inputCounter = len(self.content.children[1].children[0].children)-1
        correct = False
        for widget in self.content.children[1].children[1].children[::-1]:
            if(isinstance(widget,TextInput)):
                correctLabel = self.content.children[1].children[0].children[inputCounter]
                correctLabel.opacity = 1
                correctLabel.disabled = False 
                correctText = correctLabel.text
                if(len(correctText.split(" ",1)) > 1 and ("'" not in correctText.split(" ")[0])):
                    correctText = correctText.split(" ",1)[1]
                if(len(correctText.split("'",1)) > 1):
                    correctText = correctText.split("'",1)[1]
                if(widget.text == correctText or (widget.text == "" and correctText == "-")):
                    correct = True
                else:
                    correct = False
                inputCounter -= 1
            if(isinstance(widget,Image)):
                widget.height = 30
                widget.width = 30
                widget.opacity = 1
                widget.disabled = False
                if correct:
                    widget.source = "./src/img/green.png"
                else:
                    widget.source = "./src/img/red.png"

class IndicativePresent(Screen):
    tabNumber = NumericProperty(0)
    tabbedList = []
    def clearTabbedPanel(self):
        self.ids.mode.clear_tabs()
    def fillTabbedPanel(self):
        global data
        self.tabbedList = []
        first = True
        for (typ,header) in zip(data.types,data.headers):
            typ_Panel = TabbedPanelItem(text=str(typ))
            innerPanel = TabbedPanel(do_default_tab=False, tab_width=125)
            self.tabbedList.append(innerPanel)
            for head in header:
                innerPanel.add_widget(MyTabbedPanelItem(text=str(head)))
            typ_Panel.add_widget(innerPanel)
            self.ids.mode.add_widget(typ_Panel)
            if(first):
                self.ids.mode.default_tab = typ_Panel
                first = False
    def on_pre_enter(self, *args):
        self.updater()
        return super().on_pre_enter(*args)
    def returnToStart(self):
        self.manager.transition.direction = "down"
        self.manager.current = "Start"
    def newRandomWordThread(self):
        global data
        global verbs
        global verb_eng
        global verb_pl
        data = obtenirVerb.obtenirVerb(random.choice(verbs))
        blob = TextBlob(data.verb)
        assignTranslation(blob)
        self.updater()
    def newRandomWord(self):
        thread = Thread(target = self.newRandomWordThread)
        thread.start()
    def searchForANewWord(self):
        thread = Thread(target = self.searchForANewWordThread)
        thread.start()
        self.ids.verbInputInside.text = ""
    def searchForANewWordThread(self):
        global data
        global verb_eng
        global verb_pl
        verb = self.ids.verbInputInside.text
        verb = verb.replace(" ","_")
        data = obtenirVerb.obtenirVerb(verb)
        blob = TextBlob(data.verb)
        assignTranslation(blob)
        self.updater()
    @mainthread
    def updater(self):
        global data
        self.ids.verbInputInside.text = ""
        if data.verb:
            self.ids.verbName.text = '[size=20][b][i]' + data.verb + '[/i][/b][/size]'
        else:
            self.ids.verbName.text = "[size=20][b][i] Verb not found [/i][/b][/size]"
        self.ids.verbNameEng.text = '[size=20][b][i]' + verb_eng + '[/i][/b][/size]'
        self.ids.verbNamePl.text = '[size=20][b][i]' + verb_pl + '[/i][/b][/size]'
        self.clearTabbedPanel()
        self.fillTabbedPanel()
        for (typ,conj) in zip(self.tabbedList,data.conjugated):
            for (header,forms) in zip(typ._tab_strip.children[::-1],conj):
                number = 0
                for (label, newText) in zip(header.content.children[1].children[0].children[::-1], forms):
                    number += 1
                    label.text = newText
                diff = len(header.content.children[1].children[0].children) - len(forms)
                if(diff > 0):
                    for (label, x) in zip(header.content.children[1].children[0].children,range(diff)):
                        label.text = ""
                        
                    

class LearnFrenchApp(App):
    def build(self):
        self.icon ="./src/img/french_Flag.png"
        self.title = "Conjugaison française"
        kv = Builder.load_file("ConjugaisonFrancaise.kv")
        return kv


if __name__ == '__main__':
    LearnFrenchApp().run()