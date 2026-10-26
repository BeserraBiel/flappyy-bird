"""
Flappy Bird - Clone em Pygame
Arquivo Principal (Game Loop, Canos, Colisões, Pontuação e Reinício)
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
    COR_PAINEL_FUNDO,
    COR_PASSARO,
    COR_TEXTO,
    ESTADO_GAME_OVER,
    ESTADO_JOGANDO,
    FPS,
    INTERVALO_CANO,
    LARGURA,
    OFFSET_INSTRUCAO_Y,
    OFFSET_SCORE_FINAL_Y,
    OFFSET_SOMBRA_TEXTO,
    OFFSET_TITULO_Y,
    PAINEL_ALTURA,
    PAINEL_BORDA,
    PAINEL_LARGURA,
    POS_PLACAR,
    PRETO,
    TAMANHO_FONTE_GAME_OVER,
    TAMANHO_FONTE_INSTRUCAO,
    TAMANHO_FONTE_PLACAR,
    TECLA_REINICIAR,
    TEXTO_GAME_OVER,
    TEXTO_REINICIAR,
    TITULO,
)
from passaro import Passaro

# Evento customizado para geração periódica de canos
EVENTO_NOVO_CANO = pygame.USEREVENT + 1

# Objetos de fonte instanciados uma única vez fora do Game Loop
FONTE_PLACAR = None
FONTE_GAME_OVER = None
FONTE_INSTRUCAO = None


def inicializar_fontes():
    """Inicializa as fontes do Pygame uma única vez antes do Game Loop."""
    global FONTE_PLACAR, FONTE_GAME_OVER, FONTE_INSTRUCAO
    FONTE_PLACAR = pygame.font.Font(None, TAMANHO_FONTE_PLACAR)
    FONTE_GAME_OVER = pygame.font.Font(None, TAMANHO_FONTE_GAME_OVER)
    FONTE_INSTRUCAO = pygame.font.Font(None, TAMANHO_FONTE_INSTRUCAO)


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


def desenhar_placar(tela, score):
    """Exibe a pontuação atual centralizada no topo da tela com contorno."""
    texto_str = str(score)

    # Sombra do texto para boa leitura sobre o céu e os canos
    superficie_sombra = FONTE_PLACAR.render(texto_str, True, PRETO)
    rect_sombra = superficie_sombra.get_rect(
        center=(
            POS_PLACAR[0] + OFFSET_SOMBRA_TEXTO,
            POS_PLACAR[1] + OFFSET_SOMBRA_TEXTO,
        )
    )
    tela.blit(superficie_sombra, rect_sombra)

    # Texto principal do placar
    superficie_texto = FONTE_PLACAR.render(texto_str, True, COR_TEXTO)
    rect_texto = superficie_texto.get_rect(center=POS_PLACAR)
    tela.blit(superficie_texto, rect_texto)


def desenhar_game_over(tela, score):
    """
    Desenha a sobreposição de Game Over centralizada sobre a cena congelada,
    mostrando o título, a pontuação final e a instrução de reinício.
    """
    centro_x = LARGURA // 2
    centro_y = ALTURA // 2

    # Painel centralizado para destacar as informações de fim de jogo
    painel_rect = pygame.Rect(0, 0, PAINEL_LARGURA, PAINEL_ALTURA)
    painel_rect.center = (centro_x, centro_y)
    pygame.draw.rect(tela, COR_PAINEL_FUNDO, painel_rect, border_radius=10)
    pygame.draw.rect(tela, COR_TEXTO, painel_rect, PAINEL_BORDA, border_radius=10)

    # 1. Título "Game Over"
    sup_titulo = FONTE_GAME_OVER.render(TEXTO_GAME_OVER, True, COR_PASSARO)
    rect_titulo = sup_titulo.get_rect(center=(centro_x, centro_y + OFFSET_TITULO_Y))
    tela.blit(sup_titulo, rect_titulo)

    # 2. Pontuação Final
    sup_score = FONTE_INSTRUCAO.render(f"Pontuação final: {score}", True, COR_TEXTO)
    rect_score = sup_score.get_rect(center=(centro_x, centro_y + OFFSET_SCORE_FINAL_Y))
    tela.blit(sup_score, rect_score)

    # 3. Instrução para reiniciar
    sup_instrucao = FONTE_INSTRUCAO.render(TEXTO_REINICIAR, True, COR_TEXTO)
    rect_instrucao = sup_instrucao.get_rect(
        center=(centro_x, centro_y + OFFSET_INSTRUCAO_Y)
    )
    tela.blit(sup_instrucao, rect_instrucao)


def desenhar(tela, passaro, canos, score, estado):
    """
    Fase 3 do Game Loop: Renderização.
    Desenha o cenário, entidades, placar e (se aplicável) a tela de Game Over.
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
    desenhar_placar(tela, score)

    if estado == ESTADO_GAME_OVER:
        desenhar_game_over(tela, score)


def resetar_jogo():
    """
    Reinicia todos os elementos da partida (pássaro, lista de canos, score,
    estado do jogo e timer de geração de obstáculos).
    """
    passaro = Passaro()
    canos = []
    score = 0
    estado = ESTADO_JOGANDO

    # Reativa o timer de geração de canos sem duplicar timers existentes
    pygame.time.set_timer(EVENTO_NOVO_CANO, INTERVALO_CANO)

    return passaro, canos, score, estado


def main():
    """
    Função principal responsável pela inicialização do Pygame e execução do Game Loop.
    """
    # 1. Inicialização do Pygame e das fontes (fora do loop)
    pygame.init()
    inicializar_fontes()

    # 2. Configuração da janela e do relógio de controle de FPS
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption(TITULO)
    relogio = pygame.time.Clock()

    # 3. Inicialização do estado e objetos do jogo via resetar_jogo()
    passaro, canos, score, estado = resetar_jogo()

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

            elif evento.type == pygame.KEYDOWN:
                if estado == ESTADO_JOGANDO and evento.key in (
                    pygame.K_SPACE,
                    pygame.K_UP,
                ):
                    passaro.pular()
                elif estado == ESTADO_GAME_OVER and evento.key == TECLA_REINICIAR:
                    passaro, canos, score, estado = resetar_jogo()

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
            else:
                score = atualizar_pontuacao(passaro, canos, score)

        # ------------------------------------------
        # FASE 3: RENDERIZAÇÃO NA TELA
        # ------------------------------------------
        desenhar(tela, passaro, canos, score, estado)
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
