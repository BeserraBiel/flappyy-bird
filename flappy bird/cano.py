"""
Flappy Bird - Clone em Pygame
Módulo da Entidade Cano (Obstáculos)
"""

import random
import pygame
from config import (
    ALTURA,
    ALTURA_CHAO,
    COR_CANO,
    GAP_CANO,
    LARGURA,
    LARGURA_CANO,
    MARGEM_VAO_MAX,
    MARGEM_VAO_MIN,
    PRETO,
    VELOCIDADE_CANO,
)


class Cano:
    """
    Representa um par de canos (superior e inferior) separado por um vão vertical
    fixo (GAP_CANO), que se desloca da direita para a esquerda.
    """

    def __init__(self):
        self.x = LARGURA

        # Sorteia onde começa o vão vertical respeitando as margens de segurança
        topo_vao = random.randint(MARGEM_VAO_MIN, MARGEM_VAO_MAX)
        base_vao = topo_vao + GAP_CANO
        limite_chao_y = ALTURA - ALTURA_CHAO

        # Retângulos de colisão e desenho (superior e inferior)
        self.rect_superior = pygame.Rect(
            self.x,
            0,
            LARGURA_CANO,
            topo_vao,
        )
        self.rect_inferior = pygame.Rect(
            self.x,
            base_vao,
            LARGURA_CANO,
            limite_chao_y - base_vao,
        )

    def atualizar(self):
        """Move o par de canos para a esquerda e sincroniza seus Rects."""
        self.x -= VELOCIDADE_CANO
        self.rect_superior.x = int(self.x)
        self.rect_inferior.x = int(self.x)

    def desenhar(self, tela):
        """Renderiza os canos superior e inferior na tela."""
        pygame.draw.rect(tela, COR_CANO, self.rect_superior)
        pygame.draw.rect(tela, PRETO, self.rect_superior, 2)

        pygame.draw.rect(tela, COR_CANO, self.rect_inferior)
        pygame.draw.rect(tela, PRETO, self.rect_inferior, 2)

    def fora_da_tela(self) -> bool:
        """Retorna True quando o cano saiu completamente pela borda esquerda."""
        return self.rect_superior.right < 0
