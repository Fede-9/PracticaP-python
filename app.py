# Primera parte

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    color_buttom = 'success'
    return render_template('index.html')

@app.route("/info")
def info():
    return render_template('info.html')



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)



