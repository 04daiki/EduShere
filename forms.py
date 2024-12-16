from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField, SelectField, FileField, HiddenField, TextAreaField


from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from models import User
from flask_wtf.file import FileAllowed
from wtforms import TextAreaField, validators
        
class PostForm(FlaskForm):
    
    condition_choices = [
        ('', '選択してください'),
        ('1', '未開封'),
        ('2', '非常に良い'),
        ('3', '良い'),
        ('4', '傷あり'),
        ('5', '汚れあり'),
        ('6', '傷と汚れあり'),
        ('7', 'ジャンク品'),
    ]
    
    category_choices = [
        ('', '選択してください'),
        ('1', 'AI・IT・Iot・情報処理系'),
        ('2', 'ゲームプログラミング系'),
        ('3', 'アニメ制作・アニメーター・キャラクターデザイン系'),
        ('4', '音・楽曲制作・音響効果・ゲームサウンド系'),
        ('5', '建築・インテリアデザイン系'),
        ('6', 'ロボット制御・センサー・電子回路系'),
        ('7', 'eスポーツイベント企画・運営系'),
        ('8', '声優・タレント・ナレーター・俳優系'),
        ('9', 'グラフィック・Webデザイン・動画系'),
        ('10', '国際コミュニケーション系'),
        ('11', 'ビジネス・パソコン活用・事務・企画・営業販売系'),
        ('12', 'ゲームCG・3DCG映像作成系'),
        ('13', '音響・照明・映像・レコーディング系'),
        ('14', '製品デザイン・機械設計・3次元CAD'),
        ('15', '日本語系'),
    ]
        
    genre_choices = [
        ('', '選択してください'),
        ('1', '参考書'),
        ('2', '問題集'),
        ('3', '教科書'),
        ('4', '機材'),
        ('5', 'その他'),
    ]
    
    # 項目数が必要のため最大項目数に合わせて設定する
    subject_choices = [
        ('', '選択してください'),
        ('1', '国語'),('2', '数学'),('3', 'ドイツ語'),('4', 'ドイツ語'),('5', 'ドイツ語'),
        ('6', 'ドイツ語'),('7', 'ドイツ語'),('8', 'ドイツ語'),('9', 'ドイツ語'),('10', 'ドイツ語'),
        ('11', 'ドイツ語'),('12', 'ドイツ語'),('13', 'ドイツ語'),('14', 'ドイツ語'),('15', 'ドイツ語'),
        ('16', 'ドイツ語'),('17', 'ドイツ語'),('18', 'ドイツ語'),('19', 'ドイツ語'),('20', 'ドイツ語'),
        ('21', 'ドイツ語'),('22', 'ドイツ語'),('23', 'ドイツ語'),('24', 'ドイツ語'),('25', 'ドイツ語'),
        ('26', 'ドイツ語'),('27', 'ドイツ語'),('28', 'ドイツ語'),('29', 'ドイツ語'),('30', 'ドイツ語'),
        ('31', 'ドイツ語'),('32', 'ドイツ語'),('33', 'ドイツ語'),('34', 'ドイツ語'),('35', 'ドイツ語'),
        ('36', 'ドイツ語'),('37', 'ドイツ語'),('38', 'ドイツ語'),('39', 'ドイツ語'),('40', 'ドイツ語'),
        ('41', 'ドイツ語'),('42', 'ドイツ語'),('43', 'ドイツ語'),('44', 'ドイツ語'),('45', 'ドイツ語'),
        ('46', 'ドイツ語'),('47', 'ドイツ語'),('48', 'ドイツ語'),('49', 'ドイツ語'),('50', 'ドイツ語'),
        ('51', 'ドイツ語'),('52', 'ドイツ語'),('53', 'ドイツ語'),('54', 'ドイツ語'),('55', 'ドイツ語'),
        ('56', 'ドイツ語'),('57', 'ドイツ語'),('58', 'ドイツ語'),('59', 'ドイツ語'),('60', 'ドイツ語'),
        ('61', 'ドイツ語'),('62', 'ドイツ語'),('63', 'ドイツ語'),('64', 'ドイツ語'),('65', 'ドイツ語'),
        ('66', 'その他'),
    ]
    
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
    message = TextAreaField('リクエストメッセージ', validators=[DataRequired()], render_kw={"rows": 5, "cols": 50, "placeholder": "コメントを入力してください","maxlength": 150})
    submit = SubmitField('リクエストを送信する',render_kw={"onclick": "return confirm('本当に送信しますか？');"})

class Deleteform(FlaskForm):
    submit = SubmitField('投稿を削除',render_kw={"onclick": "return confirm('本当に削除しますか？');"}) 