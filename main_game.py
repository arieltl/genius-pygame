#importa dependências
import pygame
import pygame.gfxdraw
from random import randint
from math import pi,sin,cos
from support_classes import Circle, Note
from CONFIG import HEIGHT,WIDTH, DRAW_RADIUS, COLORS, FREQUENCIES, QUIT, END, INIT,FPS
import os
import json

#definindo a classe GeniusGame (lógica do jogo) 
class GeniusGame:
    def __init__(self, window, manager):
        self.window = window
        self.manager = manager
        luci = pygame.image.load(os.path.join("sprites","luci.png")).convert_alpha()
        self.luci_sound = pygame.mixer.Sound(os.path.join("sprites","scream.ogg"))
        self.buzzer_sound = pygame.mixer.Sound(os.path.join("sprites","buzzer.wav"))
        height = HEIGHT-50
        width = int(luci.get_width() * height / luci.get_height())
        self.luci = pygame.transform.scale(luci,(width,height))

    def start_game(self):
        #reseta valor de propriedades para comecar um novo jogo
        self.sequence = []
        self.input_sequence = []
        self.circles = []
        self.actions_list = []
        self.current_index = 0
        self.awaiting_input = False
        self.difficulty = self.manager.difficulty
        self.waiting_time = 300
        self.flash_time = 1000
        self.game_over = False
        #pega record do modo no arquivo JSON
        self.get_highscore()
        #inicia um jogo
        return self.game_loop()

    #adiciona um botão na sequência
    def increment_sequence(self):
        #ajusta dificuladade de acordo com modo de jogo
        self.increase_difficulty()
        self.sequence.append(randint(0, len(self.circles)-1))
        #reproduz a sequência correta
        self.play_sequence()
        
    def increase_difficulty(self):
        round = len(self.sequence)
        #adicona novos botões de acordo com modo de jogo
        if self.difficulty[1] and round % 3 == 0 and round !=0 and len(self.circles) < 8:
            next_i = len(self.circles)
            self.circles.append(Circle(50,COLORS[next_i],FREQUENCIES[next_i]))
            print(round)
            print(COLORS[round])
            self.calculate_scene()
            self.draw_scene()
       
        #diminui tempo de reprodução da sequência de acordo com modo de jogo
        if self.difficulty[0] and round % 2 == 0 and round !=0:
            self.flash_time = int(self.flash_time * (0.85 if self.flash_time > 300 else 1))
            self.waiting_time = int(self.waiting_time * (0.95 if self.waiting_time > 200 else 1))
        
   #reproduz a sequência correta
    def play_sequence(self):
        actions = []
        for i in self.sequence:
            action = {"function": self.circles[i].flash, "arguments": (self.window, self.flash_time), "delay": self.waiting_time}
            action2 = {"function": self.draw_scene, "delay": self.flash_time}
            
            actions.append(action)
            actions.append(action2)
        await_input = {"function": self.enable_input, "arguments": (True,), "delay": 0}
        self.actions_list += actions + [await_input]

    #lida com input nos botões
    def new_input(self, circle):
        self.enable_input(False)
        #caso o tenha pressionado o botão correto
        if self.circles.index(circle) == self.sequence[self.current_index]:
            #piscar o botão
            circle.flash(self.window, 300)
            await_input = {"function": self.enable_input, "arguments": (True,), "delay": 0}
            action = {"function": self.draw_scene, "delay":300}
            self.actions_list.append(action)
            #esperar próximo input ou iniciar próxima rodada
            self.current_index += 1
            if self.current_index == len(self.sequence):
                self.current_index = 0
                self.enable_input(False)
                action = {"function": self.increment_sequence, "delay":500}
                self.actions_list.append(action)
            else:
                self.actions_list.append(await_input)
        else:
            #caso tenha pressionado botão incorreto encerrar jogo
            self.end_game()
            


    #habilita e desabilita input do usuário
    def enable_input(self,enable):
        self.awaiting_input = enable

    #posiciona os botões ao redor de uma circuferência imaginária com raio
    # DRAW_RADIUS e com espaçamentos em ângulo iguais
    def calculate_scene(self):
        for i, circle in enumerate(self.circles):
            angle = i*2*pi/len(self.circles) + pi/4
            x = int(WIDTH/2 + cos(angle) * DRAW_RADIUS)
            y = int(HEIGHT/2 + sin(angle) * DRAW_RADIUS)
            circle.move_to((x, y))

    #desenha os elementos da cena na tela
    def draw_scene(self):
        self.window.fill((0, 0, 0))
        for circle in self.circles:
            circle.draw(self.window)
        font = pygame.font.SysFont(None, 48)
        score_t = font.render("Score: {}".format(max(len(self.sequence)-1,0)), True, (255, 255, 255))
        highscore_t = font.render("Your highscore: {}".format(self.highscore), True, (255, 255, 255))
        self.window.blit(score_t, (20, 20))
        self.window.blit(highscore_t, (20, 30 + score_t.get_height()))


    # encerra o jogo
    def end_game(self):
        #aparece tela vermelha por 1.5 segundos
        self.window.fill((255,0,0))
        action = {"function":self.set_game_over,"arguments":(True,),"delay":1500}
        self.actions_list.append(action)
        #caso modo seja "lucianius" aparece imagem e toca som de grito
        if self.difficulty == [True, True]:
            self.window.blit(self.luci,(WIDTH/2-self.luci.get_width()/2, HEIGHT/2-self.luci.get_height()/2))
            self.luci_sound.play()
        else:
            #caso contrário toca som de buzina
            self.buzzer_sound.play()
        self.set_highscore()

    #finaliza o jogo
    def set_game_over(self,over):
        self.game_over = over
        

    #pega o highscore do arquivo JSON
    def get_highscore(self):
        with open("scores.json", "r") as file:
            data = json.load(file)
            self.highscore = data[str(self.difficulty)]

    #define o highscore
    def set_highscore(self):
        #caso bata o record salve a pontuação no arquivo JSON
        score = max(0,len(self.sequence)-1)
        if score > self.highscore:
            with open("scores.json", "r+") as file:
                data = json.load(file)
                data.update({str(self.difficulty) : score})
                file.seek(0)
                json.dump(data, file,indent=4)
                file.truncate()

    #loop de jogo
    def game_loop(self):
        #cria botões inicias
        for i in range(4):
            self.circles.append(Circle(50,COLORS[i], FREQUENCIES[i]))
            print(COLORS[i])
        self.calculate_scene()
        self.draw_scene()
        #adiciona primerio círculo a sequência correta 
        self.increment_sequence()

        #variáveis para sistema de delay de funções
        running_action = False
        delay = 0
        timer = 0
        clock = pygame.time.Clock()

        while True:
            # ----- Trata eventos
            dt = clock.tick(FPS)
            # ir para tela game over caso jogo tenha acabado
            if self.game_over == True:
                return END

            #sistema de delay que não deixa jogo irresponsivel
            if not running_action and len(self.actions_list) > 0:
                delay = self.actions_list[0]["delay"]
                timer = 0
                running_action = True

            if running_action:
                timer += dt
                if timer >= delay:
                    action = self.actions_list[0]
                    if "arguments" in action:
                        action["function"](*action["arguments"])
                    else:
                        action["function"]()
                    if len(self.actions_list) > 0:
                        del self.actions_list[0]
                    running_action = False

            # tratar dos eventos
            for event in pygame.event.get():
                #fechar jogo caso feche a janela
                if event.type == pygame.QUIT:
                    return QUIT
                #ir para menu principal caso aperte esc
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return INIT
                #lidar com botão pressionado
                elif self.awaiting_input and event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            
                            for circle in self.circles:
                                if circle.colision(event.pos):
                                    self.new_input(circle)                
            
            pygame.display.update()  # Mostra o novo frame para o jogador
