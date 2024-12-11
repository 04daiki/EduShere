from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField, SelectField, FileField, HiddenField, TextAreaField


from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from models import User
from flask_wtf.file import FileAllowed
from wtforms import TextAreaField, validators
        
class PostForm(FlaskForm):
    
    condition_choices = [
        ('', '選択してください'),  # 初期値
        ('1', '未開封'),
        ('2', '非常に良い'),
        ('3', '良い'),
        ('4', '傷あり'),
        ('5', '汚れあり'),
        ('6', '傷と汚れあり'),
        ('7', 'ジャンク品'),
    ]
    
    category_choices = [
        ('', '選択してください'),  # 初期値
        ('1', 'Option 1'),
        ('2', 'Option 2'),
        ('3', 'Option 3'),
        ('4', 'その他'),
    ]
    
    genre_choices = [
        ('', '選択してください'),  # 初期値
        ('1', '参考書'),
        ('2', '問題集'),
        ('3', '教科書'),
        ('4', '機材'),
        ('5', 'その他'),
    ]
    
    subject_choices = [
        ('', '選択してください'),  # 初期値
        ('1', '国語'),
        ('2', '数学'),
        ('3', 'ドイツ語'),
        ('4', 'その他'),
    ]
    
    photo = FileField('画像を追加する', validators=[DataRequired()])
    item_name = TextAreaField('教材名', validators=[DataRequired(), Length(min=1, max=50)],render_kw={"rows": 3, "cols": 50,"placeholder": "教材名を入力してください","maxlength": 50})
    post_text = TextAreaField('コメント',render_kw={"rows": 5, "cols": 50, "placeholder": "コメントを入力してください","maxlength": 150})
    condition = SelectField('商品状態', choices=condition_choices, validators=[DataRequired()])
    category = SelectField('カテゴリー', choices=category_choices, validators=[DataRequired()])
    genre = SelectField('分類', choices=genre_choices, validators=[DataRequired()])
    Subject = SelectField('科目', choices=subject_choices, validators=[DataRequired()])
    submit = SubmitField('投稿')

class Requestform(FlaskForm):
    userid = HiddenField('userid')
    message = TextAreaField('リクエストメッセージ', validators=[DataRequired()], render_kw={"rows": 5, "cols": 50, "placeholder": "コメントを入力してください","maxlength": 150})
    submit = SubmitField('リクエストを送信する',render_kw={"onclick": "return confirm('本当に送信しますか？');"})