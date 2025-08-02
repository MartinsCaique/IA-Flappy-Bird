import pygame
import os
import random
import neat
import math

# Variáveis da inteligência artificial
ai_jogando = True
geracao = 0
velocidade_acelerada = False  # Para acelerar visualização

pygame.font.init()

# Tamanho da tela
TELA_LARGURA = 400
TELA_ALTURA = 630

# Carregar imagens redimensionadas
IMAGENS_PASSARO = [
    pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'bird1.png')), (34, 24)),
    pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'bird2.png')), (34, 24)),
    pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'bird3.png')), (34, 24))
]

IMAGEM_CANO = pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'pipe.png')), (52, 400))
IMAGEM_CHAO = pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'base.png')), (TELA_LARGURA, 112))
IMAGEM_BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'bg.png')), (TELA_LARGURA, TELA_ALTURA))

FONTE_PONTOS = pygame.font.SysFont('arial', 30)
FONTE_MENU = pygame.font.SysFont('arial', 40)

def obter_configuracao_dificuldade(geracao):
    """Retorna as configurações de dificuldade baseadas na geração atual"""
    config = {
        'movimento_vertical': False,
        'velocidade_multiplicador': 1.0,
        'distancia_canos': 160,
        'obstaculos_falsos': False,
        'canos_invisiveis': False,
        'fase_nome': 'Normal',
        'chance_movimento_vertical': 0,
        'chance_velocidade_aumentada': 0,
        'chance_espaco_reduzido': 0,
        'chance_obstaculos_falsos': 0
    }
    
    if geracao <= 3:
        # Gerações 1-3: Jogo normal
        config['fase_nome'] = 'Normal'
    elif geracao <= 6:
        # Gerações 4-6: Movimento vertical dos canos
        config['movimento_vertical'] = True
        config['chance_movimento_vertical'] = 100  # 100% dos canos se movem
        config['fase_nome'] = 'Movimento Vertical'
    elif geracao <= 9:
        # Gerações 7-9: Velocidade aumentada + movimento vertical aleatório
        config['velocidade_multiplicador'] = 1.5
        config['chance_movimento_vertical'] = 65  # 65% dos canos se movem
        config['fase_nome'] = 'Velocidade + Movimento'
    elif geracao <= 12:
        # Gerações 10-12: Espaço reduzido + fases anteriores aleatórias
        config['chance_movimento_vertical'] = 50  # 50% chance
        config['chance_velocidade_aumentada'] = 65  # 65% chance
        config['chance_espaco_reduzido'] = 100  # 100% chance
        config['fase_nome'] = 'Espaço Reduzido + Mix'
    elif geracao <= 16:
        # Gerações 13-16: Obstáculos falsos + mix de tudo anterior
        config['chance_movimento_vertical'] = 40  # 40% chance
        config['chance_velocidade_aumentada'] = 50  # 50% chance
        config['chance_espaco_reduzido'] = 65  # 65% chance
        config['chance_obstaculos_falsos'] = 30  # 30% chance
        config['fase_nome'] = 'Obstáculos Falsos + Mix'
    else:
        # Geração 17+: Canos invisíveis + mix completo
        config['canos_invisiveis'] = True
        config['chance_movimento_vertical'] = 35  # 35% chance
        config['chance_velocidade_aumentada'] = 45  # 45% chance
        config['chance_espaco_reduzido'] = 55  # 55% chance
        config['chance_obstaculos_falsos'] = 25  # 25% chance
        config['fase_nome'] = 'Canos Invisíveis + Mix Completo'
    
    return config

def menu_principal():
    """Exibe o menu principal e retorna a escolha do usuário"""
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pygame.display.set_caption("Flappy Bird IA")
    relogio = pygame.time.Clock()
    
    while True:
        tela.blit(IMAGEM_BACKGROUND, (0, 0))
        
        # Título
        titulo = FONTE_MENU.render("FLAPPY BIRD IA", True, (255, 255, 255))
        titulo_rect = titulo.get_rect(center=(TELA_LARGURA//2, 150))
        tela.blit(titulo, titulo_rect)
        
        # Opções
        opcao1 = FONTE_PONTOS.render("1 - Jogar Manualmente", True, (255, 255, 255))
        opcao1_rect = opcao1.get_rect(center=(TELA_LARGURA//2, 250))
        tela.blit(opcao1, opcao1_rect)
        
        opcao2 = FONTE_PONTOS.render("2 - IA Jogando", True, (255, 255, 255))
        opcao2_rect = opcao2.get_rect(center=(TELA_LARGURA//2, 300))
        tela.blit(opcao2, opcao2_rect)
        
        instrucoes = pygame.font.SysFont('arial', 20).render("Pressione 1 ou 2 para escolher", True, (200, 200, 200))
        instrucoes_rect = instrucoes.get_rect(center=(TELA_LARGURA//2, 400))
        tela.blit(instrucoes, instrucoes_rect)
        
        pygame.display.update()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    return False  # Jogador manual
                elif evento.key == pygame.K_2:
                    return True   # IA jogando
        
        relogio.tick(30)

class Passaro:
    IMGS = IMAGENS_PASSARO
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem = self.IMGS[0]

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        self.tempo += 1

        deslocamento = self.velocidade * self.tempo + 1.5 * (self.tempo ** 2)

        if deslocamento > 16:
            deslocamento = 16

        if deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        if deslocamento < 0 or self.y < self.altura + 50:
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO

    def desenhar(self, tela):
        self.contagem_imagem += 1

        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*4:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem >= self.TEMPO_ANIMACAO*4:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0

        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        nova_posicao = imagem_rotacionada.get_rect(center=self.imagem.get_rect(topleft=(self.x, self.y)).center)
        tela.blit(imagem_rotacionada, nova_posicao.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)

class Cano:
    VELOCIDADE_BASE = 5

    def __init__(self, x, config_dificuldade=None):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.CANO_BASE = IMAGEM_CANO
        self.passou = False
        self.config_dificuldade = config_dificuldade or {}
        
        # Determinar características deste cano baseado nas chances
        self.tem_movimento_vertical = random.randint(1, 100) <= self.config_dificuldade.get('chance_movimento_vertical', 0)
        self.tem_velocidade_aumentada = random.randint(1, 100) <= self.config_dificuldade.get('chance_velocidade_aumentada', 0)
        self.tem_espaco_reduzido = random.randint(1, 100) <= self.config_dificuldade.get('chance_espaco_reduzido', 0)
        self.eh_falso = random.randint(1, 100) <= self.config_dificuldade.get('chance_obstaculos_falsos', 0)
        
        # Definir distância baseado nas características
        self.distancia = 120 if self.tem_espaco_reduzido else 160
        
        # Para movimento vertical
        self.movimento_vertical = 0
        self.direcao_movimento = 1
        self.amplitude_movimento = random.randint(30, 60)  # Amplitude aleatória
        self.velocidade_movimento = random.uniform(1.5, 3.0)  # Velocidade aleatória
        
        self.definir_altura()

    def definir_altura(self):
        if self.eh_falso:
            # Obstáculos falsos podem ter posições mais variadas
            self.altura = random.randrange(80, 400)
        else:
            self.altura = random.randrange(50, 320)
        
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.distancia

    def mover(self):
        # Movimento horizontal com velocidade individual
        velocidade = self.VELOCIDADE_BASE
        if self.tem_velocidade_aumentada:
            velocidade *= 1.5
        
        self.x -= velocidade
        
        # Movimento vertical se este cano específico tem essa característica
        if self.tem_movimento_vertical:
            self.movimento_vertical += self.velocidade_movimento * self.direcao_movimento
            
            if abs(self.movimento_vertical) >= self.amplitude_movimento:
                self.direcao_movimento *= -1
            
            # Aplicar movimento vertical mantendo limites seguros
            nova_altura = self.altura + self.movimento_vertical
            if 80 <= nova_altura <= 320:
                self.pos_topo = nova_altura - self.CANO_TOPO.get_height()
                self.pos_base = nova_altura + self.distancia

    def desenhar(self, tela):
        if not self.config_dificuldade.get('canos_invisiveis', False):
            # Canos falsos são desenhados com transparência
            if self.eh_falso:
                # Criar superfície com alpha para transparência
                superficie_topo = self.CANO_TOPO.copy()
                superficie_base = self.CANO_BASE.copy()
                superficie_topo.set_alpha(100)  # 100 de 255 = semi-transparente
                superficie_base.set_alpha(100)
                tela.blit(superficie_topo, (self.x, self.pos_topo))
                tela.blit(superficie_base, (self.x, self.pos_base))
            else:
                tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
                tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    def colidir(self, passaro):
        # Obstáculos falsos não causam colisão
        if self.eh_falso:
            return False
            
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        return topo_ponto or base_ponto

class Chao:
    VELOCIDADE_BASE = 5
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO

    def __init__(self, y, config_dificuldade=None):
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA
        self.config_dificuldade = config_dificuldade or {}

    def mover(self):
        # Chão sempre se move na velocidade padrão
        velocidade = self.VELOCIDADE_BASE
        self.x1 -= velocidade
        self.x2 -= velocidade

        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x2 + self.LARGURA

        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA

    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))

def desenhar_tela(tela, passaros, canos, chao, pontos, config_dificuldade=None):
    tela.blit(IMAGEM_BACKGROUND, (0, 0))

    for cano in canos:
        cano.desenhar(tela)

    texto = FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))

    if ai_jogando and config_dificuldade:
        texto = FONTE_PONTOS.render(f"Geração: {geracao}", 1, (255, 255, 255))
        tela.blit(texto, (10, 10))
        
        # Mostrar fase atual
        fase_texto = pygame.font.SysFont('arial', 20).render(f"Fase: {config_dificuldade['fase_nome']}", 1, (255, 255, 0))
        tela.blit(fase_texto, (10, 45))
        
        # Mostrar se está acelerado
        if velocidade_acelerada:
            acelerado_texto = pygame.font.SysFont('arial', 16).render("ACELERADO (A para desativar)", 1, (255, 100, 100))
            tela.blit(acelerado_texto, (10, 70))
        else:
            acelerado_texto = pygame.font.SysFont('arial', 16).render("Pressione A para acelerar", 1, (150, 150, 150))
            tela.blit(acelerado_texto, (10, 70))

    chao.desenhar(tela)

    for passaro in passaros:
        passaro.desenhar(tela)

    pygame.display.update()

def jogo_manual():
    """Jogo para o jogador humano (simples)"""
    passaro = Passaro(100, 300)
    chao = Chao(550)
    canos = [Cano(400)]
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pygame.display.set_caption("Flappy Bird - Jogador Manual")
    pontos = 0
    relogio = pygame.time.Clock()

    rodando = True
    while rodando:
        relogio.tick(30)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    passaro.pular()

        # Mover passaro
        passaro.mover()
        
        # Mover chão
        chao.mover()

        # Processar canos
        adicionar_cano = False
        remover_canos = []

        for cano in canos:
            # Verificar colisão
            if cano.colidir(passaro):
                rodando = False
                break

            # Verificar se passou
            if not cano.passou and cano.x < passaro.x:
                cano.passou = True
                adicionar_cano = True

            cano.mover()

            if cano.x + cano.CANO_TOPO.get_width() < 0:
                remover_canos.append(cano)

        if adicionar_cano:
            pontos += 1
            canos.append(Cano(400))

        for cano in remover_canos:
            canos.remove(cano)

        # Verificar colisão com chão/teto
        if passaro.y + passaro.imagem.get_height() >= chao.y or passaro.y < 0:
            rodando = False

        desenhar_tela(tela, [passaro], canos, chao, pontos)
    
    # Tela de game over
    game_over_texto = FONTE_MENU.render("GAME OVER", True, (255, 0, 0))
    pontos_texto = FONTE_PONTOS.render(f"Pontuação Final: {pontos}", True, (255, 255, 255))
    continuar_texto = pygame.font.SysFont('arial', 20).render("Pressione qualquer tecla para voltar ao menu", True, (200, 200, 200))
    
    tela.blit(game_over_texto, (TELA_LARGURA//2 - game_over_texto.get_width()//2, 200))
    tela.blit(pontos_texto, (TELA_LARGURA//2 - pontos_texto.get_width()//2, 280))
    tela.blit(continuar_texto, (TELA_LARGURA//2 - continuar_texto.get_width()//2, 350))
    pygame.display.update()
    
    # Esperar tecla para continuar
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return
            if evento.type == pygame.KEYDOWN:
                esperando = False

def main(genomas, config): #Fitness Function
    global geracao, velocidade_acelerada
    geracao += 1
    
    # Obter configuração de dificuldade para a geração atual
    config_dificuldade = obter_configuracao_dificuldade(geracao)
    print(f"Geração {geracao} - Fase: {config_dificuldade['fase_nome']}")

    if ai_jogando:
        redes = []
        listas_genomas = []
        passaros = []
        for _, genoma in genomas:
            rede = neat.nn.FeedForwardNetwork.create(genoma, config)
            redes.append(rede)
            genoma.fitness = 0 
            listas_genomas.append(genoma)
            passaros.append(Passaro(100, 300))
    else:
        passaros = [Passaro(100, 300)]

    chao = Chao(550, config_dificuldade)
    canos = [Cano(400, config_dificuldade)]
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pygame.display.set_caption("Flappy Bird IA - Treinamento")
    pontos = 0
    relogio = pygame.time.Clock()

    rodando = True
    while rodando and pontos < 40:  # Limite de 40 pontos por geração
        # Velocidade do jogo baseada na aceleração
        fps = 120 if velocidade_acelerada else 30
        relogio.tick(fps)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_a:  # Tecla A para acelerar/desacelerar
                    velocidade_acelerada = not velocidade_acelerada
                    print(f"Aceleração {'ATIVADA' if velocidade_acelerada else 'DESATIVADA'}")

        indice_cano = 0
        if len(passaros) > 0:
            if len(canos) > 1 and passaros[0].x > (canos[0].x + canos[0].CANO_TOPO.get_width()):
                indice_cano = 1
        else:
            rodando = False
            break

        # Mover coisas
        for i, passaro in enumerate(passaros):
            passaro.mover()
            # Aumentar a fitness do passaro
            listas_genomas[i].fitness += 0.1
            output = redes[i].activate((passaro.y, abs(passaro.y - canos[indice_cano].altura), abs(passaro.y - canos[indice_cano].pos_base)))
            # -1 e 1 -> se o output for > 0.5 então o pássaro pula
            if output[0] > 0.5:
                passaro.pular()

        chao.mover()

        adicionar_cano = False
        remover_canos = []

        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                    passaros.pop(i)
                    if ai_jogando:
                        listas_genomas[i].fitness -= 1
                        listas_genomas.pop(i)
                        redes.pop(i)

                if not cano.passou and cano.x < passaro.x:
                    cano.passou = True
                    adicionar_cano = True

            cano.mover()

            if cano.x + cano.CANO_TOPO.get_width() < 0:
                remover_canos.append(cano)

        if adicionar_cano:
            pontos += 1
            
            # Criar novo cano com características aleatórias baseadas na configuração
            novo_cano = Cano(400, config_dificuldade)
            canos.append(novo_cano)

            for genoma in listas_genomas:
                genoma.fitness += 5

        for cano in remover_canos:
            canos.remove(cano)

        for i, passaro in enumerate(passaros):
            if passaro.y + passaro.imagem.get_height() >= chao.y or passaro.y < 0:
                passaros.pop(i)
                if ai_jogando:
                    listas_genomas.pop(i)
                    redes.pop(i)

        # Só desenhar se não estiver muito acelerado para economizar processamento
        if not velocidade_acelerada or relogio.get_time() > 8:  # Desenha menos quando acelerado
            desenhar_tela(tela, passaros, canos, chao, pontos, config_dificuldade)

def rodar(caminho_config):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                 caminho_config)
    populacao = neat.Population(config)
    populacao.add_reporter(neat.StdOutReporter(True))
    populacao.add_reporter(neat.StatisticsReporter())

    if ai_jogando:
        populacao.run(main, 50)
    else:
        main(None, None)

if __name__ == '__main__':
    pygame.init()
    
    # Menu principal
    while True:
        ai_jogando = menu_principal()
        velocidade_acelerada = False  # Reset da aceleração
        
        if ai_jogando:
            # Resetar geração para IA
            geracao = 0
            caminho = os.path.dirname(__file__)
            caminho_config = os.path.join(caminho, 'configIA.txt')
            rodar(caminho_config)
        else:
            # Jogo manual
            jogo_manual()