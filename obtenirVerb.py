import requests
from bs4 import BeautifulSoup
from bs4.element import NavigableString
from bs4.element import Tag

class ReturnedData():
    conjugated = []
    headers = []
    types = []
    verb = ""
    def __init__(self, conjugated, headers, types, verb):
        self.conjugated = conjugated
        self.headers = headers
        self.types = types
        self.verb = verb
def obtenirVerb(verb):
    url = 'https://la-conjugaison.nouvelobs.com/du/verbe/' + str(verb)+ '.php'
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'html.parser')

    headers = []
    types = []
    conjugaison = []
    for typ in soup.find_all("h2", class_="mode")[:-2]:
        conjugaisonByType = []
        if "Participe passé" in typ.text:
            continue
        localHeaders = []
        for span in typ.children:
            if(span.name == "span"):
                types.append(span.text)
        next_element = typ.next_sibling.next_sibling
        while(next_element.name != "h2"):
            for head in next_element.children:
                if(head.name == "h3" and head.has_attr("class") and "tempsheader" in head["class"]):
                    localHeaders.append(head.text)
                    tab = head.next_sibling
                    dataInTab = []
                    tmp = ""
                    for element in tab.contents:
                        # print(element)
                        # print(type(element))
                        if(isinstance(element,NavigableString)):
                            if(element[0] == " "):
                                element = element[1:]
                            if(len(element) != 0 and (element[0].isalpha()or element[0] == "-")):
                                tmp += str(element)
                        elif(isinstance(element,Tag)):
                            if(element.text):
                                tmp += element.text
                            elif(element.name == "br" and tmp!=""):
                                dataInTab.append(tmp)
                                tmp=""
                    if(dataInTab):    
                        conjugaisonByType.append(dataInTab)

            next_element = next_element.next_sibling.next_sibling
            #print(next_element)
        headers.append(localHeaders)
        conjugaison.append(conjugaisonByType)

    verb = soup.find("h1", class_="titre_fiche")
    if verb and len(verb.span.b.text.split(" ")) < 3:
        return ReturnedData(conjugaison,headers, types, verb.span.b.text)
    elif verb:
        return ReturnedData(conjugaison,headers, types, verb.span.b.text.split(" ")[0])
    return ReturnedData(conjugaison,headers, types, "")