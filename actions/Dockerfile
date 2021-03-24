# https://hub.docker.com/r/rasa/rasa-sdk/tags
FROM rasa/rasa-sdk:2.3.1

COPY actions.py /app/actions

USER root
RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir -r /app/actions/requirements-actions.txt

USER 1001
CMD ["start", "--actions", "actions"]
