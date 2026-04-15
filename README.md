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

- recommended platform: Render
- start command: `gunicorn run:app`
- build command: `pip install -r requirements.txt`
- environment variables: `SECRET_KEY` and optionally `DATABASE_URL`
- public URL: `https://flask-microblog-l749.onrender.com`

### Render quick setup

1. Create a new Web Service in Render from this GitHub repository.
2. Use the existing `render.yaml` settings or set `Build Command = pip install -r requirements.txt`.
3. Set `Start Command = gunicorn run:app`.
4. After the first deploy, open the service URL and register a user or use the seeded demo data locally.

## Code Climate

To target grade `4/5`, connect the repository to Code Climate and add the generated maintainability badge to this README. A short setup guide is available in [`docs/code_climate_setup.md`](docs/code_climate_setup.md).

## Tests

```bash
pytest
```
