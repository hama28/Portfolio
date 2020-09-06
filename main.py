from flask import Flask, render_template
from flask import request, url_for, redirect
import datetime
import qrcode


app = Flask(__name__)


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



def show_msg(msg):
    return render_template('msg.html', msg=msg)



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)