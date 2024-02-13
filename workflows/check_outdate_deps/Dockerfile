FROM python:3.12-slim

COPY check_outdate_deps.sh /check_outdate_deps.sh

RUN chmod +x /check_outdate_deps.sh

# needed for the open_issue.py
RUN pip3 install requests

ENTRYPOINT [ "/check_outdate_deps.sh" ]
