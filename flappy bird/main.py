"""
Flappy Bird - Clone em Pygame
Arquivo Principal (Game Loop, Gerenciamento de Canos e Estados do Jogo)
"""

import sys
import pygame
from cano import Cano
from colisao import verificar_colisao
from config import (
    ALTURA,
    ALTURA_CHAO,
    COR_CEU,
    COR_CHAO,
    ESTADO_GAME_OVER,
    ESTADO_JOGANDO,
    FPS,
    INTERVALO_CANO,
    LARGURA,
    PRETO,
    TITULO,
)
from passaro import Passaro

# Evento customizado para geração periódica de canos
EVENTO_NOVO_CANO = pygame.USEREVENT + 1


def atualizar(passaro, canos):
    """
    Fase 2 do Game Loop: Atualização de Estado.
    Atualiza a física do pássaro, move os canos e remove os que saíram da tela.
    """
    passaro.atualizar()

    for cano in canos:
        cano.atualizar()

    # Remove da lista os canos que já saíram totalmente pela esquerda
    canos[:] = [cano for cano in canos if not cano.fora_da_tela()]


def desenhar(tela, passaro, canos):
    """
    Fase 3 do Game Loop: Renderização.
    Desenha o céu, os canos, a faixa do chão e o pássaro.
    """
    tela.fill(COR_CEU)

    for cano in canos:
        cano.desenhar(tela)

    # Desenha o chão na base da tela
    chao_rect = pygame.Rect(0, ALTURA - ALTURA_CHAO, LARGURA, ALTURA_CHAO)
    pygame.draw.rect(tela, COR_CHAO, chao_rect)
    pygame.draw.line(
        tela,
        PRETO,
        (0, ALTURA - ALTURA_CHAO),
        (LARGURA, ALTURA - ALTURA_CHAO),
        2,
    )

    passaro.desenhar(tela)


def main():
    """
    Função principal responsável pela inicialização do Pygame e execução do Game Loop.
    """
    # 1. Inicialização do Pygame
    pygame.init()

    # 2. Configuração da janela e do relógio de controle de FPS
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption(TITULO)
    relogio = pygame.time.Clock()

    # 3. Instanciação dos objetos e estado inicial do jogo
    passaro = Passaro()
    canos = []
    estado = ESTADO_JOGANDO

    # Configura o timer para disparar EVENTO_NOVO_CANO a cada INTERVALO_CANO ms
    pygame.time.set_timer(EVENTO_NOVO_CANO, INTERVALO_CANO)

    rodando = True

    # ==========================================
    # GAME LOOP PRINCIPAL
    # ==========================================
    while rodando:
        # ------------------------------------------
        # FASE 1: LEITURA E PROCESSAMENTO DE EVENTOS
        # ------------------------------------------
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            elif evento.type == EVENTO_NOVO_CANO and estado == ESTADO_JOGANDO:
                canos.append(Cano())

            elif evento.type == pygame.KEYDOWN and estado == ESTADO_JOGANDO:
                if evento.key in (pygame.K_SPACE, pygame.K_UP):
                    passaro.pular()

            elif evento.type == pygame.MOUSEBUTTONDOWN and estado == ESTADO_JOGANDO:
                if evento.button == 1:  # Botão esquerdo do mouse
                    passaro.pular()

        # ------------------------------------------
        # FASE 2: ATUALIZAÇÃO DO ESTADO DO JOGO
        # ------------------------------------------
        if estado == ESTADO_JOGANDO:
            atualizar(passaro, canos)

            if verificar_colisao(passaro, canos):
                estado = ESTADO_GAME_OVER
                pygame.time.set_timer(EVENTO_NOVO_CANO, 0)
                print("Game over")

        # ------------------------------------------
        # FASE 3: RENDERIZAÇÃO NA TELA
        # ------------------------------------------
        desenhar(tela, passaro, canos)
        pygame.display.flip()

        # Controle de taxa de quadros por segundo (FPS estável)
        relogio.tick(FPS)

    # ==========================================
    # FINALIZAÇÃO SEGURA
    # ==========================================
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
