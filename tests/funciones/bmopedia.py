import wikipedia

#from __init__ import query

def bmoPedia():
    wikipedia.set_lang("es")

    queryWiki = " "

    wikipediaPage = wikipedia.summary(queryWiki, sentences=2)

    print(wikipediaPage)
   


bmoPedia()