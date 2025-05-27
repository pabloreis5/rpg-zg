from flask import Flask, render_template, redirect, url_for, session, request
from random import randint
from monsters import MONSTROS
from functions import executar_rodada, limpar_dados_batalha

app = Flask(__name__)
app.secret_key = 'rpg_secreto_123'

# Rota Principal
@app.route('/')
def index():
    session.clear()
    return render_template('index.html')

@app.route('/reiniciar')
def reiniciar():
    session.clear()
    return redirect(url_for('index'))

@app.route('/regiao1')
def regiao1():
    # Opcional: Passar vida atual para exibir no #boxVida
    vida = session.get("vida_max_personagem", 5)
    return render_template('regiao1.html', vida_atual=vida)

@app.route('/regiao2')
def regiao2():
    vida = session.get("vida_max_personagem", 5)
    return render_template('regiao2.html', vida_atual=vida) 

@app.route("/batalha/<string:monster_id>", methods=["GET", "POST"])
def batalha(monster_id):
    if monster_id not in MONSTROS:
        return "Monstro não encontrado!", 404

    monstro_data = MONSTROS[monster_id]

    if request.method == "GET":
        if "batalha_iniciada" not in session or not session["batalha_iniciada"]:
            session["monster_id"] = monster_id
            session["vida_max_personagem"] = session.get("vida_max_personagem", 5)
            session["vida_personagem"] = session["vida_max_personagem"]
            
            session["vida_monstro"] = monstro_data['vida_inicial']
            session["vida_monstro_inicial"] = monstro_data['vida_inicial']
            session["qtd_sorteios_monstro"] = monstro_data['qtd_sorteios'] 

            session["vida_personagem_inicial"] = session["vida_personagem"]
            session["num_secreto_monstro"] = randint(1, session["vida_monstro_inicial"])
            session["num_secreto_personagem"] = randint(1, session["vida_personagem_inicial"])
    
            session["qtd_sorteios_personagem"] = monstro_data['qtd_sorteios'] 
            
            session["log_batalha"] = []
            session["ultima_rodada"] = []
            session["batalha_iniciada"] = True
            session["itens_conquistados"] = session.get("itens_conquistados", [])

    if request.method == "POST":
        rodada_log = executar_rodada()
        session["ultima_rodada"] = rodada_log
        session["log_batalha"].extend(rodada_log)

        if session["vida_monstro"] <= 0:
            monstro_data = MONSTROS[session['monster_id']]
            session["vida_max_personagem"] = session.get("vida_max_personagem", 5) + 2
            item_ganho = monstro_data['item_nome']
            if item_ganho not in session.get("itens_conquistados", []):
                 session["itens_conquistados"].append(item_ganho)
                 session.modified = True
            session['vitoria_context'] = {
                'item_nome': item_ganho,
                'item_imagem': monstro_data['item_imagem'],
                'proxima_url': monstro_data['proxima_url'],
                'mensagem_vitoria': f"Você derrotou o {monstro_data['nome']}!"
            }
            limpar_dados_batalha()
            return redirect(url_for('vitoria'))

        if session["vida_personagem"] <= 0:
            monstro_data = MONSTROS[session['monster_id']]
            session['derrota_context'] = {
                'mensagem_derrota': f"Você foi derrotado por {monstro_data['nome']}...",
                'tentar_novamente_url': url_for('reiniciar')
            }
            limpar_dados_batalha()
            return redirect(url_for('derrota'))

    return render_template("batalha.html", 
                           vida_personagem=session.get("vida_personagem", 0),
                           vida_monstro=session.get("vida_monstro", 0),
                           nome_monstro=monstro_data['nome'],
                           ultima_rodada=session.get("ultima_rodada", []),
                           imagem_fundo=monstro_data.get('imagem_fundo', 'fundo_padrao.jpg')
                           )

@app.route("/vitoria")
def vitoria():
    context = session.pop('vitoria_context', None) 
    if not context:
        return redirect(url_for('index'))
    vida_atual = session.get("vida_max_personagem", 5)
    return render_template("vitoria.html", context=context, vida_atual=vida_atual)

@app.route("/derrota")
def derrota():
    context = session.pop('derrota_context', None)
    if not context:
        return redirect(url_for('index'))
    return render_template("derrota.html", context=context)

if __name__ == '__main__':
    app.run(debug=True)