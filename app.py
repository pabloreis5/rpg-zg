from flask import Flask, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'rpg_secreto_123'  # Necessário para usar session

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/regiao')
def regiao():
    return "<h2>Você iniciou um novo jogo! (região ainda não implementada)</h2>"

@app.route('/continuar')
def continuar():
    # Exemplo simples: se não houver progresso salvo, redireciona pro início
    if 'personagem' not in session:
        return redirect(url_for('index'))
    return "<h2>Carregando jogo salvo... (lógica de continuar ainda será implementada)</h2>"

@app.route('/reiniciar')
def reiniciar():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
