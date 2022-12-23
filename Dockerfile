FROM python:3

RUN pip install PlexAPI

COPY overseerr_cleaner.py /overseerr_cleaner.py

CMD python -u ./overseerr_cleaner.py