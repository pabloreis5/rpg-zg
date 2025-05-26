MONSTROS = {
    'processus': {
        'id': 'processus', # ID único para a rota/lógica
        'nome': 'Processus ministerii',
        'vida_inicial': 3,
        'qtd_sorteios': 1, 
        'item_nome': 'Guia de atendimento',
        'item_imagem': '../imagens/item1_guia', 
        'proxima_url': '/regiao2'
    },
    'urso': {
        'id': 'urso',
        'nome': 'Urso Sangrento',
        'vida_inicial': 6,
        'qtd_sorteios': 2,
        'item_nome': 'Faturamentus',
        'item_imagem': 'faturamentus.png', # Você precisará criar essa imagem
        'proxima_url': '/regiao3'
    },
    'dragao': {
        'id': 'dragao',
        'nome': 'Dragão da transmissão',
        'vida_inicial': 12,
        'qtd_sorteios': 3,
        'item_nome': 'Azah Transmissão',
        'item_imagem': 'azah_transmissao.png', # Você precisará criar essa imagem
        'proxima_url': '/regiao4' 
    },
    'estatua': {
        'id': 'estatua',
        'nome': 'Estátua do último herói',
        'vida_inicial': 25,
        'qtd_sorteios': 5,
        'item_nome': 'Colar da estátua sagrada',
        'item_imagem': 'colar_estatua.png', # Você precisará criar essa imagem
        'proxima_url': '/regiao5' 
    },
    'glozium': {
        'id': 'glozium',
        'nome': 'Glozium',
        'vida_inicial': 100,
        'qtd_sorteios': 10,
        'item_nome': 'A PAZ FOI RESTAURADA', # Ou o que fizer sentido na vitória final
        'item_imagem': 'espada_zg.png', # Ou uma imagem de vitória
        'proxima_url': '/final_jogo' 
    }
}