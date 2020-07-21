rom flask import render_template,redirect,url_for,abort
from . import main
from . forms import CommentForm,UpdateProfile,BlogForm
from ..models import Comment, User, Blog, Role
from flask_login import login_required, current_user
from .. import db,photos
import markdown2  

# #Ajax
# @main.route('/signUp')
# def signUp():
#     return render_template('signUp.html')


# @main.route('/signUpUser', methods=['POST'])
# def signUpUser():
#     user =  request.form['username'];
#     password = request.form['password'];
#     return json.dumps({'status':'OK','user':user,'pass':password});

# Views
@main.route('/')
def index():
    '''
    function that returns the index page and its data
    '''

    title = 'My Blog'

    return render_template('index.html', title = title)

@main.route('/blog', methods=['GET','POST'])
@login_required
def new_blog():
    form = BlogForm()
    blogs = Blog.query.all()

    if form.validate_on_submit():
        new_blog=Blog(blog_title=form.title.data,blog_post=form.content.data)
        new_blog.save_blog()
        return render_template('blog.html',form=form,blogs=blogs)
    return render_template('blog.html',form=form,blogs=blogs)   

@main.route('/blog/comment/new/<int:id>', methods = ['GET','POST'])
@login_required
def new_comment(id):

    form = CommentForm()

    if form.validate_on_submit():
       
        #updated comment instance
        new_comment = Comment(Blog.id,blog_comment=Comment, user=current_user)

        #save comment method
        new_comment.save_comment()
        return redirect(url_for('.blog',form=form ))

    return render_template('new_comment.html',comment_form=form, blog=blog)

@main.route('/comment/<int:id>')
@login_required

def comment(id):
    comment=Comment.query.get(id)
    if comment is None:
        abort(404)
    format_comment = markdown2.markdown(comment.blog_comment,extras=["code-friendly", "fenced-code-blocks"])
    return render_template('comment.html',comment=comment,format_comment=format_comment)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)    


@main.route('/user/<uname>/update/pic',methods= ['GET', 'POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))    