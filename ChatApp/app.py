from flask import (
        Flask,
        redirect,
        url_for,
        render_template,
        request,
        session,
        flash
        )
from forms import SignupForm, LoginForm

from flask_login import (
        LoginManager,
        login_user,
        logout_user,
        login_required,
        current_user
        )
from flask_bcrypt import (
        Bcrypt,
        generate_password_hash,
        check_password_hash
        )
from datetime import timedelta
import uuid
import os
from models import User

SESSION_DAYS = 7


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', uuid.uuid4().hex)
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=SESSION_DAYS)

# Flask-Login初期化
login_manager = LoginManager(app)
login_manager.init_app(app)

bcrypt = Bcrypt(app)


@login_manager.user_loader
def load_user(uid):
    print(f'[load_user] uid: {uid}')
    user = User.get_by_id(uid)
    print(f'[load_user] user: {user}')
    return user


# ルートの定義
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home_view'))
    return redirect(url_for('login_view'))


# 新規登録
@app.route('/signup', methods=['GET'])
def signup_view():
    form = SignupForm()
    return render_template('auth/signup.html', form=form)


@app.route('/signup', methods=['POST'])
def signup():
    form = SignupForm()

    # 入力内容がバリテーションチェックが通ったときの処理
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        uid = uuid.uuid4()
        pw_hash = generate_password_hash(password).decode('utf-8')
        registered_user = User.find_email(email)

        if registered_user:
            flash('既に登録さています')
        else:
            # データベースに登録
            User.create(uid, username, email, pw_hash)
            user = User.get_by_id(uid)
            login_user(user, remember=True)

            # ホーム画面に遷移
            return redirect(url_for('home_view'))
    return render_template('auth/signup.html', form=form)


# ログイン
@app.route('/login', methods=['GET'])
def login_view():
    form = LoginForm()
    return render_template('auth/login.html', form=form)


@app.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.find_username(form.username.data)
        if not user:
            flash('このユーザーは存在しません')
        else:
            if user and check_password_hash(
                            user.password,
                            form.password.data
                            ):
                login_user(user, remember=True)
                return redirect(url_for('home_view'))
        return render_template('auth/login.html', form=form)


# ログアウト
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    # remove the uid from the session if it's there
    logout_user()
    return redirect(url_for('login'))


# ホーム画面
# ルーム(友達)を一覧表示する
@app.route('/home', methods=['GET'])
@login_required
def home_view():
    return render_template('home.html')


# 友達を追加する(友達 == ルーム)
@app.route('/friend/add', methods=['POST'])
@login_required
def add_friend():
    return redirect(url_for('home_view'))


# 友達を削除する(友達 == ルーム)
@app.route('/friend/delete/<int:room_id>', methods=['POST'])
@login_required
def delete_friend():
    return redirect(url_for('home_view'))


# メッセージ画面
# ルーム内のメッセージを一覧表示
@app.route('/room/<int:room_id>/message', methods=['GET'])
@login_required
def messages_view():
    return render_template('messages.html')


# ルーム内でフレンドにメッセージを送信する
@app.route('/room/<int:room_id>/add/message', methods=['POST'])
@login_required
def add_message():
    return redirect(url_for('messages_view'))


# ルーム内でフレンドに送信したメッセージを編集する
@app.route('/messages/edit/<int:message_id>', methods=['POST'])
@login_required
def edit_message():
    return redirect(url_for('messages_view'))


# ルーム内でフレンドに送信したメッセージを削除する
@app.route('/messages/delete/<int:message_id>', methods=['POST'])
@login_required
def delete_message():
    return redirect(url_for('messages_view'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
