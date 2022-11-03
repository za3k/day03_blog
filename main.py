import flask, flask_login
from datetime import datetime
from base import app,DBList

posts = DBList("posts")
info = {
    "project_name": "Hack-A-Blog",
    "source_url": "TODO",
}

@app.route("/post/{post_id}")
def view_post(post_id):
    return flask.render_template("view_one.html", post=posts[post_id], **info)

@app.route("/")
def view_posts():
    return flask.render_template('view.html', posts=posts, **info)

@app.route("/new_post")
@flask_login.login_required
def new_post(content):
    post = {
        "author": current_user.id,
        "content": content,
        "creation_time": datetime.now(),
        "edit_time": datetime.now(),
    }
    posts.append(post)
    post_id = len(posts)
    return flask.redirect_to("view_post", post_id)

@app.route("/edit_post/{post_id}")
@flask_login.login_required
def edit_post(post_id, new_content):
    post = posts[post_id]
    post["edit_time"] = datetime.now()
    post["content"] = new_content
    posts[post_id] = post
    return flask.redirect_to("view_post", post_id)
