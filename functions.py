from flask import session
from random import randint

def executar_rodada():
    log = []

    # --- Ataque de Sandubinha ---
    rodada_log = []
    rodada_log.append("🎲 Rodada - Sandubinha ataca")

    intervalo = session["vida_monstro_inicial"] 
    num_secreto = session["num_secreto_monstro"]
    qtd = session["qtd_sorteios_personagem"]

    sorteios = [randint(1, intervalo) for _ in range(qtd)] 
    acertos = sorteios.count(num_secreto)
    dano = acertos * num_secreto
    session["vida_monstro"] = max(0, session["vida_monstro"] - dano)

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

    intervalo_m = session["vida_personagem_inicial"] 
    num_secreto_m = session["num_secreto_personagem"]
    qtd_m = session["qtd_sorteios_monstro"] 

    sorteios_m = [randint(1, intervalo_m) for _ in range(qtd_m)]
    acertos_m = sorteios_m.count(num_secreto_m)
    dano_m = acertos_m * num_secreto_m
    session["vida_personagem"] = max(0, session["vida_personagem"] - dano_m) 

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
        "vida_personagem", "vida_monstro", "num_secreto_personagem",
        "num_secreto_monstro", "qtd_sorteios_personagem", "qtd_sorteios_monstro",
        "log_batalha", "ultima_rodada", "batalha_iniciada",
        "vida_personagem_inicial", "vida_monstro_inicial", "monster_id"
    ]:
        session.pop(chave, None)