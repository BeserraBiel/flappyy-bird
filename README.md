# 🐦 Flappy Bird — Clone em Python & Pygame

Clone completo do clássico **Flappy Bird** desenvolvido em **Python** com **Pygame**, estruturado em arquitetura modular e renderizado inteiramente com primitivas gráficas (sem dependência de sprites externos). O projeto implementa física de gravidade, geração periódica de obstáculos, detecção de colisões, sistema de pontuação em tempo real e tela de Game Over com reinício imediato.

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.6.1-34B14C?style=for-the-badge&logo=python&logoColor=white)

<!-- adicionar print aqui -->

---

## 📑 Índice

- [Funcionalidades](#-funcionalidades)
- [Como o Jogo Funciona](#-como-o-jogo-funciona)
- [Arquitetura do Projeto](#-arquitetura-do-projeto)
- [Visão Geral do Código](#-visão-geral-do-código)
- [Configurações](#-configurações)
- [Como Executar](#-como-executar)
- [Controles](#-controles)
- [Solução de Problemas](#-solução-de-problemas)
- [Etapas de Desenvolvimento](#-etapas-de-desenvolvimento)
- [Ideias de Melhorias Futuras](#-ideias-de-melhorias-futuras)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Autor](#-autor)

---

## ✨ Funcionalidades

- **Física de voo responsiva:** aceleração gravitacional contínua, velocidade terminal de queda e impulso vertical por teclado ou mouse.
- **Geração automática de obstáculos:** pares de canos criados a cada `1500 ms` com vão fixo de `150 px` e alturas sorteadas dentro de margens seguras.
- **Gerenciamento de memória:** remoção automática dos canos que saem pela borda esquerda da tela.
- **Colisões precisas:** verificação pura baseada em `pygame.Rect` contra o cano superior, cano inferior, chão e topo da janela.
- **Pontuação em tempo real:** placar centralizado no topo que soma `+1` ponto exatamente uma vez por obstáculo ultrapassado.
- **Tela de Game Over e reinício rápido:** congelamento imediato da cena ao colidir, exibição da pontuação final e reinício da partida com a tecla `R`.

---

## ⚙️ Como o Jogo Funciona

### 1. Game Loop em 3 Fases (60 FPS)
O loop principal em `main.py` executa a `60 FPS` constantes (`relogio.tick(FPS)`) e mantém separação estrita entre:
1. **Fase 1 — Leitura e Processamento de Eventos:** captura o fechamento da janela (`pygame.QUIT`), o timer de criação de canos (`EVENTO_NOVO_CANO`), os comandos de pulo (`K_SPACE`, `K_UP` ou botão esquerdo do mouse) e a tecla de reinício (`K_r`).
2. **Fase 2 — Atualização do Estado:** quando o jogo está ativo, atualiza a física do pássaro, desloca os canos para a esquerda, descarta canos fora da tela, verifica colisões e contabiliza a pontuação.
3. **Fase 3 — Renderização na Tela:** desenha em ordem o céu, os pares de canos, a faixa do chão, o pássaro, o placar e, quando aplicável, o painel de Game Over.

### 2. Máquina de Estados
O fluxo da partida é controlado pela variável `estado`, que alterna entre dois valores definidos em `config.py`:
- `ESTADO_JOGANDO = "jogando"`: física ativa, controles de pulo liberados e timer `EVENTO_NOVO_CANO` disparando a cada `1500 ms`.
- `ESTADO_GAME_OVER = "game_over"`: acionado assim que `verificar_colisao(passaro, canos)` retorna `True`. Desativa o timer de spawn (`pygame.time.set_timer(EVENTO_NOVO_CANO, 0)`), imprime `"Game over"` uma única vez no console, congela a posição do pássaro e dos canos e exibe o painel de fim de jogo.

### 3. Sistema de Pontuação e Reinício
- **Pontuação (`score`):** cada instância de `Cano` possui o atributo `pontuado = False`. A cada frame em `ESTADO_JOGANDO` (desde que não haja colisão), a função `atualizar_pontuacao()` verifica se a posição horizontal do pássaro ultrapassou a borda direita do cano (`passaro.x > cano.rect_superior.right`). Se `cano.pontuado` for `False`, incrementa `score += 1` e marca `cano.pontuado = True`, garantindo que o mesmo cano nunca pontue duas vezes.
- **Reinício (`resetar_jogo()`):** ao pressionar `R` durante o estado `ESTADO_GAME_OVER`, a função recria o objeto `Passaro`, esvazia a lista `canos = []`, zera `score = 0`, restaura `estado = ESTADO_JOGANDO` e reprograma o timer `EVENTO_NOVO_CANO`.

---

## 📂 Arquitetura do Projeto

O repositório possui o `README.md` na raiz e o código-fonte do jogo dentro da pasta `flappy bird/`:

```text
flappyy-bird/
├── README.md                # Documentação completa do projeto
└── flappy bird/
    ├── main.py              # Ponto de entrada, Game Loop, eventos, placar, Game Over e reinício
    ├── config.py            # Constantes globais de janela, estados, cores, física, canos e UI
    ├── passaro.py           # Classe Passaro (gravidade, pulo, hitbox e renderização vetorial)
    ├── cano.py              # Classe Cano (sorteio do vão vertical, movimento, flag pontuado e remoção)
    ├── colisao.py           # Função pura verificar_colisao() para canos, chão e topo
    ├── requirements.txt     # Dependência externa do projeto (pygame==2.6.1)
    └── .gitignore           # Ignora venv/ e __pycache__/ no controle de versão
```

---

## 🧩 Visão Geral do Código

### 1. `main.py` — Game Loop, Estados, Placar e Reinício
Gerencia o ciclo de vida do Pygame, inicializa as fontes uma única vez fora do loop (`inicializar_fontes()`), processa eventos e coordena a transição entre `ESTADO_JOGANDO` e `ESTADO_GAME_OVER`.

```python
def atualizar_pontuacao(passaro, canos, score) -> int:
    """
    Soma +1 ao score quando o eixo X do pássaro ultrapassa o lado direito
    de um cano que ainda não foi contabilizado (cano.pontuado == False).
    """
    for cano in canos:
        if not cano.pontuado and passaro.x > cano.rect_superior.right:
            score += 1
            cano.pontuado = True
    return score


def resetar_jogo():
    """
    Reinicia todos os elementos da partida (pássaro, lista de canos, score,
    estado do jogo e timer de geração de obstáculos).
    """
    passaro = Passaro()
    canos = []
    score = 0
    estado = ESTADO_JOGANDO

    pygame.time.set_timer(EVENTO_NOVO_CANO, INTERVALO_CANO)

    return passaro, canos, score, estado
```

### 2. `config.py` — Configurações e Constantes Globais
Centraliza todas as dimensões, cores RGB, parâmetros físicos, medidas dos canos e textos da interface para evitar números mágicos espalhados pelo código.

```python
# Constantes de Física do Pássaro
PASSARO_X = 80                  # Posição horizontal fixa do pássaro
PASSARO_RAIO = 17               # Raio do corpo do pássaro
GRAVIDADE = 0.45                # Aceleração da gravidade por frame
FORCA_PULO = -8.5               # Impulso vertical ao pular (negativo = sobe)
VELOCIDADE_MAX_QUEDA = 10.0     # Velocidade terminal de queda

# Constantes dos Canos e Cenário
ALTURA_CHAO = 60                # Altura da faixa do chão na base da janela
GAP_CANO = 150                  # Abertura vertical fixa entre cano superior e inferior
LARGURA_CANO = 70               # Largura horizontal de cada cano
VELOCIDADE_CANO = 3             # Velocidade de deslocamento dos canos para a esquerda
INTERVALO_CANO = 1500           # Intervalo de geração de novos canos (em milissegundos)
```

### 3. `passaro.py` — Entidade `Passaro`
Controla a posição vertical do jogador, aplica a gravidade com limite de velocidade terminal, mantém a *hitbox* (`self.rect`) sincronizada e desenha o personagem (corpo, asa, olho e bico).

```python
class Passaro:
    def __init__(self):
        self.x = PASSARO_X
        self.y = ALTURA // 2
        self.raio = PASSARO_RAIO
        self.velocidade_y = 0.0
        self.rect = pygame.Rect(
            int(self.x - self.raio),
            int(self.y - self.raio),
            self.raio * 2,
            self.raio * 2,
        )

    def pular(self):
        """Aplica um impulso vertical para cima."""
        self.velocidade_y = FORCA_PULO
```

### 4. `cano.py` — Entidade `Cano`
Representa cada par de obstáculos (superior e inferior). Sorteia a posição do vão com `random.randint(MARGEM_VAO_MIN, MARGEM_VAO_MAX)`, move os retângulos para a esquerda e informa quando o obstáculo saiu da tela.

```python
class Cano:
    def __init__(self):
        self.x = LARGURA
        self.pontuado = False

        topo_vao = random.randint(MARGEM_VAO_MIN, MARGEM_VAO_MAX)
        base_vao = topo_vao + GAP_CANO
        limite_chao_y = ALTURA - ALTURA_CHAO

        self.rect_superior = pygame.Rect(self.x, 0, LARGURA_CANO, topo_vao)
        self.rect_inferior = pygame.Rect(
            self.x, base_vao, LARGURA_CANO, limite_chao_y - base_vao
        )

    def fora_da_tela(self) -> bool:
        """Retorna True quando o cano saiu completamente pela borda esquerda."""
        return self.rect_superior.right < 0
```

### 5. `colisao.py` — Detecção de Colisões
Módulo com a função pura `verificar_colisao(passaro, canos)`, que decide se houve impacto sem alterar variáveis globais nem imprimir efeitos colaterais.

```python
def verificar_colisao(passaro, canos) -> bool:
    limite_chao_y = ALTURA - ALTURA_CHAO

    if passaro.rect.bottom >= limite_chao_y or passaro.rect.top <= 0:
        return True

    for cano in canos:
        if (
            passaro.rect.colliderect(cano.rect_superior)
            or passaro.rect.colliderect(cano.rect_inferior)
        ):
            return True

    return False
```

---

## 🔧 Configurações

Todas as constantes abaixo estão em `flappy bird/config.py` e podem ser ajustadas para calibrar a dificuldade ou o visual do jogo:

| Constante | Valor Real | Descrição |
| :--- | :--- | :--- |
| `LARGURA` | `400` | Largura da janela em pixels |
| `ALTURA` | `600` | Altura da janela em pixels |
| `FPS` | `60` | Taxa de quadros por segundo |
| `TITULO` | `"Flappy Bird"` | Título exibido na barra da janela |
| `ESTADO_JOGANDO` | `"jogando"` | Identificador do estado de partida em andamento |
| `ESTADO_GAME_OVER` | `"game_over"` | Identificador do estado de fim de jogo |
| `COR_CEU` | `(113, 197, 207)` | Cor RGB do fundo da tela (azul claro) |
| `COR_PASSARO` | `(247, 213, 29)` | Cor RGB do corpo do pássaro e título de Game Over |
| `COR_ASA` | `(255, 235, 120)` | Cor RGB da asa do pássaro |
| `COR_BICO` | `(232, 97, 1)` | Cor RGB do bico do pássaro |
| `COR_CANO` | `(34, 177, 76)` | Cor RGB dos canos (verde) |
| `COR_CHAO` | `(222, 216, 149)` | Cor RGB da faixa do chão (bege) |
| `BRANCO` | `(255, 255, 255)` | Cor RGB branca (olho do pássaro) |
| `PRETO` | `(0, 0, 0)` | Cor RGB preta (contornos e sombra do placar) |
| `COR_PAINEL_FUNDO` | `(30, 30, 30)` | Cor RGB do fundo do painel de Game Over |
| `PASSARO_X` | `80` | Posição horizontal fixa do pássaro |
| `PASSARO_RAIO` | `17` | Raio do círculo do pássaro em pixels |
| `GRAVIDADE` | `0.45` | Aceleração vertical somada a cada frame |
| `FORCA_PULO` | `-8.5` | Velocidade vertical aplicada no momento do pulo |
| `VELOCIDADE_MAX_QUEDA` | `10.0` | Velocidade máxima permitida durante a queda |
| `ALTURA_CHAO` | `60` | Altura da faixa do chão na base da tela |
| `GAP_CANO` | `150` | Abertura vertical livre entre o cano superior e o inferior |
| `LARGURA_CANO` | `70` | Largura de cada cano em pixels |
| `VELOCIDADE_CANO` | `3` | Pixels deslocados para a esquerda a cada frame |
| `INTERVALO_CANO` | `1500` | Intervalo entre novos pares de canos em milissegundos |
| `MARGEM_VAO_MIN` | `70` | Limite mínimo superior (`Y`) para o sorteio do vão |
| `MARGEM_VAO_MAX` | `320` (`ALTURA - ALTURA_CHAO - GAP_CANO - 70`) | Limite máximo inferior (`Y`) para o sorteio do vão |
| `TAMANHO_FONTE_PLACAR` | `56` | Tamanho da fonte do placar no topo |
| `TAMANHO_FONTE_GAME_OVER` | `54` | Tamanho da fonte do título `"Game Over"` |
| `TAMANHO_FONTE_INSTRUCAO` | `26` | Tamanho da fonte da pontuação final e instrução |
| `COR_TEXTO` | `(255, 255, 255)` | Cor RGB dos textos do placar e painel |
| `POS_PLACAR` | `(200, 50)` (`(LARGURA // 2, 50)`) | Coordenada central do placar no topo da janela |
| `TECLA_REINICIAR` | `pygame.K_r` | Tecla que reinicia o jogo após o Game Over |
| `TEXTO_GAME_OVER` | `"Game Over"` | Título exibido no painel de fim de jogo |
| `TEXTO_REINICIAR` | `"Pressione R para jogar novamente"` | Instrução exibida no painel de fim de jogo |
| `PAINEL_LARGURA` | `340` | Largura do painel central de Game Over |
| `PAINEL_ALTURA` | `190` | Altura do painel central de Game Over |
| `PAINEL_BORDA` | `3` | Espessura da borda do painel de Game Over |
| `OFFSET_SOMBRA_TEXTO` | `2` | Deslocamento em pixels da sombra do placar |
| `OFFSET_TITULO_Y` | `-50` | Deslocamento vertical do título no painel de Game Over |
| `OFFSET_SCORE_FINAL_Y` | `0` | Deslocamento vertical da pontuação final no painel |
| `OFFSET_INSTRUCAO_Y` | `50` | Deslocamento vertical da instrução de reinício no painel |

---

## 🚀 Como Executar

### Pré-requisitos
- **Python 3.12** instalado.

### 1. Clonar o repositório e acessar a pasta do código

```bash
git clone https://github.com/BeserraBiel/flappyy-bird.git
cd "flappyy-bird/flappy bird"
```

### 2. Criar o ambiente virtual e instalar as dependências

#### No Windows (PowerShell)
```powershell
py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

> **Alternativa rápida no Windows (sem ativar o `venv`):**
> ```powershell
> py -3.12 -m venv venv
> .\venv\Scripts\python.exe -m pip install -r requirements.txt
> .\venv\Scripts\python.exe main.py
> ```

#### No Linux / macOS
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

---

## 🕹️ Controles

| Tecla / Ação | Estado | Função |
| :--- | :--- | :--- |
| `Espaço` (`pygame.K_SPACE`) | `jogando` | Faz o pássaro pular |
| `Seta para Cima` (`pygame.K_UP`) | `jogando` | Faz o pássaro pular |
| `Botão Esquerdo do Mouse` (`button == 1`) | `jogando` | Faz o pássaro pular |
| `R` (`pygame.K_r`) | `game_over` | Reinicia a partida do zero |
| Fechar a janela (`X` / `pygame.QUIT`) | Qualquer estado | Encerra o Pygame e fecha o programa |

---

## 🛠️ Solução de Problemas

- **O comando `python` abre a Microsoft Store no Windows:**
  O atalho padrão do Windows está interceptando o comando. Use o launcher oficial passando a versão instalada:
  ```powershell
  py -3.12 -m venv venv
  ```
- **O PowerShell bloqueia o script `.\venv\Scripts\Activate.ps1`:**
  Não é necessário alterar a política de execução (`ExecutionPolicy`) do sistema. Execute o Python e o `pip` diretamente pelo executável de dentro do `venv`:
  ```powershell
  .\venv\Scripts\python.exe main.py
  ```
- **Erro `ModuleNotFoundError: No module named 'pygame'`:**
  Certifique-se de estar dentro da pasta `flappy bird` e de executar o script usando o interpretador do ambiente virtual (`.\venv\Scripts\python.exe main.py`), onde o `pygame` foi instalado.

---

## 📈 Etapas de Desenvolvimento

1. **Etapa 1 — Janela e Game Loop:** configuração da janela `400x600` a `60 FPS` e estruturação do loop principal em eventos, atualização e renderização.
2. **Etapa 2 — Pássaro e Gravidade:** implementação da classe `Passaro` com queda acelerada, velocidade terminal, pulo e desenho vetorial.
3. **Etapa 3 — Canos:** criação da classe `Cano` com abertura vertical de `150 px` sorteada, spawn periódico via timer de `1500 ms` e remoção ao sair da tela.
4. **Etapa 4 — Colisão e Estados:** detecção pura de impacto (`colisao.py`) com canos, chão e topo, congelando a partida no estado `game_over`.
5. **Etapa 5 — Pontuação e Reinício:** contagem de pontos por cano superado (`cano.pontuado`), placar no topo, tela de Game Over e reinício com a tecla `R`.

---

## 💡 Ideias de Melhorias Futuras

- **Recorde salvo em arquivo:** persistir a maior pontuação (`High Score`) em um arquivo local para exibi-la no painel de Game Over.
- **Efeitos sonoros:** adicionar áudio para o pulo, pontuação e colisão utilizando `pygame.mixer`.
- **Sprites e animações:** incluir texturas para o cenário, canos e animação de bater de asas com rotação do pássaro.
- **Dificuldade progressiva:** elevar gradualmente a velocidade dos canos (`VELOCIDADE_CANO`) conforme a pontuação aumenta.
- **Menu inicial:** adicionar uma tela de título antes do início da primeira partida.

---

## 🧰 Tecnologias Utilizadas

- **[Python 3.12](https://www.python.org/)** (módulos nativos `sys` e `random`)
- **[Pygame 2.6.1](https://www.pygame.org/)** (`pygame==2.6.1` no `requirements.txt`)

---

## 👤 Autor

Desenvolvido por **BeserraBiel** — [github.com/BeserraBiel](https://github.com/BeserraBiel)
