"""
Flappy Bird - Clone em Pygame
Módulo da Entidade Pássaro
"""

import pygame
from config import (
    ALTURA,
    ALTURA_CHAO,
    BRANCO,
    COR_ASA,
    COR_BICO,
    COR_PASSARO,
    FORCA_PULO,
    GRAVIDADE,
    PASSARO_RAIO,
    PASSARO_X,
    PRETO,
    VELOCIDADE_MAX_QUEDA,
)


class Passaro:
    """
    Representa o pássaro controlado pelo jogador, gerenciando sua posição,
    física (gravidade e pulo), retângulo de colisão (rect) e renderização.
    """

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

    def atualizar(self):
        """Atualiza a velocidade, a posição vertical e sincroniza o rect de colisão."""
        self.velocidade_y += GRAVIDADE
        if self.velocidade_y > VELOCIDADE_MAX_QUEDA:
            self.velocidade_y = VELOCIDADE_MAX_QUEDA

        self.y += self.velocidade_y

        limite_chao_y = ALTURA - ALTURA_CHAO

        # Impede que o pássaro atravesse o topo ou afunde além da superfície do chão
        if self.y - self.raio < 0:
            self.y = self.raio
            self.velocidade_y = 0.0
        elif self.y + self.raio > limite_chao_y:
            self.y = limite_chao_y - self.raio
            self.velocidade_y = 0.0

        # Sincroniza o atributo obrigatório rect com a posição atual
        self.rect.x = int(self.x - self.raio)
        self.rect.y = int(self.y - self.raio)

    def obter_rect(self):
        """Retorna o retângulo de colisão (hitbox) do pássaro."""
        return self.rect

    def desenhar(self, tela):
        """Desenha o pássaro na tela com corpo, asa, olho e bico."""
        centro = (int(self.x), int(self.y))

        # Corpo principal
        pygame.draw.circle(tela, COR_PASSARO, centro, self.raio)
        pygame.draw.circle(tela, PRETO, centro, self.raio, 2)

        # Asa
        asa_rect = pygame.Rect(int(self.x - 12), int(self.y - 2), 14, 10)
        pygame.draw.ellipse(tela, COR_ASA, asa_rect)
        pygame.draw.ellipse(tela, PRETO, asa_rect, 1)

        # Olho
        olho_pos = (int(self.x + 6), int(self.y - 5))
        pygame.draw.circle(tela, BRANCO, olho_pos, 6)
        pygame.draw.circle(tela, PRETO, olho_pos, 6, 1)
        pygame.draw.circle(tela, PRETO, (int(self.x + 8), int(self.y - 5)), 2)

        # Bico
        bico_pontos = [
            (int(self.x + 12), int(self.y - 2)),
            (int(self.x + 24), int(self.y + 3)),
            (int(self.x + 12), int(self.y + 8)),
        ]
        pygame.draw.polygon(tela, COR_BICO, bico_pontos)
        pygame.draw.polygon(tela, PRETO, bico_pontos, 1)
