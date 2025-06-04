from flask import Flask, render_template

from app1 import register_dailymotion_routes
from app2 import register_facebook_routes
from app3 import register_instagram_routes
from app4 import register_pinterest_routes
from app5 import register_reddit_routes
from app6 import register_tiktok_routes
from app7 import register_twitch_routes
from app8 import register_twitter_routes
from app9 import register_youtube_routes

app = Flask(__name__, template_folder='templates')

# Register blueprints from all downloader apps
register_dailymotion_routes(app)
register_facebook_routes(app)
register_instagram_routes(app)
register_pinterest_routes(app)
register_reddit_routes(app)
register_tiktok_routes(app)
register_twitch_routes(app)
register_twitter_routes(app)
register_youtube_routes(app)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/dailymotion')
def dailymotion():
    return render_template('index1.html')


@app.route('/facebook')
def facebook():
    return render_template('index2.html')


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
