from flask import Flask, render_template, redirect, url_for, session, request
from random import randint
from monsters import MONSTROS


app = Flask(__name__)
app.secret_key = 'rpg_secreto_123'

# ROTAS
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
        # Inicia batalha se não estiver em andamento
        if "batalha_iniciada" not in session or not session["batalha_iniciada"]:
            # --- AJUSTE: Usar vida máxima/base e guardar vida inicial ---
            session["vida_max_personagem"] = session.get("vida_max_personagem", 5) # Começa com 5, aumenta com vitórias
            session["vida_personagem"] = session["vida_max_personagem"]
            session["vida_monstro"] = 3 # Vida do monstro para esta batalha
            
            session["vida_personagem_inicial"] = session["vida_personagem"] # Guarda a vida inicial para os intervalos
            session["vida_monstro_inicial"] = session["vida_monstro"] # Guarda a vida inicial para os intervalos

            # --- AJUSTE: Sortear número secreto com base na vida inicial ---
            session["num_secreto_monstro"] = randint(1, session["vida_monstro_inicial"])
            session["num_secreto_personagem"] = randint(1, session["vida_personagem_inicial"])

            session["qtd_sorteios_personagem"] = 2 # Quantidade de sorteios (pode variar por batalha/item)
            session["qtd_sorteios_monstro"] = 2 # Quantidade de sorteios (pode variar por batalha/item)
            
            session["log_batalha"] = []
            session["ultima_rodada"] = []
            session["batalha_iniciada"] = True
            session["itens_conquistados"] = session.get("itens_conquistados", [])
            session["item_equipado"] = session.get("item_equipado", None)

    if request.method == "POST":
        rodada_log = executar_rodada()
        session["ultima_rodada"] = rodada_log  # salva apenas a rodada atual
        session["log_batalha"].extend(rodada_log)  # mantém o log completo internamente

        if session["vida_monstro"] <= 0:
            # --- AJUSTE: Aumentar vida máxima ao vencer ---
            session["vida_max_personagem"] = session.get("vida_max_personagem", 5) + 2

            if "guia_atendimento" not in session["itens_conquistados"]:
                session["itens_conquistados"].append("guia_atendimento")
            session["ultimo_log"] = session["log_batalha"].copy()
            limpar_dados_batalha()
            return redirect("/vitoria1")

        if session["vida_personagem"] <= 0:
            session["ultimo_log"] = session["log_batalha"].copy()
            limpar_dados_batalha()
            return redirect("/derrota")

    return render_template("batalha1.html",
                           vida_personagem=session.get("vida_personagem", 0),
                           vida_monstro=session.get("vida_monstro", 0),
                           ultima_rodada=session.get("ultima_rodada", [])
                           )

@app.route("/vitoria1")
def vitoria1():
    # --- AJUSTE: Informar sobre o aumento de vida na mensagem de vitória (opcional) ---
    vida_atual = session.get("vida_max_personagem", 5)
    return f"<h1>Vitória!</h1><p>Você derrotou o monstro e ganhou o Guia de Atendimento!</p><p>Sua vida máxima aumentou para {vida_atual}!</p><a href='/regiao2'>Avançar para Região 2</a>" # Supondo que /regiao2 exista

@app.route("/derrota")
def derrota():
    return "<h1>Derrota...</h1><p>Sandubinha caiu na batalha.</p><a href='/'>Tentar novamente</a>"

# FUNÇÕES
def executar_rodada():
    log = []

    # --- Ataque de Sandubinha ---
    rodada_log = []
    rodada_log.append("🎲 Rodada - Sandubinha ataca")

    # --- AJUSTE: Usar vida inicial para o intervalo ---
    intervalo = session["vida_monstro_inicial"] 
    num_secreto = session["num_secreto_monstro"]
    qtd = session["qtd_sorteios_personagem"]

    sorteios = [randint(1, intervalo) for _ in range(qtd)]
    acertos = sorteios.count(num_secreto)
    dano = acertos * num_secreto
    session["vida_monstro"] = max(0, session["vida_monstro"] - dano) # Garante que a vida não fique negativa

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

    # --- AJUSTE: Usar vida inicial para o intervalo ---
    intervalo_m = session["vida_personagem_inicial"] 
    num_secreto_m = session["num_secreto_personagem"]
    qtd_m = session["qtd_sorteios_monstro"]

    sorteios_m = [randint(1, intervalo_m) for _ in range(qtd_m)]
    acertos_m = sorteios_m.count(num_secreto_m)
    dano_m = acertos_m * num_secreto_m
    session["vida_personagem"] = max(0, session["vida_personagem"] - dano_m) # Garante que a vida não fique negativa

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
    # Limpa apenas os dados específicos da batalha atual.
    # Preserva 'vida_max_personagem', 'itens_conquistados', etc.
    for chave in [
        "vida_personagem",
        "vida_monstro",
        "num_secreto_personagem",
        "num_secreto_monstro",
        "qtd_sorteios_personagem",
        "qtd_sorteios_monstro",
        "log_batalha",
        "ultima_rodada",
        "batalha_iniciada",
        "vida_personagem_inicial", # Limpa os valores iniciais da batalha encerrada
        "vida_monstro_inicial"
    ]:
        session.pop(chave, None)

if __name__ == '__main__':
    app.run(debug=True)