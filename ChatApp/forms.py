from flask_wtf import FlaskForm
from wtforms import (
        StringField,
        PasswordField,
        SubmitField,
        )
from wtforms.validators import (
        DataRequired,
        Length,
        EqualTo,
        Regexp
        )


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message='アカウント名を入力してください')], 
        render_kw={"placeholder": "Email"}
        )

    password = PasswordField('Password', validators=[
        DataRequired(message='パスワードを入力してください')], 
        render_kw={"placeholder": "Password"}
        )

    submit = SubmitField('ログイン')


class SignupForm(FlaskForm):
    username = StringField('Account Name', validators=[
        DataRequired(message='アカウント名を入力してください'),
        Length(max=20, message='文字数が多すぎます'),
        Regexp(r'^[A-Za-zぁ-んァ-ヶ一-龯ー_]+$',
        message='使用できない文字が含まれています')], 
        render_kw={"placeholder": "Raretech-ro"}
        )

    email = StringField('Email', validators=[
        DataRequired('メールアドレスを入力してください'),
        Regexp(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
        message='メールアドレスが正しくありません')], 
        render_kw={"placeholder": "rare-tech@gmail.com"}
        )

    password = PasswordField('Password', validators=[
        Length(min=8, message='8文字以上で入力してください'),
        DataRequired('パスワードを入力してください'),
        Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d!@#$%^&*()_+\-=]+$',
        message='英大文字・小文字・数字を含めてください。'),
        EqualTo('confirm', message='パスワードが一致しません')], 
        render_kw={"placeholder": "英大小文字・数字含む8文字以上"}
        )
    
    confirm = PasswordField('Password (再入力)', validators=[
        DataRequired('パスワードを入力してください')], 
        render_kw={"placeholder": "パスワードを再入力してください"}
        )
    
    submit = SubmitField('送信')


class SearchForm(FlaskForm):
    search_friend = StringField('検索キーワード')
    submit = SubmitField('検索')


class MessageForm(FlaskForm):
    message = StringField('メッセージ', validators=[
        DataRequired('メッセージを入力してください'),
        Length(max=100, message='100文字以内で入力してください')
    ])
    submit = SubmitField('送信')
