FROM python:3

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

COPY . /

ADD entrypoint.sh /
ADD shisito.py /
ADD test_shisito.py /

RUN chmod +x /entrypoint.sh
RUN chmod +x /shisito.py
RUN chmod +x /test_shisito.py

ENTRYPOINT [ "/entrypoint.sh"]
