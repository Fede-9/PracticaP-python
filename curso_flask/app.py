from flask import Flask,  render_template, redirect, url_for, request


app = Flask(__name__)


@app.route('/')
def home():
    return 'holaaaaa'

if __name__ == '__main__':
    app.run(host="0.0.0.0")



