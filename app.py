from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/instagram')
def instagram():
    return render_template('index3.html')


@app.route('/pinterest')
def pinterest():
    return render_template('index4.html')


@app.route('/reddit')
def reddit():
    return render_template('index5.html')


@app.route('/tiktok')
def tiktok():
    return render_template('index6.html')


@app.route('/twitch')
def twitch():
    return render_template('index7.html')


@app.route('/twitter')
def twitter():
    return render_template('index8.html')


@app.route('/youtube')
def youtube():
    return render_template('index9.html')


if __name__ == '__main__':
    app.run(debug=True)
