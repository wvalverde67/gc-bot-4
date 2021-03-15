import spacy

nlp = spacy.load("es_core_news_lg")
doc = nlp("Apple esta buscando la compra de una emergente del Reino Unido por mil millones de dolares")
for token in doc:
    print(token.text, token.pos_, token.dep_)

