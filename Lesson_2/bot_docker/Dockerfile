FROM python:3.10

ENV BOT_HOME /app

WORKDIR $BOT_HOME

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]
