from flask import Flask, request, session, abort, render_template, redirect, url_for
import logging
import datetime
import qrcode
import ds
import account


app = Flask(__name__)
logging.getLogger().setLevel(logging.DEBUG)
app.secret_key = 'm9XE4JH5dBOQK4o4'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')


@app.route('/works/myprpage')
def myprpage():
    return render_template('works/myprpage.html')


@app.route('/works/mygoalpage')
def mygoalpage():
    return render_template('works/mygoalpage.html')


@app.route('/works/imagelayout')
def imagelayout():
    return render_template('works/imagelayout.html')


# ----- QRコード生成ページ -----
@app.route('/works/qrcoder')
def qrcoder():
    return render_template('works/qrcoder.html', qrcodeimage='/static/images/blank.gif')

@app.route('/works/qrcc', methods=['POST'])
def qrcc():
    # 生成するQRcodeの詳細設定
    qr = qrcode.QRCode(
        box_size=4,
        border=8,
        version=12,
        error_correction=qrcode.constants.ERROR_CORRECT_Q
    )
    # フォームのテキストを取得
    urlqr = request.form.get('urlqr', '')
    if urlqr == '':
        return show_msg('URLを入力してから生成ボタンを押してください')
    # 描画するデータを指定する
    qr.add_data(urlqr)
    # QRコードの元データを作る
    qr.make()
    # データをImageオブジェクトとして取得
    img = qr.make_image()
    # Imageをファイルに保存
    imgurl = 'static/images/qrcode.png'
    img.save(imgurl)
    # 現在日時を取得
    ctime = str(datetime.datetime.now())
    # キャッシュの画像が表示されないようにパスの後ろに日時を追加
    return render_template('works/qrcoder.html', qrcodeimage=('/' + imgurl + '?' + ctime))
# ---------------


# ----- ToDoListApp -----
# ----- 通常ページ -----
@app.route('/works/todo')
def todo():
    data = ds.get_all()
    message = "ToDoList にようこそ！"
    return render_template('works/todo.html',
                    message=message,
                    data=data)

@app.route('/works/todo/check/<key_id>', methods=['POST'])
def check(key_id=None):
    entity = ds.get_by_id(key_id)
    if not entity:
        abort(404)
    entity['check'] = "1"
    ds.update(entity)
    return redirect('/works/todo')
# ---------------


# ----- ログインページ -----
@app.route('/works/todo/login')
def login():
    # 既にログインしていれば管理画面へ
    if is_login():
        return redirect('/works/todo/admin')
    return render_template('works/todo_login.html')

@app.route('/works/todo/check_login', methods=['POST'])
def check_login():
    # フォームの値の取得
    name, pw = (None, None)
    if 'name' in request.form:
        name = request.form['name']
    if 'pw' in request.form:
        pw = request.form['pw']
    if (name is None) or (pw is None):
        return redirect('/works/todo')
    # ログインチェック
    if try_login(name, pw) == False:
        return """
        <h1>ユーザー名かパスワードが間違っています</h1>
        <p><a href="/works/todo/login">ログインフォームに戻る</a></p>
        """
    # 管理ページにリダイレクト
    return redirect('/works/todo/admin')

# ログイン処理を行う
def try_login(name, pw):
    data = account.get_all()
    # ユーザー名があっているかチェック
    if data[0]['name'] != name:
        return False
    # パスワードがあっているかチェック
    if data[0]['pw'] != pw:
        return False
    # ログイン処理を実行
    session['login'] = name
    return True

# ログインしているかチェック
def is_login():
    if 'login' in session:
        return True
    return False
# ---------------


# ----- 管理者ページ -----
@app.route('/works/todo/admin')
def admin():
    # ログインしていなければトップへリダイレクト
    if not is_login():
        return """
        <h1>ログインしてください</h1>
        <p><a href="/works/todo/login">ログインする</a></p>
        """
    data = ds.get_all()
    message = "ToDoList 管理画面"
    return render_template('works/todo_admin.html',
                    message=message,
                    data=data)

@app.route('/works/todo/add', methods=['PUT'])
def add():
    # ログインしていなければトップへリダイレクト
    if not is_login():
        return """
        <h1>ログインしてください</h1>
        <p><a href="/works/todo/login">ログインする</a></p>
        """
    addtodo = request.form.get('addtodo', '')
    if addtodo == '':
        return redirect('/works/todo/admin')
    things = addtodo
    check = "0"
    ds.insert(things, check)
    return redirect('/works/todo/admin')

@app.route('/works/todo/delete/<key_id>', methods=['DELETE'])
def delete(key_id=None):
    # ログインしていなければトップへリダイレクト
    if not is_login():
        return """
        <h1>ログインしてください</h1>
        <p><a href="/works/todo/login">ログインする</a></p>
        """
    ds.delete(key_id)
    return redirect('/works/todo/admin')

@app.route('/works/todo/logout')
def logout_page():
    # ログアウト処理の実行
    try_logout()
    return """
    <h1>ログアウトしました</h1>
    <p><a href="/works/todo">ToDoリストに戻る</a></p>
    """

# ログアウトする
def try_logout():
    session.pop('login', None)
    return True
# ---------------



def show_msg(msg):
    return render_template('msg.html', msg=msg)


@app.errorhandler(404)
def error_404(exception):
    logging.exception(exception)
    return render_template('404.html'), 404



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)