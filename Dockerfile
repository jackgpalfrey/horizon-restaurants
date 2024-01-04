FROM python:3.10 AS prod
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./src ./src
COPY api-entry.py api-entry.py
CMD ["python", "./api-entry.py"]


FROM prod AS test
COPY ./tests ./tests
CMD ["python", "-m", "pytest"]
