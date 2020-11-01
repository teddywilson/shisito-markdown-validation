FROM python:3

COPY requirements.txt /tmp/
COPY . /

RUN pip install -r /tmp/requirements.txt

ADD entrypoint.py /
RUN chmod +x /entrypoint.py

CMD [ "python", "/entrypoint.py" ]
