# https://hub.docker.com/r/rasa/rasa-sdk/tags
FROM rasa/rasa:2.4.0-full

COPY actions /app/actions

USER root

RUN pip3 install wheel
RUN pip3 install -U pip setuptools wheel
RUN pip3 install -U spacy
RUN python3 -m spacy download es_core_news_lg

USER 1001
CMD ["start", "--actions", "actions"]


