# Flask Microblog

Practice project based on the tutorial ["Build a Microblog with Flask"](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) from the [project-based-learning](https://github.com/practical-tutorials/project-based-learning) catalog. The application lets users register, publish short posts, subscribe to other authors, edit profiles, and search through users and content. This version is adapted for the web-development practice report and demo scenario.

## Features

- registration and login
- personal feed with followed authors' posts
- user profiles with editable description
- create, edit, and delete post
- follow and unfollow other users
- search by username or post text
- seeded demo data for report screenshots and video

## Stack

- frontend: Flask templates, HTML, CSS
- backend: Python 3, Flask
- database: SQLite, Flask-SQLAlchemy

## Local run

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
flask --app run init-db
flask --app run run
```

The application will be available at `http://127.0.0.1:5000`.

## Demo credentials

- username: `demo_alice`
- password: `demo123`

## Project source from catalog

- catalog entry: [project-based-learning / Build a Microblog with Flask](https://github.com/practical-tutorials/project-based-learning)
- tutorial: [The Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

## Deployment

- add your deployment URL here after publishing, for example on Render or Railway

## Tests

```bash
pytest
```
