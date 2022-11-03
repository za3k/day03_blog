import flask, flask_login
from datetime import datetime
from base import app,DBList

info = {
    "project_name": "Hack-A-Blog",
    "source_url": "https://github.com/za3k/day03_blog",
    "subdir": "/hackaday/blog"
}
app.config['APPLICATION_ROOT'] = info["subdir"]

posts = DBList("posts")

@app.route("/post/<int:post_id>")
def view_post(post_id):
    return flask.render_template("view_one.html", post=posts[post_id], **info)

@app.route("/")
def view_posts():
    return flask.render_template('view.html', posts=reversed(posts), **info)

@app.route("/about")
def about():
    with open("README", "r") as f:
        readme = f.read()
    return flask.render_template('about.html', content=readme, **info)

@app.route("/new_post", methods=["GET","POST"])
@flask_login.login_required
def new_post():
    if flask.request.method == "GET":
        return flask.render_template("new.html", **info)
    title = flask.request.form.get('title', '')
    content = flask.request.form.get('content', '')
    post_id = len(posts)
    posts.append({
        "author": flask_login.current_user.id,
        "title": title or 'untitled post',
        "content": content,
        "creation_time": datetime.now(),
        "edit_time": datetime.now(),
        "id": len(posts), # posts[post_id] == post
        "deleted": False,
    })
    return flask.redirect(flask.url_for("view_posts"))

@app.route("/edit_post/<int:post_id>", methods=["GET", "POST"])
@flask_login.login_required
def edit_post(post_id):
    post = posts[post_id]
    if flask_login.current_user.id != post["author"]:
        return 'Unauthorized -- not the original author', 401
    if flask.request.method == "GET":
        return flask.render_template("edit.html", post=post, **info)
    title = flask.request.form.get('title', post["title"])
    content = flask.request.form.get('content', post["content"])
    posts[post_id] = {
        "author": post["author"],
        "title": title,
        "content": content,
        "creation_time": post["creation_time"],
        "edit_time": datetime.now(),
        "id": post["id"],
        "deleted": False,
    }
    return flask.redirect(flask.url_for("view_post", post_id=post_id))

@app.route("/delete_post/<int:post_id>", methods=["GET"])
@flask_login.login_required
def delete_post(post_id):
    post = posts[post_id]
    if flask_login.current_user.id != post["author"]:
        return 'Unauthorized -- not the original author', 401
    post["deleted"] = True
    posts[post_id] = post
    return flask.redirect(flask.url_for("view_posts"))

if __name__ == "__main__":
    app.run(host='0.0.0.0')
