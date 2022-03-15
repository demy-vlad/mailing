## Basic Local Alignment Search Tool
### The name of the test bot
```sh
Bot name: @nucleotide_blast_bot
URL: https://t.me/nucleotide_blast_bot
```
### Actual branch - main.
### How to run in production:
```sh
$ docker build -t blast .
$ docker run blast
```
#### How stop in production:
```sh
$ docker stop blast
```
### How to local run:
#### Download WebDriver.
```sh
https://chromedriver.chromium.org/downloads
```
#### In terminal:
```sh
$ python 3 -m venv env
$ . env/bin/activate
$ pip install -r requirements.txt
$ python main.py runserver
```