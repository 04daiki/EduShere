from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, FileField, HiddenField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from models import User
from flask_wtf.file import FileAllowed

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
        
class PostForm(FlaskForm):
    
    condition_choices = [
        ('1', 'Option 1'),
        ('2', 'Option 2'),
        ('3', 'Option 3'),
    ]
    
    category_choices = [
        ('1', 'Option 1'),
        ('2', 'Option 2'),
        ('3', 'Option 3'),
    ]
    
    genre_choices = [
        ('1', 'Option 1'),
        ('2', 'Option 2'),
        ('3', 'Option 3'),
    ]
    
    photo = FileField(validators=[DataRequired(),FileAllowed(['jpg', 'jpeg', 'png'])])
    item_name = StringField('教材名', validators=[DataRequired(), Length(min=1, max=50)])
    post_text = StringField('備考')
    condition = SelectField('商品状態', choices=condition_choices, validators=[DataRequired()])
    category = SelectField('カテゴリー', choices=category_choices, validators=[DataRequired()])
    genre = SelectField('分類', choices=genre_choices, validators=[DataRequired()])
    submit = SubmitField('投稿')

class Requestform(FlaskForm):
    userid = HiddenField('userid')
    submit = SubmitField('リクエストを送信する',render_kw={"onclick": "return confirm('本当に送信しますか？');"})