import flask, flask_login
from datetime import datetime
from base import app,DBList

posts = DBList("posts")
info = {
    "project_name": "Hack-A-Blog",
    "source_url": "TODO",
}

@app.route("/post/<int:post_id>")
def view_post(post_id):
    return flask.render_template("view_one.html", post=posts[post_id], **info)

@app.route("/")
def view_posts():
    return flask.render_template('view.html', posts=reversed(posts), **info)

@app.route("/new_post", methods=["GET","POST"])
@flask_login.login_required
def new_post():
    if flask.request.method == "GET":
        return flask.render_template("new.html", **info)
    title = flask.request.form.get('title', 'untitled post')
    content = flask.request.form.get('content', '')
    post_id = len(posts)
    posts.append({
        "author": flask_login.current_user.id,
        "title": title,
        "content": content,
        "creation_time": datetime.now(),
        "edit_time": datetime.now(),
        "id": len(posts), # posts[post_id] == post
    })
    return flask.redirect(flask.url_for("view_posts"))

@app.route("/edit_post/<int:post_id>", methods=["GET", "POST"])
@flask_login.login_required
def edit_post(post_id):
    old_post = posts[post_id]
    if flask_login.current_user.id != old_post["author"]:
        return 'Unauthorized -- not the original author', 401
    if flask.request.method == "GET":
        return flask.render_template("edit.html", post=old_post, **info)
    title = flask.request.form.get('title', old_post["title"])
    content = flask.request.form.get('content', old_post["content"])
    posts[post_id] = {
        "author": old_post["author"],
        "title": title,
        "content": content,
        "creation_time": old_post["creation_time"],
        "edit_time": datetime.now(),
        "id": old_post["id"],
    }
    return flask.redirect(flask.url_for("view_post", post_id=post_id))
