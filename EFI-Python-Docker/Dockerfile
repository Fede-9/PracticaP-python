FROM alpine:3.10

RUN apk add --no-cache  python3 \
    && pip3 install --upgrade pip

WORKDIR /appflask 

COPY . /appflask

RUN /bin/sh -c pip3 install -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["app.py"]





