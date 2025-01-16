from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, FileField, HiddenField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from models import User
from flask_wtf.file import FileAllowed
from wtforms import TextAreaField, validators
from choices import *
        
class PostForm(FlaskForm):
    
    photo = FileField('画像を追加する', validators=[DataRequired(), FileAllowed(['png', 'jpg', 'jpeg'], '画像形式はPNG, JPG, JPEGのみです。')])
    item_name = TextAreaField('教材名', validators=[DataRequired(), Length(min=1, max=50)],render_kw={"rows": 3, "cols": 50,"placeholder": "教材名を入力してください","maxlength": 50})
    post_text = TextAreaField('コメント',render_kw={"rows": 5, "cols": 50, "placeholder": "コメントを入力してください","maxlength": 150})
    
    condition = SelectField('商品状態', choices=condition_choices, validators=[DataRequired()], default='')
    category = SelectField('カテゴリー', choices=category_choices, validators=[DataRequired()], default='')
    genre = SelectField('分類', choices=genre_choices, validators=[DataRequired()], default='')
    Subject = SelectField('科目', choices=subject_choices, validators=[DataRequired()], default='')

    submit = SubmitField('投稿')

class Requestform(FlaskForm):
    userid = HiddenField('userid')
    # message = TextAreaField('リクエストメッセージ', validators=[DataRequired()], render_kw={"rows": 5, "cols": 50, "placeholder": "コメントを入力してください","maxlength": 150})
    submit = SubmitField('リクエスト',render_kw={"onclick": "return confirm('保有ポイントを1消費してリクエストを送信します。本当に送信しますか？');"})

class Deleteform(FlaskForm):
    submit = SubmitField('投稿を削除',render_kw={"onclick": "return confirm('本当に削除しますか？');"}) 
    
class Messageform(FlaskForm):
    userid = HiddenField('userid')
    message = TextAreaField('送信メッセージ', validators=[DataRequired()], render_kw={"placeholder": "メッセージを入力してください", "maxlength":200})
    submit = SubmitField("送信")
