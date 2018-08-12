FROM python:2.7

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

COPY . .

EXPOSE 5000 8000

CMD [ "python", "main.py", "-p", "5000", "-h", "0.0.0.0" ]

