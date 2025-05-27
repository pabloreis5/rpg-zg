# RPG ZG - A Aventura de Sandubinha

<img src="./static/imagens/logo.jpg" alt="Logo RPG ZG" width="100">

## 📜 Sobre o Jogo

RPG ZG é uma aventura épica baseada na web, onde você assume o papel de Sandubinha, um herói improvável com cabeça de hambúrguer, em uma missão para derrotar o temível Glozium. Viaje por terras místicas, enfrente monstros bizarros e colete artefatos sagrados para forjar a lendária Espada ZG e restaurar a paz no mundo.

Este projeto foi desenvolvido usando Python com o framework Flask, apresentando uma mecânica de batalha por turnos única e uma narrativa envolvente distribuída por várias regiões.

## ✨ Funcionalidades

* **Interface Web:** Jogue diretamente no seu navegador.
* **Narrativa Progressiva:** Acompanhe a jornada de Sandubinha através de 5 regiões distintas.
* **Batalhas por Turnos:** Enfrente monstros com um sistema de combate estratégico.
* **Mecânica de "Número Secreto":** Uma forma única de determinar o dano em batalha.
* **Progressão do Personagem:** Aumente a vida máxima de Sandubinha a cada vitória.
* **Coleta de Itens:** Reúna artefatos para forjar a arma final.
* **Sistema de Sessão:** Seu progresso (vida, itens) é salvo entre as batalhas usando sessões Flask.
* **Design Responsivo (Básico):** Adapta-se a diferentes tamanhos de tela.

## ⚔️ Mecânica de Batalha

O coração do RPG ZG é seu sistema de batalha:

1.  **Atributos:** Tanto o personagem quanto o monstro possuem "Pontos de Vida" e um "Número Secreto" sorteado no início da batalha.
2.  **Sorteios:** A cada rodada, ambos (personagem e monstro) sorteiam uma quantidade definida de números. Essa quantidade é a mesma para ambos em uma dada batalha e varia de acordo com o monstro enfrentado.
3.  **Intervalo:** Os números são sorteados dentro do intervalo `[1, Vida_Inicial_do_Oponente]`.
4.  **Dano:** Se um número sorteado for igual ao "Número Secreto" do oponente, um acerto é registrado. O dano causado é igual ao `Número_Secreto * Quantidade_de_Acertos`.
5.  **Vitória/Derrota:** A batalha termina quando a vida de um dos combatentes chega a 0. Ao vencer, Sandubinha ganha 2 pontos de vida máxima e um artefato.

## 💻 Tecnologias Utilizadas

* **Backend:** Python
* **Framework Web:** Flask
* **Servidor (Sugestão):** Gunicorn
* **Frontend:** HTML5, CSS3
* **Interatividade (Básica):** JavaScript

## 🚀 Como Instalar e Rodar

1.  **Clone o Repositório:**
    ```bash
    git clone <url-do-seu-repositorio>
    cd rpg-zg
    ```

2.  **Crie e Ative um Ambiente Virtual (Recomendado):**
    ```bash
    python -m venv venv
    # No Windows:
    .\venv\Scripts\activate
    # No Linux/macOS:
    source venv/bin/activate
    ```

3.  **Instale as Dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute a Aplicação:**
    ```bash
    python app.py
    ```
    Ou, para um ambiente mais robusto (se Gunicorn estiver instalado):
    ```bash
    gunicorn app:app
    ```

5.  **Acesse no Navegador:** Abra seu navegador e acesse `http://127.0.0.1:5000/`.

## 🎮 Como Jogar

1.  Acesse a URL do jogo.
2.  Clique em "Jogar" na tela inicial.
3.  Você será levado para a primeira região. Leia a história ou clique em "[skip]" para avançar os diálogos.
4.  Quando o botão "Batalhar" aparecer, clique nele para iniciar o combate.
5.  Na tela de batalha, clique em "Avançar Rodada" para executar um turno.
6.  Continue até vencer ou ser derrotado.
7.  Se vencer, você irá para a tela de vitória, ganhará um item e poderá avançar para a próxima região.
8.  Se perder, você terá a opção de tentar novamente (reiniciando o jogo).
9.  O botão "Novo Jogo" ou "Desistir" reinicia completamente o jogo.

---

Divirta-se na jornada épica de Sandubinha!

