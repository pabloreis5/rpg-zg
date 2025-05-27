# Em functions.py

from flask import session
from random import randint
from items import ITENS  # <-- ADICIONAR IMPORTAÇÃO

def executar_rodada():
    log = []
    item_ativo_id = session.get('item_ativo')
    item = ITENS.get(item_ativo_id) if item_ativo_id else None
    efeitos_proxima_rodada = session.pop('efeitos_proxima_rodada', {}) # Pega e limpa efeitos

    # --- Aplica Custos/Efeitos Iniciais ---
    if item and item.get('custo_uso'):
        custo = item['custo_uso']
        if custo['tipo'] == 'vida':
            session["vida_personagem"] -= custo['valor']
            log.append(f"🩸 Custo de {item['nome']}: -{custo['valor']} de vida.")
            if session["vida_personagem"] <= 0:
                log.append("💀 Sandubinha foi derrotado pelo custo do item...")
                return log

    # --- Ataque de Sandubinha ---
    rodada_log = ["🎲 Rodada - Sandubinha ataca"]
    intervalo = session["vida_monstro_inicial"]
    num_secreto = session["num_secreto_monstro"]
    qtd = session["qtd_sorteios_personagem"]

    if item:
        rodada_log.append(f"✨ Usando: {item['nome']}")
        if item.get('beneficio', {}).get('tipo') == 'sorteios_adicionais':
            qtd += item['beneficio']['valor']
            rodada_log.append(f"   -> Bônus: +{item['beneficio']['valor']} sorteios!")

    sorteios = [randint(1, intervalo) for _ in range(qtd)]
    acertos = sorteios.count(num_secreto)
    errou = acertos == 0
    dano = acertos * num_secreto
    session["vida_monstro"] = max(0, session["vida_monstro"] - dano)

    rodada_log.append(f"- Sorteia {qtd} número(s) no intervalo [1-{intervalo}]: {sorteios}")
    rodada_log.append(f"- Número secreto do monstro: {num_secreto}")
    rodada_log.append(f"- Acertos: {acertos}")
    rodada_log.append(f"- Dano causado: {dano}")
    rodada_log.append(f"- Vida restante do monstro: {session['vida_monstro']}")

    # Aplica consequências de erro
    if errou and item and item.get('consequencia') and item['consequencia']['gatilho'] == 'erro':
        efeito = item['consequencia']
        if efeito['efeito'] == 'bonus_dano_monstro':
            efeitos_proxima_rodada['bonus_dano_monstro'] = efeito['valor']
            rodada_log.append(f"   -> ⚠️ Errou! Próximo ataque do monstro terá +{efeito['valor']} dano.")
        # Adicionar outras consequências de erro aqui...

    log.extend(rodada_log)

    if session["vida_monstro"] <= 0:
        log.append("✅ O monstro foi derrotado!")
        session.pop('item_ativo', None) # Limpa item ao fim da batalha
        session.pop('efeitos_proxima_rodada', None)
        return log

    # --- Ataque do Monstro ---
    rodada_log = ["👹 Rodada - Monstro ataca"]
    intervalo_m = session["vida_personagem_inicial"]
    num_secreto_m = session["num_secreto_personagem"]
    qtd_m = session["qtd_sorteios_monstro"]
    sorteios_m = [randint(1, intervalo_m) for _ in range(qtd_m)]
    acertos_m = sorteios_m.count(num_secreto_m)
    dano_m = acertos_m * num_secreto_m

    # Aplica bônus de dano de efeitos anteriores
    if 'bonus_dano_monstro' in efeitos_proxima_rodada:
        dano_m += efeitos_proxima_rodada['bonus_dano_monstro']
        rodada_log.append(f"   -> ⚠️ Efeito de item: Monstro causa +{efeitos_proxima_rodada['bonus_dano_monstro']} dano!")

    session["vida_personagem"] = max(0, session["vida_personagem"] - dano_m)

    rodada_log.append(f"- Sorteia {qtd_m} número(s) no intervalo [1-{intervalo_m}]: {sorteios_m}")
    rodada_log.append(f"- Número secreto do personagem: {num_secreto_m}")
    rodada_log.append(f"- Acertos: {acertos_m}")
    rodada_log.append(f"- Dano causado: {dano_m}")
    rodada_log.append(f"- Vida restante do personagem: {session['vida_personagem']}")
    log.extend(rodada_log)

    if session["vida_personagem"] <= 0:
        log.append("💀 Sandubinha foi derrotado...")
        session.pop('item_ativo', None) # Limpa item ao fim da batalha
        session.pop('efeitos_proxima_rodada', None)

    # Salva efeitos para a próxima rodada, se houver
    if efeitos_proxima_rodada:
         session['efeitos_proxima_rodada'] = efeitos_proxima_rodada

    # Limpa o item ativo para forçar a seleção na próxima rodada
    # session.pop('item_ativo', None) # DESCOMENTE se quiser que o item seja escolhido a CADA rodada

    return log

def limpar_dados_batalha():
    chaves_para_limpar = [
        "vida_personagem", "vida_monstro", "num_secreto_personagem",
        "num_secreto_monstro", "qtd_sorteios_personagem", "qtd_sorteios_monstro",
        "log_batalha", "ultima_rodada", "batalha_iniciada",
        "vida_personagem_inicial", "vida_monstro_inicial", "monster_id",
        "item_ativo", "efeitos_proxima_rodada" # <-- ADICIONAR
    ]
    for chave in chaves_para_limpar:
        session.pop(chave, None)