from sqlalchemy import or_
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app import db
from app.models import Post, User


def register_routes(app):
    @app.route("/")
    def index():
        if current_user.is_authenticated:
            posts = current_user.followed_posts().all()
        else:
            posts = Post.query.order_by(Post.created_at.desc()).all()
        return render_template("index.html", posts=posts)

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for("index"))

        if request.method == "POST":
            username = request.form.get("username", "").strip()
            email = request.form.get("email", "").strip().lower()
            password = request.form.get("password", "")
            confirm_password = request.form.get("confirm_password", "")

            if not username or not email or not password:
                flash("Fill in all required fields.", "error")
            elif password != confirm_password:
                flash("Passwords do not match.", "error")
            elif User.query.filter(
                or_(User.username == username, User.email == email)
            ).first():
                flash("User with this username or email already exists.", "error")
            else:
                user = User(username=username, email=email)
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
                flash("Registration completed. Sign in with your new account.", "success")
                return redirect(url_for("login"))

        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("index"))

        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")
            user = User.query.filter_by(username=username).first()

            if user is None or not user.check_password(password):
                flash("Invalid username or password.", "error")
            else:
                login_user(user)
                flash("You are signed in.", "success")
                next_page = request.args.get("next")
                return redirect(next_page or url_for("index"))

        return render_template("login.html")

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("You are signed out.", "success")
        return redirect(url_for("index"))

    @app.route("/users")
    def users():
        all_users = User.query.order_by(User.username.asc()).all()
        return render_template("users.html", users=all_users)

    @app.route("/user/<username>")
    def profile(username):
        user = User.query.filter_by(username=username).first_or_404()
        posts = user.posts.order_by(Post.created_at.desc()).all()
        return render_template("profile.html", profile_user=user, posts=posts)

    @app.route("/profile/edit", methods=["GET", "POST"])
    @login_required
    def edit_profile():
        if request.method == "POST":
            new_username = request.form.get("username", "").strip()
            about_me = request.form.get("about_me", "").strip()

            if not new_username:
                flash("Username cannot be empty.", "error")
            else:
                username_owner = User.query.filter_by(username=new_username).first()
                if username_owner and username_owner.id != current_user.id:
                    flash("This username is already taken.", "error")
                else:
                    current_user.username = new_username
                    current_user.about_me = about_me
                    db.session.commit()
                    flash("Profile updated.", "success")
                    return redirect(url_for("profile", username=current_user.username))

        return render_template("edit_profile.html")

    @app.route("/posts/create", methods=["GET", "POST"])
    @login_required
    def create_post():
        if request.method == "POST":
            body = request.form.get("body", "").strip()
            if not body:
                flash("Post text cannot be empty.", "error")
            elif len(body) > 280:
                flash("Post text must be no longer than 280 characters.", "error")
            else:
                db.session.add(Post(body=body, author=current_user))
                db.session.commit()
                flash("Post published.", "success")
                return redirect(url_for("index"))

        return render_template("post_form.html", post=None)

    @app.route("/posts/<int:post_id>/edit", methods=["GET", "POST"])
    @login_required
    def edit_post(post_id):
        post = Post.query.get_or_404(post_id)
        if post.author_id != current_user.id:
            flash("You can edit only your own posts.", "error")
            return redirect(url_for("index"))

        if request.method == "POST":
            body = request.form.get("body", "").strip()
            if not body:
                flash("Post text cannot be empty.", "error")
            elif len(body) > 280:
                flash("Post text must be no longer than 280 characters.", "error")
            else:
                post.body = body
                db.session.commit()
                flash("Post updated.", "success")
                return redirect(url_for("profile", username=current_user.username))

        return render_template("post_form.html", post=post)

    @app.route("/posts/<int:post_id>/delete", methods=["POST"])
    @login_required
    def delete_post(post_id):
        post = Post.query.get_or_404(post_id)
        if post.author_id != current_user.id:
            flash("You can delete only your own posts.", "error")
            return redirect(url_for("index"))

        db.session.delete(post)
        db.session.commit()
        flash("Post deleted.", "success")
        return redirect(url_for("profile", username=current_user.username))

    @app.route("/follow/<username>", methods=["POST"])
    @login_required
    def follow(username):
        user = User.query.filter_by(username=username).first_or_404()
        current_user.follow(user)
        db.session.commit()
        flash(f"You are now following {username}.", "success")
        return redirect(url_for("profile", username=username))

    @app.route("/unfollow/<username>", methods=["POST"])
    @login_required
    def unfollow(username):
        user = User.query.filter_by(username=username).first_or_404()
        current_user.unfollow(user)
        db.session.commit()
        flash(f"You stopped following {username}.", "success")
        return redirect(url_for("profile", username=username))

    @app.route("/search")
    def search():
        query = request.args.get("q", "").strip()
        users = []
        posts = []
        if query:
            users = User.query.filter(User.username.ilike(f"%{query}%")).all()
            posts = (
                Post.query.join(User)
                .filter(or_(Post.body.ilike(f"%{query}%"), User.username.ilike(f"%{query}%")))
                .order_by(Post.created_at.desc())
                .all()
            )
        return render_template("search.html", query=query, users=users, posts=posts)
