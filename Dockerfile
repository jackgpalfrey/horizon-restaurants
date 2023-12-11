FROM python:3.10 AS prod
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./src ./src
RUN touch __init__.py
ENV PYTHONPATH "$PYTHONPATH:/app"

CMD ["python", "./src/main.py"]

FROM prod AS cli
COPY ./cli ./cli
CMD ["python", "-m", "cli/core/repl.py"]

FROM prod AS test
COPY ./tests ./tests
CMD ["python", "-m", "pytest"]