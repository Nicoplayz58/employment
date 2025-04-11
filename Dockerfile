FROM python:3.12.4

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8050

CMD ["sh", "-c", "exec gunicorn -w 4 -b 0.0.0.0:$PORT app:server"]

