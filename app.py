from flask import Flask, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'rpg_secreto_123'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/regiao1')
def regiao1():
    return render_template('regiao1.html')


@app.route('/reiniciar')
def reiniciar():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
