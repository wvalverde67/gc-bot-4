# https://hub.docker.com/r/rasa/rasa-sdk/tags
FROM rasa/rasa-sdk:2.4.0-full

COPY actions /app/actions

USER root
RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir -r /app/actions/requirements-actions.txt

USER 1001
CMD ["start", "--actions", "actions"]
