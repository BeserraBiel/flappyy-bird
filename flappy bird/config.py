"""
Flappy Bird - Clone em Pygame
Módulo de Configurações e Constantes Globais
"""

# ==========================================
# CONFIGURAÇÕES DA JANELA E JOGO
# ==========================================
LARGURA = 400
ALTURA = 600
FPS = 60
TITULO = "Flappy Bird"

# Estados do Jogo
ESTADO_JOGANDO = "jogando"
ESTADO_GAME_OVER = "game_over"

# ==========================================
# PALETA DE CORES (RGB)
# ==========================================
COR_CEU = (113, 197, 207)       # Azul claro clássico do Flappy Bird
COR_PASSARO = (247, 213, 29)    # Amarelo do pássaro
COR_ASA = (255, 235, 120)       # Amarelo claro da asa
COR_BICO = (232, 97, 1)         # Laranja do bico
COR_CANO = (34, 177, 76)        # Verde dos canos
COR_CHAO = (222, 216, 149)      # Bege clássico do chão
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# ==========================================
# CONSTANTES DE FÍSICA DO PÁSSARO
# ==========================================
PASSARO_X = 80                  # Posição horizontal fixa do pássaro
PASSARO_RAIO = 17               # Raio do corpo do pássaro
GRAVIDADE = 0.45                # Aceleração da gravidade por frame
FORCA_PULO = -8.5               # Impulso vertical ao pular (negativo = sobe)
VELOCIDADE_MAX_QUEDA = 10.0     # Velocidade terminal de queda

# ==========================================
# CONSTANTES DOS CANOS E CENÁRIO
# ==========================================
ALTURA_CHAO = 60                # Altura da faixa do chão na base da janela
GAP_CANO = 150                  # Abertura vertical fixa entre cano superior e inferior
LARGURA_CANO = 70               # Largura horizontal de cada cano
VELOCIDADE_CANO = 3             # Velocidade de deslocamento dos canos para a esquerda
INTERVALO_CANO = 1500           # Intervalo de geração de novos canos (em milissegundos)
MARGEM_VAO_MIN = 70             # Posição Y mínima para o início do vão livre
MARGEM_VAO_MAX = ALTURA - ALTURA_CHAO - GAP_CANO - 70  # Posição Y máxima para o início do vão
