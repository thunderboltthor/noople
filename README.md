# noople - the world's worst search engine

(Change `SITE_NAME` to DuckDuckNope for enhanced privacy.)

noople is a search engine that doesn't have any results. It is used for demonstration purposes only:

* Reading GET requests in Flask
* Processing SQL requests in Python
* Reflected XSS vulnerabilities
* Stored XSS vulnerabilities
* SQL injection vulnerabilities

## Run the application

Create a Python virtual environment, if you haven't already:

    python3 -m venv venv

Activate your virtual environment:

    source venv/bin/activate

Install the requirements:

    pip3 install -r requirements.txt

Run the application:

    export FLASK_APP=noople/search.py
    flask run

Visit http://localhost:5000 in a web browser.

## (Known) Vulnerabilities

### Reflected XSS

To fix this, use `escape`

### Stored XSS

To fix this, use `escape`

### SQL injection

To fix this, used bind variables
