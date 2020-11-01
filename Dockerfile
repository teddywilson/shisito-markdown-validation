FROM python:3

COPY requirements.txt /tmp/
COPY . /

RUN pip install -r /tmp/requirements.txt

ADD shisito.py /
RUN chmod +x /shisito.py

CMD [ "python", "/shisito.py" ]
