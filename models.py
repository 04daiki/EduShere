from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone  # datetimeを明示的にインポート

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    posts = db.relationship('Post', back_populates = 'user')

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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # ユーザーID
    image_path = db.Column(db.String, nullable=False)  # 画像パス
    item_name = db.Column(db.String(50), nullable=False)  # 商品名
    condition = db.Column(db.Integer, nullable=False)  # 商品状態
    category = db.Column(db.Integer, nullable=False)  # カテゴリー
    genre = db.Column(db.Integer, nullable=False)  # 分類
    updatetime = db.Column(db.DateTime, nullable=True)  # 更新日
    status = db.Column(db.Integer, nullable=False)  # 取引状態
    
    user = db.relationship('User', back_populates = 'posts') 

    def __repr__(self):
        return f"<Post {self.post_id}>"

class Request(db.Model):
    __tablename__ = 'requests'
    
    request_id = db.Column(db.Integer, primary_key=True) #主キー
    request_text = db.Column(db.String(200), nullable=False) #コメント
    user_id = db.Column(db.Integer, nullable=False)  # ユーザーID
    post_id = db.Column(db.Integer, nullable=False)  # 投稿ID
    timestamps = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)) # リクエスト日'
    
    
    