"""
Flappy Bird - Clone em Pygame
Arquivo Principal (Game Loop e Controle de Eventos)
"""

import sys
import pygame
from config import ALTURA, COR_CEU, FPS, LARGURA, TITULO
from passaro import Passaro


def atualizar(passaro):
    """
    Fase 2 do Game Loop: Atualização de Estado.
    Aqui será inserida a lógica de física, movimentação e colisões nas próximas etapas.
    """
    passaro.atualizar()


def desenhar(tela, passaro):
    """
    Fase 3 do Game Loop: Renderização.
    Preenche a tela com a cor de fundo e prepara os elementos visuais.
    """
    tela.fill(COR_CEU)
    passaro.desenhar(tela)
    # Nas próximas etapas, desenharemos aqui os canos, chão e placar.


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

    # 3. Instanciação dos objetos do jogo
    passaro = Passaro()

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
            elif evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_SPACE, pygame.K_UP):
                    passaro.pular()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # Botão esquerdo do mouse
                    passaro.pular()

        # ------------------------------------------
        # FASE 2: ATUALIZAÇÃO DO ESTADO DO JOGO
        # ------------------------------------------
        atualizar(passaro)

        # ------------------------------------------
        # FASE 3: RENDERIZAÇÃO NA TELA
        # ------------------------------------------
        desenhar(tela, passaro)
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
