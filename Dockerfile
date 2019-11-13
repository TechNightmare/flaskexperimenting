FROM python:3-onbuild
EXPOSE 5000

RUN pip install -r requirements.txt

WORKDIR /app

COPY . .

CMD python app.py
