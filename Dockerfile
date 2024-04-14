FROM python:alpine3.19

WORKDIR /bot
COPY ./requirements.txt /bot/requirements.txt
COPY ./paste.py /bot/paste.py
COPY ./.secret /bot/.secret
RUN pip3 install -r requirements.txt
CMD [ "python3", "./paste.py" ]