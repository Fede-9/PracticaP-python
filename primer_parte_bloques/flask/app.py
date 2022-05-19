from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    color_button = 'success'
    return render_template(
        'index.html',
        color = color_button
    )

@app.route("/info")
def info():
    color_button = 'warning'
    return render_template(
        'info.html',
        color = color_button
        )


if __name__ == '__main__':
    app.run(host="0.0.0.0")