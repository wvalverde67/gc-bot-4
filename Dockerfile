# https://hub.docker.com/r/rasa/rasa-sdk/tags
FROM rasa/rasa:2.4.0-full


USER root

RUN pip install -U pip setuptools wheel
RUN pip install -U spacy
RUN python3 -m spacy download es_core_news_lg


