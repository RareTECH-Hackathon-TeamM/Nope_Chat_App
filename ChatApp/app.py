from flask import (
        Flask,
        redirect,
        url_for,
        render_template,
        request,
        flash,
        send_file
        )
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
from forms import (SignupForm,
                   LoginForm,
                   SearchForm,
                   MessageForm
                   )
import io
from models import User, Room, Message
from nanoid import generate
import os
import qrcode
import uuid

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
    # print(f'[load_user] uid: {uid}')
    user = User.get_by_id(uid)
    # print(f'[load_user] user: {user}')
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
            if check_password_hash(
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
    form = SearchForm()
    uid = current_user.get_id()
    rooms = Room.get_all_friends(uid)
    return render_template('home.html',
                           form=form,
                           rooms=rooms
                           )


# 既存のルームの絞込検索
@app.route('/home', methods=['POST'])
@login_required
def home():
    pass


# 友達を追加する
@app.route('/room/add', methods=['POST'])
@login_required
def add_friend():
    uid = current_user.get_id()
    room_id = generate(size=10)
    Room.add_room(uid, room_id)
    return redirect(url_for('invite_sender_view', room_id=room_id))


# QRコードを表示する画面に遷移
@app.route('/invite/sender/<room_id>', methods=['GET'])
@login_required
def invite_sender_view(room_id):
    return render_template('invite_sender.html', room_id=room_id)


# QRコード読み取り後遷移する画面
@app.route('/invite/receiver/<room_id>', methods=['GET'])
@login_required
def invite_receiver_view(room_id):
    return render_template('invite_receiver.html', room_id=room_id)


# 友達追加したときの処理
@app.route('/invite/receiver/<room_id>', methods=['POST'])
@login_required
def invite_receiver(room_id):
    uid = current_user.get_id()
    Room.add_friend(uid, room_id)
    return redirect(url_for('home_view'))


# QRコードを返す
@app.route('/invite/qrcode/<room_id>')
@login_required
def invite_qrcode(room_id):
    invite_url = url_for(
            'invite_receiver_view',
            room_id=room_id,
            _external=True
            )
    qr = qrcode.make(invite_url)
    buf = io.BytesIO()
    qr.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')


# ルームを論理削除
@app.route('/room/delete/<room_id>', methods=['POST'])
@login_required
def delete_room(room_id):
    Room.delete_room(room_id)
    return redirect(url_for('home_view'))


# メッセージ画面
# メッセージ一覧表示
@app.route('/room/<room_id>/messages', methods=['GET'])
@login_required
def messages_view(room_id):
    form = MessageForm()
    uid = current_user.get_id()
    messages = Message.get_all_messages(uid, room_id)
    latest_message = Message.latest_message(room_id)
    print(latest_message)
    return render_template(
            'messages.html',
            form=form,
            room_id=room_id,
            messages=messages,
            uid=uid,
            latest_message=latest_message
            )


# メッセージ送信
@app.route('/room/<room_id>/add/message', methods=['POST'])
@login_required
def add_message(room_id):
    form = MessageForm()

    # 入力内容がバリテーションチェックが通ったときの処理
    if form.validate_on_submit():
        uid = current_user.get_id()
        latest_message = Message.latest_message(room_id)
        if latest_message.get('uid') != uid:
            message_id = generate()
            message = form.message.data
            Message.add_message(message_id, uid, room_id, message)
            return redirect(url_for('messages_view', room_id=room_id))
    return redirect(url_for('messages_view', room_id=room_id, form=form))


# メッセージ編集
@app.route('/room/<room_id>/message/edit/<message_id>', methods=['POST'])
@login_required
def edit_message(room_id, message_id):
    form = MessageForm()
    uid = current_user.get_id()
    latest_message = Message.latest_message(room_id)
    if latest_message.get('uid') == uid:
        edit_message = request.form.get('edit_message')
        Message.edit_message(message_id, edit_message)
        return redirect(url_for('messages_view', room_id=room_id, form=form))
    return redirect(url_for('messages_view', room_id=room_id, form=form))


# ルーム内でフレンドに送信したメッセージを削除する
@app.route('/message/delete/<message_id>', methods=['POST'])
@login_required
def delete_message():
    return redirect(url_for('messages_view'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
