from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, User, Post, Request, Message
from forms import PostForm, Requestform, Deleteform, Messageform 
import time
from werkzeug.utils import secure_filename
import os
from authlib.integrations.flask_client import OAuth
from authlib.integrations.base_client.errors import OAuthError
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
from choices import *

# .env ファイルを読み込む
load_dotenv()

app = Flask(__name__)

# 保存先のディレクトリ
UPLOAD_FOLDER = './static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# アップロード可能な拡張子
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']

# Configuration settings
CONNECT_INFO = 'sqlite:///app.db'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = CONNECT_INFO
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['GOOGLE_CLIENT_ID'] = os.getenv('GOOGLE_CLIENT_ID')
app.config['GOOGLE_CLIENT_SECRET'] = os.getenv('GOOGLE_CLIENT_SECRET')

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    client_kwargs={'scope': 'openid profile email'},
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
)

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
    # 表示
    posts = Post.query.filter(Post.status == 1).order_by(Post.timestamps.desc()).all()
    return render_template('home.html', name=current_user.username, posts=posts, point = current_user.point, item_condition=condition_choices)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login/google')
def google_login():
    redirect_uri = url_for('google_auth_callback', _external=True)
    return google.authorize_redirect(redirect_uri, prompt='select_account')

@app.route('/auth/callback')
def google_auth_callback():
    try:
        token = google.authorize_access_token()
        resp = google.get('https://www.googleapis.com/oauth2/v1/userinfo', token=token)
        user_info = resp.json()
        email = user_info['email']

        user = User.query.filter_by(email=email).first()
        if user is None:
            user = User(
                email=email, 
                username=user_info['name'],
                password_hash=generate_password_hash('default_password')  
            )
            db.session.add(user)
            db.session.commit()

        login_user(user)
        return redirect(url_for('home'))
    except OAuthError as error:
        flash(f'Authentication failed: {error.description}', 'danger')
        return redirect(url_for('login'))
    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('ログアウトしました。')
    return redirect(url_for('login'))


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
            
            #teplatesディレクトリからの相対パスに変換
            file_path = "." + file_path
        
        post = Post(post_text = form.post_text.data, user_id = current_user.id, image_path=file_path, 
                    item_name=form.item_name.data, condition=form.condition.data, category=form.category.data, genre=form.genre.data, status=1, subject=form.Subject.data)
        
        db.session.add(post)
        db.session.commit()
        flash('商品を投稿しました')

        return redirect(url_for('home'))
        
    # GET時
    
    return render_template('post.html',form=form)

@app.route('/detail/<int:post_id>', methods=['GET', 'POST'])
@login_required
def show_detail(post_id):
    
    message_display = False
    
    dform = Deleteform()
    rform = Requestform()
    mform = Messageform()
    
    # クリックされた教材の行取得
    post = Post.query.filter_by(post_id=post_id).first()
    if not post:
        flash('該当する投稿が見つかりません。')
        return redirect(url_for('home'))
    
    # リクエストが承認された教材かどうか
    if post.status == 0:
        #リクエストあるかどうか
        if post.request:
            for req in post.request:
                #メッセージ機能を使える人か
                if req.user_id == current_user.id or req.recipient_id == current_user.id:
                    message_display = True
                    messages = Message.query.filter_by(post_id = post_id).order_by(Message.timestamps.desc()).all()
                    return render_template('detail.html', name=current_user.username, id=current_user.id, post=post, form=mform,
                                    category=category_choices, subject=subject_choices, genre=genre_choices, condition=condition_choices, message_display=message_display,messages=messages) 
    
    #削除時の動作
    if dform.validate_on_submit():
        
        #ポイントの払い戻し
        # for request in post.request:
        #     request.user.point = request.user.point + 1
 
        db.session.delete(post)
        db.session.commit()
        flash('商品を削除しました')
        return redirect(url_for('home'))
        
    if post.user_id == current_user.id:
        return render_template('detail.html', name=current_user.username, id=current_user.id, post=post, form=dform,
                                category=category_choices, subject=subject_choices, genre=genre_choices, condition=condition_choices, message_display=message_display, point=current_user.point)
    else:
        return render_template('detail.html', name=current_user.username, id=current_user.id, post=post, form=rform,
                                category=category_choices, subject=subject_choices, genre=genre_choices, condition=condition_choices, message_display=message_display, point=current_user.point)

#リクエストボタンが押された時   
@app.route('/detail/request/<int:post_id>', methods=['GET', 'POST'])
@login_required
def request(post_id):
    rform = Requestform()

    
    if rform.validate_on_submit():
        
        # 送信時にポイント-1(リクエスト送信側)、ポイント+1(リクエスト送信側)
        # sender = User.query.filter_by(id=current_user.id).first()
        # sender.point = sender.point - 1
        
        # receiver = Post.query.filter_by(post_id=post_id).first()
        # receiver.user.point = receiver.user.point + 1
        
        # リクエスト追加
        request = Request(request_text = rform.message.data, user_id = current_user.id, post_id = post_id, recipient_id = rform.userid.data)
        db.session.add(request)
        
        #取引成立フラグ、ホームに表示されないように
        post = Post.query.filter_by(post_id=post_id, status = 1).first()
        post.status = 0
        
        db.session.commit()
        flash('リクエストが送信されました')
        return redirect(url_for('home'))
    
@app.route('/detail/message/<int:post_id>', methods=['GET', 'POST'])
@login_required
def message(post_id):
    mform = Messageform()
    post = Post.query.filter_by(post_id=post_id).first()
    
    if mform.validate_on_submit():
        for req in post.request:       
            messages = Message(post_id=post_id, request_id=req.request_id, user_id=mform.userid.data, message=mform.message.data)
        db.session.add(messages)
        db.session.commit()
        
        return redirect(url_for('show_detail', post_id=post.post_id))
    

@app.route('/list')
@login_required
def list():
    item_condition =[
        "未開封",
        "非常に良い",
        "良い",
        "傷あり",
        "汚れあり",
        "傷と汚れあり",
        "ジャンク品"
    ]
    posts = Post.query.filter(Post.user_id == current_user.id ).order_by(Post.timestamps.desc()).all()
    return render_template('list.html', posts=posts, item_condition=item_condition)

@app.route('/notification')
@login_required
def notification():
    # requests = Request.query.filter(Request.recipient_id == current_user.id).order_by(Request.timestamps.desc()).all()
    requests = Request.query.order_by(Request.timestamps.desc()).all()
    return render_template('notification.html', requests=requests, current_user=current_user.id)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)