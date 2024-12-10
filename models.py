from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone  # datetimeを明示的にインポート

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    

class Post(db.Model):
    __tablename__ = 'posts'  # テーブル名を指定
    post_id = db.Column(db.Integer, primary_key=True)  # 主キー
    post_text = db.Column(db.String(200), nullable=True)  # 投稿テキスト（NULL可）
    timestamps = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))  # 投稿日
    user_id = db.Column(db.Integer, nullable=False)  # ユーザーID
    image_path = db.Column(db.String, nullable=False)  # 画像パス
    item_name = db.Column(db.String(50), nullable=False)  # 商品名
    condition = db.Column(db.Integer, nullable=False)  # 商品状態
    category = db.Column(db.Integer, nullable=False)  # カテゴリー
    genre = db.Column(db.Integer, nullable=False)  # 分類
    updatetime = db.Column(db.DateTime, nullable=True)  # 更新日
    status = db.Column(db.Integer, nullable=False)  # 取引状態

    def __repr__(self):
        return f"<Post {self.post_id}>"

# class Request(db.Model):
#     __tablename__ = 'requests'
    
    
    