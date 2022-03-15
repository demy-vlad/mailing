### Actual branch - main.
### How to run in production:
```sh
$ docker build -t mailing .
$ docker run mailing
```
#### How stop in production:
```sh
$ docker stop mailing
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