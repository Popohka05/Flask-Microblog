from app import create_app, db
from app.models import Post, User


def make_app():
    app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test-secret",
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )
    return app


def create_user(username="alice", email="alice@example.com", password="secret123"):
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user


def test_register_login_create_post_and_search():
    app = make_app()

    with app.app_context():
        db.create_all()

    client = app.test_client()

    response = client.post(
        "/register",
        data={
            "username": "alice",
            "email": "alice@example.com",
            "password": "secret123",
            "confirm_password": "secret123",
        },
        follow_redirects=True,
    )
    assert b"Registration completed" in response.data

    response = client.post(
        "/login",
        data={"username": "alice", "password": "secret123"},
        follow_redirects=True,
    )
    assert b"You are signed in" in response.data

    response = client.post(
        "/posts/create",
        data={"body": "First practice-ready post"},
        follow_redirects=True,
    )
    assert b"Post published" in response.data
    assert b"First practice-ready post" in response.data

    response = client.get("/search?q=practice-ready")
    assert b"First practice-ready post" in response.data


def test_follow_and_feed():
    app = make_app()

    with app.app_context():
        db.create_all()
        alice = create_user()
        bob = create_user("bob", "bob@example.com")
        post = Post(body="Bob shares an update", author=bob)
        db.session.add(post)
        alice.follow(bob)
        db.session.commit()

    client = app.test_client()
    response = client.post(
        "/login",
        data={"username": "alice", "password": "secret123"},
        follow_redirects=True,
    )

    assert b"Bob shares an update" in response.data
