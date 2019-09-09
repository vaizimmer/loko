import arcade

linhas_palavras = 20
lista_palav = ("pa", "la", "ta", "pd", "rg", "uh", "ta"
        )

class Word:
    def __init__(self, word, linha, screen_width, screen_height):
        self.word = word
        self.linha = linha
        self.x = screen_width
        self.y = (int((screen_height - 50) / linhas_palavras) * linha) + 50
        self.in_focus = False
    
    def draw(self):
        arcade.draw_text(self.word, self.x, self.y,
            arcade.color.DODGER_BLUE if self.in_focus else arcade.color.WHITE,
        14)
    
    def attack(self):
        self.word = self.word[1:]