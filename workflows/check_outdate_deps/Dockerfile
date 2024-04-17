FROM python:3.12-slim

COPY check_deps.py /check_deps.py
RUN chmod +x /check_deps.py

RUN pip3 install requests; \
	apt-get update; \
	apt-get install -y --no-install-recommends git

ENTRYPOINT [ "/check_deps.py" ]
