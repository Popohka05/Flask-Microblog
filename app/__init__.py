import os
from pathlib import Path

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message = "Please sign in to continue."


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    instance_path = Path(app.instance_path)
    instance_path.mkdir(parents=True, exist_ok=True)
    default_db_path = instance_path / "microblog.db"

    app.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-secret-key-change-me"),
        SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL", f"sqlite:///{default_db_path}"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)

    from app import models, routes

    models.register_login_loader()
    routes.register_routes(app)
    register_cli(app)

    return app


def register_cli(app):
    from app.models import Post, User

    @app.cli.command("init-db")
    def init_db():
        """Create tables and seed demo data for the practice project."""
        with app.app_context():
            db.drop_all()
            db.create_all()

            alice = User(
                username="demo_alice",
                email="alice@example.com",
                about_me="Frontend-oriented tester account.",
            )
            alice.set_password("demo123")

            bob = User(
                username="demo_bob",
                email="bob@example.com",
                about_me="Backend-oriented tester account.",
            )
            bob.set_password("demo123")

            charlie = User(
                username="demo_charlie",
                email="charlie@example.com",
                about_me="Full-stack tester account.",
            )
            charlie.set_password("demo123")

            db.session.add_all([alice, bob, charlie])
            db.session.flush()

            alice.follow(bob)
            alice.follow(charlie)
            bob.follow(charlie)

            db.session.add_all(
                [
                    Post(
                        body="Welcome to Flask Microblog. This seeded post helps demonstrate the feed.",
                        author=alice,
                    ),
                    Post(
                        body="Users can follow each other and build a personalized timeline.",
                        author=bob,
                    ),
                    Post(
                        body="Search, profile editing, and post management are ready for the practice demo.",
                        author=charlie,
                    ),
                ]
            )

            db.session.commit()
            print("Database initialized.")
            print("Demo credentials: demo_alice / demo123")


# Expose a module-level WSGI app so platforms like Render can run `gunicorn app:app`
# even if the service start command is configured without `run.py`.
app = create_app()
