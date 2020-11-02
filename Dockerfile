FROM python:3

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

COPY . /

ADD shisito.py /
RUN chmod +x /shisito.py

LABEL "com.github.actions.icon"="check"  
LABEL "com.github.actions.color"="red"  

CMD [ "python", "/shisito.py" ]
