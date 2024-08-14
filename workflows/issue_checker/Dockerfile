FROM python:slim

COPY issue_checker.py /run.py
RUN chmod +x /run.py

RUN pip3 install requests; \
	apt-get update; \
	apt-get install -y --no-install-recommends git

ENTRYPOINT [ "/run.py" ]
