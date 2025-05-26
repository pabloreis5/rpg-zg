from flask import Flask, render_template, redirect, url_for, session, request

app = Flask(__name__)
app.secret_key = 'rpg_secreto_123'

#ROTAS
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

@app.route("/batalha1", methods=["GET", "POST"])
def batalha1():
    if request.method == "GET":
        # Sempre reinicia a batalha se não estiver no meio de uma
        if "batalha_iniciada" not in session or not session["batalha_iniciada"]:
            session["vida_personagem"] = 5
            session["vida_monstro"] = 3
            session["num_secreto_monstro"] = randint(1, 3)
            session["num_secreto_personagem"] = randint(1, 5)
            session["qtd_sorteios_personagem"] = 2
            session["qtd_sorteios_monstro"] = 2
            session["log_batalha"] = []
            session["batalha_iniciada"] = True
            # Itens só são resetados se não existem
            session["itens_conquistados"] = session.get("itens_conquistados", [])
            session["item_equipado"] = session.get("item_equipado", None)

    if request.method == "POST":
        rodada_log = executar_rodada()
        session["log_batalha"].extend(rodada_log)

        if session["vida_monstro"] <= 0:
            if "guia_atendimento" not in session["itens_conquistados"]:
                session["itens_conquistados"].append("guia_atendimento")
            session["ultimo_log"] = session["log_batalha"].copy()
            limpar_dados_batalha()
            return redirect("/vitoria1")

        if session["vida_personagem"] <= 0:
            session["ultimo_log"] = session["log_batalha"].copy()
            limpar_dados_batalha()
            return redirect("/derrota")

    return render_template("batalha1.html")


@app.route("/vitoria1")
def vitoria1():
    return "<h1>Vitória!</h1><p>Você derrotou o monstro e ganhou o Guia de Atendimento!</p><a href='/regiao2'>Avançar para Região 2</a>"

@app.route("/derrota")
def derrota():
    return "<h1>Derrota...</h1><p>Sandubinha caiu na batalha.</p><a href='/'>Tentar novamente</a>"



#FUNÇÕES
from random import randint

def executar_rodada():
    log = []

    # --- Ataque de Sandubinha ---
    rodada_log = []
    rodada_log.append("🎲 Rodada - Sandubinha ataca")

    intervalo = session["vida_monstro"]
    num_secreto = session["num_secreto_monstro"]
    qtd = session["qtd_sorteios_personagem"]

    sorteios = [randint(1, intervalo) for _ in range(qtd)]
    acertos = sorteios.count(num_secreto)
    dano = acertos * num_secreto
    session["vida_monstro"] -= dano

    rodada_log.append(f"- Sorteia {qtd} número(s) no intervalo [1-{intervalo}]: {sorteios}")
    rodada_log.append(f"- Número secreto do monstro: {num_secreto}")
    rodada_log.append(f"- Acertos: {acertos}")
    rodada_log.append(f"- Dano causado: {dano}")
    rodada_log.append(f"- Vida restante do monstro: {session['vida_monstro']}")
    log.extend(rodada_log)

    if session["vida_monstro"] <= 0:
        log.append("✅ O monstro foi derrotado!")
        return log

    # --- Ataque do Monstro ---
    rodada_log = []
    rodada_log.append("👹 Rodada - Monstro ataca")

    intervalo_m = session["vida_personagem"]
    num_secreto_m = session["num_secreto_personagem"]
    qtd_m = session["qtd_sorteios_monstro"]

    sorteios_m = [randint(1, intervalo_m) for _ in range(qtd_m)]
    acertos_m = sorteios_m.count(num_secreto_m)
    dano_m = acertos_m * num_secreto_m
    session["vida_personagem"] -= dano_m

    rodada_log.append(f"- Sorteia {qtd_m} número(s) no intervalo [1-{intervalo_m}]: {sorteios_m}")
    rodada_log.append(f"- Número secreto do personagem: {num_secreto_m}")
    rodada_log.append(f"- Acertos: {acertos_m}")
    rodada_log.append(f"- Dano causado: {dano_m}")
    rodada_log.append(f"- Vida restante do personagem: {session['vida_personagem']}")
    log.extend(rodada_log)

    if session["vida_personagem"] <= 0:
        log.append("💀 Sandubinha foi derrotado...")
        

    return log

def limpar_dados_batalha():
    for chave in [
        "vida_personagem",
        "vida_monstro",
        "num_secreto_personagem",
        "num_secreto_monstro",
        "qtd_sorteios_personagem",
        "qtd_sorteios_monstro",
        "log_batalha",
        "batalha_iniciada"
    ]:
        session.pop(chave, None)




if __name__ == '__main__':
    app.run(debug=True)
    
    
