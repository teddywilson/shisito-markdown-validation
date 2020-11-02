FROM python:3

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

COPY . /

ADD shisito.py /
RUN chmod +x /shisito.py

CMD [ "python", "/shisito.py" ]
