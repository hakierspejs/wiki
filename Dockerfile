FROM python
RUN apt-get update && apt-get install git -y && rm -rf /var/lib/apt /var/cache/apt
ADD ./requirements.txt .
RUN python -m pip install -r requirements.txt
ADD ./extract-list-of-usernames.py .
ENTRYPOINT ./extract-list-of-usernames.py
