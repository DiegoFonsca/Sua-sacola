import pygame
import os
import sys
import random


# ================= CAMINHO SEGURO =================
def caminho_arquivo(relativo):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relativo)


def carregar_recorde():
    try:
        with open(caminho_arquivo("recorde.txt"), "r") as f:
            return int(f.read())
    except:
        return 0

def salvar_recorde(valor):
    with open(caminho_arquivo("recorde.txt"), "w") as f:
        f.write(str(valor))


# ================= INIT =================
pygame.init()
pygame.mixer.init()

# ================= TELA =================
largura = 800
altura = 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo Sua Sacola")

clock = pygame.time.Clock()

# ================= CORES =================
branco = (255, 255, 255)
azul = (0, 120, 255)

# ================= FUNDO =================
fundo_img = pygame.image.load(caminho_arquivo("imagens/fundo.png")).convert()
fundo_img = pygame.transform.scale(fundo_img, (largura, altura))

# ================= MÚSICA =================
pygame.mixer.music.load(caminho_arquivo("imagens/musica.mp3"))
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

# ================= ITENS =================
itens_imgs = []
for i in range(1, 6):
    img = pygame.image.load(caminho_arquivo(f"imagens/item{i}.png")).convert_alpha()
    img = pygame.transform.smoothscale(img, (60, 60))
    itens_imgs.append(img)

item_img = random.choice(itens_imgs)
obj_largura = item_img.get_width()
obj_altura = item_img.get_height()

obj_x = random.randint(0, largura - obj_largura)
obj_y = 0
obj_velocidade = 5

# ================= PLAYER (LOGO) =================
logo_original = pygame.image.load(caminho_arquivo("imagens/logo.png")).convert_alpha()

nova_largura = 80
proporcao = nova_largura / logo_original.get_width()
nova_altura = int(logo_original.get_height() * proporcao)

logo_img = pygame.transform.smoothscale(logo_original, (nova_largura, nova_altura))

player_x = largura // 2 - nova_largura // 2
player_y = altura - nova_altura - 10
player_velocidade = 20

# ================= TEXTO =================
fonte = pygame.font.SysFont("Arial Bold", 60)

fonte_credito = pygame.font.SysFont("Arial Black", 14)
credito_texto = fonte_credito.render("Desenvolvido por Diego", True, (0,0,0))
credito_x = largura - credito_texto.get_width() - 10
credito_y = altura - credito_texto.get_height() - 10
recorde = carregar_recorde()





pontuacao = 0
estado_jogo = "jogando"
aceleracao = 0.05

def desenhar_game_over():
    t1 = fonte.render("GAME OVER", True, azul)
    t2 = fonte.render("ESPACO - continuar", True, (0,0,0))
    t3 = fonte.render("Q - sair", True, (0,0,0))

    tela.blit(t1, (largura//2 - 100, altura//2 - 60))
    tela.blit(t2, (largura//2 - 160, altura//2))
    tela.blit(t3, (largura//2 - 40, altura//2 + 60))

def resetar_jogo():
    global obj_x, obj_y, obj_velocidade, pontuacao, item_img
    obj_y = 0
    obj_velocidade = 7
    pontuacao = 0
    item_img = random.choice(itens_imgs)
    obj_x = random.randint(0, largura - item_img.get_width())

# ================= LOOP PRINCIPAL =================
while True:
    tela.blit(fundo_img, (0, 0))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if estado_jogo == "game_over" and evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_q:
                pygame.quit()
                sys.exit()
            if evento.key == pygame.K_SPACE:
                resetar_jogo()
                estado_jogo = "jogando"



    if estado_jogo == "jogando":
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            player_x -= player_velocidade
        if teclas[pygame.K_RIGHT]:
            player_x += player_velocidade

        player_x = max(0, min(player_x, largura - nova_largura))

        obj_y += obj_velocidade

        player_rect = pygame.Rect(player_x, player_y, nova_largura, nova_altura)
        obj_rect = pygame.Rect(obj_x, obj_y, item_img.get_width(), item_img.get_height())

        if player_rect.colliderect(obj_rect):
            pontuacao += 1
            obj_velocidade += aceleracao
            item_img = random.choice(itens_imgs)
            obj_x = random.randint(0, largura - item_img.get_width())
            obj_y = 0

        if obj_y > altura:
            if pontuacao > recorde:
                recorde = pontuacao
                salvar_recorde(recorde)
            estado_jogo = "game_over"


    tela.blit(logo_img, (player_x, player_y))
    tela.blit(item_img, (obj_x, obj_y))

    texto_score = fonte.render(f"Pontos: {pontuacao}", True, branco)
    texto_recorde = fonte.render(f"Recorde: {recorde}", True, branco)

    tela.blit(texto_score, (10, 10))
    tela.blit(texto_recorde, (10, 45))

    if estado_jogo == "game_over":
        desenhar_game_over()
    tela.blit(credito_texto, (credito_x, credito_y))

    pygame.display.update()
    clock.tick(90)
