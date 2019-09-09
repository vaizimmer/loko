import os
import random
import shelve
from enum import Enum

import arcade

import src.word


class GameStates(Enum):
    game_over = 0
    rodando = 1

class Game(arcade.Window):
    def __init__(self, largura, altura):
        super().__init__(largura, altura, title="Hulk agiota")
        arcade.set_background_color((5, 2, 27))

        self.largura = largura
        self.altura = altura

        

        self.pontos = int()
        self.vidas = int()
        self.estado = None
        self.palavra_foco = None 

        self.lista_palav = set()
        

    def setup(self):
        self.pontos = 0
        self.vidas = 3
        self.estado = GameStates.rodando
        self.palavra_foco = None
        
        
        self.lista_palav = set()

        for _ in range(5):
            self.criar_jogo()
        
            
    
    def fazer_gameover(self):
        arcade.draw_text("Game Over",
            self.largura / 2, (self.altura / 2) + 68,
            arcade.color.WHITE, 54,
            align="center", anchor_x="center", anchor_y="center"
        ) 

        arcade.draw_text("espaço",
            self.largura / 2, (self.altura / 2),
            arcade.color.WHITE, 24,
            align="center", anchor_x="center", anchor_y="center"
        )

        arcade.draw_text(f"pontos : {self.pontos}", 15, 15,arcade.color.WHITE, 14,)
        
    
    def info_tela(self):
        for word in self.lista_palav:
            word.draw()
        
        arcade.draw_text(f"pontos : {self.pontos}", 15, 15, arcade.color.WHITE, 14)
        arcade.draw_text(f"vida : {self.vidas}", self.largura - 15, 15, arcade.color.WHITE, 14, align="right", anchor_x="right", anchor_y="baseline")

    def on_draw(self):
        arcade.start_render()

        if self.estado == GameStates.rodando:
            self.info_tela()
        else:
            self.fazer_gameover()
    
    def criar_jogo(self):
       
        linha = int()
        linha_utilizada = set()
        while True:
            linha = random.randrange(src.word.linhas_palavras)
            for word in self.lista_palav:
                linha_utilizada.add(word.linha)
            if linha not in linha_utilizada:
                break
        
       
        occupied_chars = set()
        for word in self.lista_palav:
            occupied_chars.add(word.word[0])
        rand_word = str()
        while True:
            rand_word = random.choice(src.word.lista_palav)
            if rand_word[0] not in occupied_chars:
                break
        
        self.lista_palav.add(src.word.Word(rand_word, linha, self.largura, self.altura))

    
    
    def update(self, delta_time):
        """ Movement and game logic """
       

        if self.estado == GameStates.rodando:
            for word in self.lista_palav:
                word.x -= 100 * delta_time
                if word.x < 0:
                    if self.palavra_foco == word:
                        self.palavra_foco = None

                    self.vidas -= 1

                    self.lista_palav.discard(word)
                    self.criar_jogo()
            
            if self.vidas <= 0:
               self.estado = GameStates.game_over
    
    def on_key_press(self, key, modifiers):
        if key > 127:
            return

        if self.estado == GameStates.game_over and key == 32:
            self.setup()
            self.estado = GameStates.RUNNING

        if self.palavra_foco == None:
            for word in self.lista_palav:
                if word.word[0] == chr(key):
                    self.palavra_foco = word

                    word.attack()
                    word.in_focus = True
                    break
        else:
            if self.palavra_foco.word[0] == chr(key):
                    self.palavra_foco.attack()
                    if self.palavra_foco.word == "":
                        self.lista_palav.discard(self.palavra_foco)
                        self.palavra_foco = None
                        self.pontos += 1
                        self.criar_jogo()