FROM alpine:3

RUN apk --update --no-cache add python3 py3-pip && \
	ln -sf /usr/bin/python3 /usr/bin/python

WORKDIR /
COPY . .

RUN pip3 install -r requirements.txt

ENTRYPOINT ["/script.py"]
