"""
Flappy Bird - Clone em Pygame
Módulo de Detecção de Colisões
"""

from config import ALTURA, ALTURA_CHAO


def verificar_colisao(passaro, canos) -> bool:
    """
    Função pura que verifica se o pássaro colidiu com o chão, com o topo da tela
    ou com qualquer um dos canos ativos na lista.
    """
    limite_chao_y = ALTURA - ALTURA_CHAO

    # 1. Verifica toque no chão ou saída pelo topo da tela
    if passaro.rect.bottom >= limite_chao_y or passaro.rect.top <= 0:
        return True

    # 2. Verifica colisão com os retângulos superior e inferior de cada cano
    for cano in canos:
        if (
            passaro.rect.colliderect(cano.rect_superior)
            or passaro.rect.colliderect(cano.rect_inferior)
        ):
            return True

    return False
