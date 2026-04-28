from Project.Posts import bp
from flask import render_template,redirect,request
from flask_login import login_required,current_user
from Project.Models import Posts,User,Comments,Likes
from Project.Posts.forms.postform import PostsForm
import os
from Project import db,app

@bp.route('/posts',methods=["POST","GET"])
@login_required
def posts():
    form = PostsForm()
    if form.validate_on_submit():
        text = form.txt.data
        img = form.file.data
        if img:
            img.save(os.path.join(app.config['UPLOAD_FOLDER'],img.filename))
            post = Posts(text,img.filename,current_user)
        else:
            img =''
            post = Posts(text,img,current_user)
        db.session.add(post)
        db.session.commit() 
        return redirect('/posts')       
    posts = Posts.query.all()
    posts.reverse()
    likes_count = {post.id: Likes.query.filter_by(likedpost=post.id).count() for post in posts}
    return render_template("post.html",form=form,posts=posts,comments=Comments,likes=Likes,likes_count=likes_count)

@bp.route('/post/<post_id>/comment',methods=["POST"])
def comment(post_id):
    commenttxt = request.form.get("comment")
    commentobject = Comments(post_id,current_user.id,commenttxt)
    db.session.add(commentobject)
    db.session.commit()

    return redirect('/posts')

@bp.route('/post/<id>/like',methods=['POST'])
def likepost(id):
    user_id = current_user.id
    liked_post=id
    like = Likes(user_id,liked_post)
    db.session.add(like)
    db.session.commit()
    return redirect('/posts')

@bp.route('/post/<id>/unlike',methods=["POST"])
def unlikepost(id):
    user_id = current_user.id
    post_id = id
    likeobj = Likes.query.filter_by(likinguser=user_id,likedpost=post_id).first()
    db.session.delete(likeobj)
    db.session.commit()
    return redirect('/posts')

@app.route('/post/<id>')
def post(id):
    pass   