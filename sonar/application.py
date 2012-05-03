import os
from flask import Flask, g, session
from flask import render_template, redirect, url_for, request

app = Flask(__name__)
app.debug = True
app.config.update(
    SECRET_KEY = '=\xce\xc4\xd1Ud\xd3\xd4\xa8M\xf0\x17\x98^H)=\xb7d:\xa2wco',
    DEBUG = True
)

@app.route('/')
def sonar():
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

