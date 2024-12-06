from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, User, Post
from forms import LoginForm, RegistrationForm, PostForm
import time
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# 保存先のディレクトリ
UPLOAD_FOLDER = './static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# アップロード可能な拡張子
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Configuration settings
CONNECT_INFO = 'sqlite:///app.db'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = CONNECT_INFO
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User loader function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
@login_required
def home():
    # return render_template('headerfooter.html', name=current_user.username)

    # 表示
    posts = Post.query.order_by(Post.timestamps.desc()).all()
    return render_template('home.html', name=current_user.username, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('ログインに成功しました。')
            return redirect(url_for('home'))
        else:
            flash('ユーザー名またはパスワードが無効です。')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('ログアウトしました。')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('ユーザー登録が完了しました。')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form = PostForm()
    # POST時
    if form.validate_on_submit():
        
        file = form.photo.data
        if file:
            # ファイル名を安全な形式に変換
            filename = secure_filename(file.filename)

            # ファイル名にタイムスタンプを追加してリネーム
            new_filename = f"{int(time.time())}_{filename}"

            # 保存パスを構築
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)

            # ファイルを保存
            file.save(file_path)
        
        post = Post(post_text = form.post_text.data, user_id = current_user.id, image_path=file_path, 
                    item_name=form.item_name.data, condition=form.condition.data, category=form.category.data, genre=form.genre.data, status=1)
        
        db.session.add(post)
        db.session.commit()
        flash('商品を投稿しました')

        return redirect(url_for('home'))
        
    # GET時
    
    return render_template('post.html',form=form)
    

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)