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
    username = StringField('アカウント名', validators=[
        DataRequired(message='アカウント名を入力してください'),
    ])

    password = PasswordField('パスワード', validators=[
        DataRequired(message='パスワードを入力してください'),
    ])

    submit = SubmitField('送信')


class SignupForm(FlaskForm):
    username = StringField('アカウント名', validators=[
        DataRequired(message='アカウント名を入力してください'),
        Length(max=20, message='文字数が多すぎます'),
        Regexp(r'^[A-Za-zぁ-んァ-ヶ一-龯ー]+$',
               message='使用できない文字が含まれています')
    ])

    email = StringField('メールアドレス', validators=[
        DataRequired('メールアドレスを入力してください'),
        Regexp(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
               message='メールアドレスが正しくありません'),
    ])

    password = PasswordField('パスワード', validators=[
        Length(min=8, message='パスワードは8文字以上で入力してください'),
        DataRequired('パスワードを入力してください'),
        Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=])[A-Za-z\d!@#$%^&*()_+\-=]+$',
               message='パスワードは8文字以上で、英大文字・小文字・数字・記号（!@#$%^&*()_+-=）を含めてください。'),
        EqualTo('confirm', message='パスワードが一致しません')
    ])
    confirm = PasswordField('パスワード再入力', validators=[
        DataRequired('パスワードを入力してください')
    ])
    submit = SubmitField('送信')


class MessageForm(FlaskForm):
    message = StringField('message', validators=[
        DataRequired('メッセージを入力してください'),
        Length(max=100, message='100文字以内で入力してください')
    ])
    submit = SubmitField('送信')
