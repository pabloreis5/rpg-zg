ITENS = {
    'guia_atendimento': {
        'id': 'guia_atendimento',
        'nome': 'Guia de Atendimento',
        'descricao': 'Fortifica o personagem, +2 números por ataque.',
        'imagem': 'item1_guia.png',
        'beneficio': {'tipo': 'sorteios_adicionais', 'valor': 2},
        'consequencia': None,
        'custo_uso': None
    },
    'faturamentus': {
        'id': 'faturamentus',
        'nome': 'Faturamentus',
        'descricao': '+4 números, mas se errar, próximo ataque do monstro +2 dano.',
        'imagem': '../imagens/item2_placa',
        'beneficio': {'tipo': 'sorteios_adicionais', 'valor': 4},
        'consequencia': {'gatilho': 'erro', 'efeito': 'bonus_dano_monstro', 'valor': 2},
        'custo_uso': None
    },
    'azah_transmissao': {
        'id': 'azah_transmissao',
        'nome': 'Azah Transmissão',
        'descricao': '+10 números. Se errar, próximo dano = (vidaAtual - NumSorteado).',
        'imagem': 'azah_transmissao.png',
        'beneficio': {'tipo': 'sorteios_adicionais', 'valor': 10},
        'consequencia': {'gatilho': 'erro', 'efeito': 'dano_especial_proximo', 'valor': None},
        'custo_uso': None
    },
    'colar_estatua': {
        'id': 'colar_estatua',
        'nome': 'Colar da estátua sagrada',
        'descricao': '+10 números, mas custa 3 de vida por uso.',
        'imagem': 'colar_estatua.png',
        'beneficio': {'tipo': 'sorteios_adicionais', 'valor': 10},
        'consequencia': None,
        'custo_uso': {'tipo': 'vida', 'valor': 3}
    },
}