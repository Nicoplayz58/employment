FROM python:3.12.4

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8050

CMD ["python", "app.py"]

