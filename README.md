# shopify_crawler

Shopify Crawler

## Pre-requisites
-  Python 3.8+
-  Redis
-  Tmux
-  MongoDB

## Installation

```bash
$ python3 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

## Usage

Open 6 tmux sessions and run the following commands in each session (one-by-one in sequence):
-   Session 1: Start redis-server
```bash
$ redis-server
```
- Session 2: Start crawling categories and homepage of Shopify.
```bash
$ python src/run_homepage_category.py
```
- Session 3: Start crawling all apps in shopify.
```bash
$ python src/run_applications.py
```
- Session 4: Start crawling reviews of each apps.
```bash
$ python src/run_app_reviews.py
```
- Session 5: Start crawling app events
```bash
$ python src/run_app_events.py
```
- Session 6: Start crawling transactions
```bash
$ python src/run_transactions.py
```
   

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`shopify_crawler` was created by Binh Nguyen Quoc. It is licensed under the terms of the MIT license.

## Credits

`shopify_crawler` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
