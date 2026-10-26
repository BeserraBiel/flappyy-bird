# 🐦 Flappy Bird — Clone em Python & Pygame

Um clone clássico do **Flappy Bird** desenvolvido em **Python** utilizando a biblioteca **Pygame**, construído com arquitetura modular, separação clara de responsabilidades e sem dependência de arquivos externos de imagem (todos os elementos visuais são renderizados via primitivas gráficas do Pygame).

---

## 🎮 Como o Jogo Funciona

O projeto implementa o ciclo clássico de um *Game Loop* em 60 FPS dividido em três fases bem definidas:

1. **Leitura de Eventos (Input):**
   - Captura ações do jogador (`Espaço`, `Seta para Cima` ou **clique esquerdo do mouse**) para aplicar impulso vertical ao pássaro.
   - Gerencia o evento temporizado (`EVENTO_NOVO_CANO`), que gera um novo par de obstáculos a cada `1500 ms`.
2. **Atualização de Estado (Física e Lógica):**
   - **Gravidade e Pulo:** O pássaro sofre aceleração gravitacional contínua a cada frame até atingir a velocidade terminal de queda, enquanto o pulo aplica uma velocidade vertical negativa instantânea.
   - **Movimentação de Obstáculos:** Os pares de canos (superior e inferior) deslocam-se da direita para a esquerda em velocidade constante e são removidos automaticamente da memória assim que saem da tela.
   - **Detecção de Colisões:** Verifica a interseção entre as *hitboxes* (`pygame.Rect`) do pássaro, dos canos e dos limites do cenário (chão e topo).
   - **Máquina de Estados:** Controla a transição entre `jogando` e `game_over`, congelando a física e o gerador de canos no momento exato do impacto.
3. **Renderização (Desenho em Tela):**
   - Desenha o céu, os pares de canos com abertura vertical sorteada (`150 px`), o chão e o pássaro (corpo, asa, olho e bico).

---

## 📂 Arquitetura do Projeto

O código é dividido em módulos independentes para facilitar a leitura, manutenção e evolução:

```text
flappy-bird/
├── main.py            # Ponto de entrada, Game Loop, eventos e máquina de estados
├── config.py          # Constantes globais (resolução, FPS, cores, física e canos)
├── passaro.py         # Classe Passaro (física de gravidade, pulo, hitbox e desenho)
├── cano.py            # Classe Cano (sorteio do vão vertical, movimento e remoção)
├── colisao.py         # Função pura para detecção de colisões com canos e limites
├── requirements.txt   # Dependências do projeto (pygame)
└── README.md          # Documentação do repositório
```

---

## 🚀 Como Executar no Seu Computador

### Pré-requisitos
- **Python 3.10+** instalado

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/SEU-USUARIO/flappy-bird.git
   cd flappy-bird
   ```

2. **Crie e ative um ambiente virtual (`venv`):**

   - **Windows (PowerShell):**
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
     *(Caso o PowerShell bloqueie a ativação de scripts, você pode rodar os comandos diretamente com `.\venv\Scripts\python.exe` sem precisar alterar as políticas do Windows).*

   - **Linux / macOS:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Inicie o jogo:**
   ```bash
   python main.py
   ```
   *(Ou no Windows sem ativar o `venv`: `.\venv\Scripts\python.exe main.py`)*

---

## 🕹️ Controles

| Tecla / Ação | Função |
| :--- | :--- |
| `Espaço` | Faz o pássaro pular |
| `Seta para Cima` (`↑`) | Faz o pássaro pular |
| `Botão Esquerdo do Mouse` | Faz o pássaro pular |
| Fechar janela (`X`) | Encerra o jogo com segurança |

---

## 🛠️ Tecnologias Utilizadas

- **[Python 3.12](https://www.python.org/)**
- **[Pygame 2.6.1](https://www.pygame.org/)** (`pygame`, `random` e `sys`)
