FROM python
RUN apt-get update && apt-get install git graphviz -y && rm -rf /var/lib/apt /var/cache/apt
ADD ./requirements.txt .
RUN python -m pip install -r requirements.txt
WORKDIR /root
ADD ./extract-list-of-usernames.py .
ENTRYPOINT ./extract-list-of-usernames.py
