from flask import Flask, request, session, abort, render_template, redirect, url_for
from google.cloud import storage
from PIL import Image
import tempfile
import logging
import datetime
import qrcode
import ds
import account
import ws


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

    # 一時ファイルを作成
    tmpdir = tempfile.TemporaryDirectory()
    # 一時ファイルのパスを指定
    imgurl = tmpdir.name + '/qrcode.png'
    # 一時ファイルに保存
    img.save(imgurl)

    # storage clientオブジェクトの作成
    client = storage.Client()
    # バケットの指定
    bucket = client.get_bucket('hama28-portfolio')
    # ファイル名の指定
    blob = bucket.blob('qrcode.png')
    # 一時ファイルに保存したファイルをアップロード
    with open(imgurl, 'rb') as photo:
        blob.upload_from_file(photo)
    # 一時ファイルの削除
    tmpdir.cleanup()
    # 画像が保存されるStorageのURL
    qrimg = 'https://storage.googleapis.com/hama28-portfolio/qrcode.png'
    # 現在日時を取得
    ctime = str(datetime.datetime.now())

    # キャッシュの画像が表示されないようにパスの後ろに日時を追加
    return render_template('works/qrcoder.html', qrcodeimage=(qrimg + '?' + ctime))
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
    if entity['check'] == "0":
        entity['check'] = "1"
    elif entity['check'] == "1":
        entity['check'] = "0"
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
        return show_msg("ユーザー名かパスワードが間違っています")
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
        return show_msg("認証失敗。ログインが必要なページです。")
    data = ds.get_all()
    message = "ToDoList 管理画面"
    return render_template('works/todo_admin.html',
                    message=message,
                    data=data)

@app.route('/works/todo/add', methods=['POST'])
def add():
    # ログインしていなければトップへリダイレクト
    if not is_login():
        return show_msg("認証失敗。ログインが必要なページです。")
    addtodo = request.form.get('addtodo', '')
    if addtodo == '':
        return redirect('/works/todo/admin')
    things = addtodo
    check = "0"
    ds.insert(things, check)
    return redirect('/works/todo/admin')

@app.route('/works/todo/edit_form/<key_id>', methods=['POST'])
def edit_form(key_id=None):
    # ログインしていなければトップへリダイレクト
    if not is_login():
        return show_msg("認証失敗。ログインが必要なページです。")
    entity = ds.get_by_id(key_id)
    if not entity:
        abort(404)
    key_id = entity['id']
    thing = entity['things']
    return render_template('works/todo_edit.html', key_id=key_id, thing=thing)

@app.route('/works/todo/edit/<key_id>', methods=['POST'])
def edit(key_id=None):
    # ログインしていなければトップへリダイレクト
    if not is_login():
        return show_msg("認証失敗。ログインが必要なページです。")
    entity = ds.get_by_id(key_id)
    if not entity:
        abort(404)
    addtodo = request.form.get('addtodo', '')
    if addtodo == '':
        return redirect('/works/todo/admin')
    entity['things'] = addtodo
    entity = ds.update(entity)
    return redirect('/works/todo/admin')


@app.route('/works/todo/delete/<key_id>', methods=['POST'])
def delete(key_id=None):
    # ログインしていなければトップへリダイレクト
    if not is_login():
        return show_msg("認証失敗。ログインが必要なページです。")
    ds.delete(key_id)
    return redirect('/works/todo/admin')

@app.route('/works/todo/logout')
def logout_page():
    # ログアウト処理の実行
    try_logout()
    return show_msg("ログアウトしました")

# ログアウトする
def try_logout():
    session.pop('login', None)
    return True
# ---------------



# ----- スクレイピング -----
@app.route('/works/ws_top')
def ws_top():
    return render_template('works/ws_top.html')

@app.route('/works/ws_start', methods=['POST'])
def ws_start():
    web_array = []
    target = request.form['target']
    users = request.form['users']

    if target == 'はてなブックマーク':
        web_array = ws.get_hatebu(users)
    
    # 親データを追加、親データのkey_idを取得
    parent_id = ws.insert(target, users)
    # 親データに紐付けて子データを追加
    ws.insert_descendant(parent_id, web_array)

    return redirect('/works/ws_get_list')

@app.route('/works/ws_get_list')
def ws_get_list():
    data = ws.get_all()
    return render_template('works/ws_get_list.html', data=data)

@app.route('/works/ws_data/<key_id>', methods=['POST'])
def ws_data(key_id=None):
    entities = ws.get_data(key_id)
    return render_template('works/ws_data.html', entities=entities)
# ---------------


# ---------------
@app.route('/works/microbit')
def microbit():
    return render_template('works/microbit.html')
# ---------------


def show_msg(msg):
    return render_template('msg.html', msg=msg)


@app.errorhandler(404)
def error_404(exception):
    logging.exception(exception)
    return render_template('404.html'), 404


@app.errorhandler(500)
def error_500(exception):
    logging.exception(exception)
    return render_template('500.html'), 500



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)