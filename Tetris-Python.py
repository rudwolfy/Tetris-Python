import pygame
import random

# Inicializando o Pygame
pygame.init()

# Configurações da tela
largura_tela = 500
altura_tela = 600
largura_jogo = 300
tela = pygame.display.set_mode((largura_tela, altura_tela))

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
CINZA = (169, 169, 169)
AMARELO = (255, 255, 0)

# Dimensões dos blocos
tamanho_bloco = 30

# Configurações do jogo
clock = pygame.time.Clock()
velocidade_jogo = 0.3

# Formatos das peças
formatos = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]]
]

# Classe Peça
class Peca:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.formato = random.choice(formatos)
        self.cor = random.choice([VERMELHO, VERDE, AZUL])
        self.largura = len(self.formato[0])
        self.altura = len(self.formato)

    def desenhar(self, tela):
        for i in range(self.altura):
            for j in range(self.largura):
                if self.formato[i][j] == 1:
                    pygame.draw.rect(tela, self.cor, pygame.Rect((self.x + j) * tamanho_bloco, (self.y + i) * tamanho_bloco, tamanho_bloco, tamanho_bloco))

    def rotacionar(self):
        self.formato = [list(row) for row in zip(*self.formato[::-1])]
        self.largura = len(self.formato[0])
        self.altura = len(self.formato)

# Funções auxiliares
def verificar_colisao(tabuleiro, peca):
    for i in range(peca.altura):
        for j in range(peca.largura):
            if peca.formato[i][j] == 1:
                if peca.y + i >= len(tabuleiro) or peca.x + j >= len(tabuleiro[0]) or peca.x + j < 0 or tabuleiro[peca.y + i][peca.x + j] != PRETO:
                    return True
    return False

def fixar_peca(tabuleiro, peca):
    for i in range(peca.altura):
        for j in range(peca.largura):
            if peca.formato[i][j] == 1:
                tabuleiro[peca.y + i][peca.x + j] = peca.cor

def limpar_linhas(tabuleiro):
    linhas_removidas = 0
    i = len(tabuleiro) - 1
    while i >= 0:
        if PRETO not in tabuleiro[i]:
            del tabuleiro[i]
            tabuleiro.insert(0, [PRETO for _ in range(len(tabuleiro[0]))])
            linhas_removidas += 1
        else:
            i -= 1
    return linhas_removidas

def desenhar_tabuleiro(tela, tabuleiro):
    for i in range(len(tabuleiro)):
        for j in range(len(tabuleiro[0])):
            pygame.draw.rect(tela, tabuleiro[i][j], pygame.Rect(j * tamanho_bloco, i * tamanho_bloco, tamanho_bloco, tamanho_bloco))

def desenhar_texto(tela, texto, tamanho, cor, x, y):
    fonte = pygame.font.SysFont('arial', tamanho)
    superficie = fonte.render(texto, True, cor)
    rect = superficie.get_rect()
    rect.center = (x, y)
    tela.blit(superficie, rect)

def tela_entrada():
    rodando = True
    opcao_selecionada = 0
    while rodando:
        tela.fill(PRETO)
        desenhar_texto(tela, "Tetris Python Rudy", 40, BRANCO, largura_tela / 2, altura_tela / 4)
        desenhar_texto(tela, "Iniciar jogo", 30, BRANCO if opcao_selecionada == 0 else CINZA, largura_tela / 2, altura_tela / 2)
        desenhar_texto(tela, "Sair", 30, BRANCO if opcao_selecionada == 1 else CINZA, largura_tela / 2, altura_tela / 2 + 50)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    opcao_selecionada = (opcao_selecionada - 1) % 2
                if evento.key == pygame.K_DOWN:
                    opcao_selecionada = (opcao_selecionada + 1) % 2
                if evento.key == pygame.K_RETURN:
                    if opcao_selecionada == 0:
                        return True
                    if opcao_selecionada == 1:
                        return False

        pygame.display.update()
        clock.tick(10)

def desenhar_proxima_peca(tela, peca):
    for i in range(peca.altura):
        for j in range(peca.largura):
            if peca.formato[i][j] == 1:
                x_centro = largura_jogo + (largura_tela - largura_jogo) // 2
                y_centro = 150 + (i * tamanho_bloco / 2)
                pygame.draw.rect(tela, peca.cor, pygame.Rect(x_centro + (j * tamanho_bloco / 2) - tamanho_bloco, y_centro, tamanho_bloco / 2, tamanho_bloco / 2))

def desenhar_layout(tela):
    pygame.draw.line(tela, BRANCO, (largura_jogo, 0), (largura_jogo, altura_tela), 3)
    pygame.draw.rect(tela, BRANCO, pygame.Rect(0, 0, largura_jogo, altura_tela), 3)

def tela_fim():
    rodando = True
    while rodando:
        tela.fill(PRETO)
        desenhar_texto(tela, "Você perdeu. Tente novamente", 40, BRANCO, largura_tela / 2, altura_tela / 2)
        desenhar_texto(tela, "Pressione ENTER para voltar ao menu", 30, BRANCO, largura_tela / 2, altura_tela / 2 + 50)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                return False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    return True

        pygame.display.update()
        clock.tick(10)

# Loop principal do jogo
def main():
    while True:
        if not tela_entrada():
            pygame.quit()
            return

        tabuleiro = [[PRETO for _ in range(largura_jogo // tamanho_bloco)] for _ in range(altura_tela // tamanho_bloco)]

        peca_atual = Peca(largura_jogo // (2 * tamanho_bloco), 0)
        peca_proxima = Peca(largura_jogo // (2 * tamanho_bloco), 0)
        contador_tempo = 0
        pontos = 0
        pausado = False

        rodando = True
        while rodando:
            tela.fill(PRETO)
            contador_tempo += clock.get_rawtime()
            clock.tick()

            if not pausado and contador_tempo / 1000 > velocidade_jogo:
                peca_atual.y += 1
                if verificar_colisao(tabuleiro, peca_atual):
                    peca_atual.y -= 1
                    fixar_peca(tabuleiro, peca_atual)
                    peca_atual = peca_proxima
                    peca_proxima = Peca(largura_jogo // (2 * tamanho_bloco), 0)
                    if verificar_colisao(tabuleiro, peca_atual):
                        rodando = False
                    pontos += limpar_linhas(tabuleiro)
                contador_tempo = 0

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                    pygame.quit()
                    return
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        pausado = not pausado

                    if not pausado:
                        if evento.key == pygame.K_LEFT:
                            peca_atual.x -= 1
                            if verificar_colisao(tabuleiro, peca_atual):
                                peca_atual.x += 1
                        if evento.key == pygame.K_RIGHT:
                            peca_atual.x += 1
                            if verificar_colisao(tabuleiro, peca_atual):
                                peca_atual.x -= 1
                        if evento.key == pygame.K_DOWN:
                            peca_atual.y += 1
                            if verificar_colisao(tabuleiro, peca_atual):
                                peca_atual.y -= 1
                        if evento.key == pygame.K_UP:
                            peca_atual.rotacionar()
                            if verificar_colisao(tabuleiro, peca_atual):
                                for _ in range(3):
                                    peca_atual.rotacionar()

            desenhar_tabuleiro(tela, tabuleiro)
            peca_atual.desenhar(tela)
            desenhar_texto(tela, f"Pontos: {pontos}", 30, BRANCO, largura_jogo + 100, 30)
            desenhar_texto(tela, "Próxima peça:", 30, BRANCO, largura_jogo + 100, 120)
            desenhar_proxima_peca(tela, peca_proxima)
            desenhar_layout(tela)

            if pausado:
                desenhar_texto(tela, "PAUSADO", 60, AMARELO, largura_tela / 2, altura_tela / 2)

            pygame.display.update()

        if not tela_fim():
            break

if __name__ == "__main__":
    main()
