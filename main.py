from pgzero.actor import Actor

from random import randint
from pygame import Rect
import math

WIDTH = 800
HEIGHT = 600

# --- Estados do jogo ---
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_GAMEOVER = "gameover"
STATE_WIN = "win"

game_state = STATE_MENU
sound_on = True

# --- Classe de jogador ---
class Player:
    def __init__(self):
        self.images_idle = [Actor(f"player_idle_{i}") for i in range(1, 5)]
        self.images_run = [Actor(f"player_run_{i}") for i in range(1, 7)]
        self.x = 50
        self.y = HEIGHT - 100
        self.vx = 0
        self.vy = 0
        self.on_ground = False
        self.frame_index = 0
        self.frame_delay = 5
        self.frame_count = 0
        self.facing_right = True
        self.state = "idle"  # or "run", "jump"
        self.width = 50
        self.height = 70
        self.lives = 3
        self.rect = Rect(self.x, self.y, self.width, self.height)

    def update(self):
        # Gravidade
        self.vy += 0.5
        self.y += self.vy

        # Mover horizontalmente 
        self.x += self.vx

        # Colisão no chão
        if self.y > HEIGHT - self.height - 50:
            self.y = HEIGHT - self.height - 50
            self.vy = 0
            self.on_ground = True
            if self.state == "jump":
                self.state = "idle"

        # Atualizar reto
        self.rect.topleft = (self.x, self.y)

        # Atualizar quadro de animação
        self.frame_count += 1
        if self.frame_count >= self.frame_delay:
            self.frame_count = 0
            self.frame_index = (self.frame_index + 1) % (len(self.images_idle) if self.state == "idle" else len(self.images_run))

    def draw(self):
        if self.state == "idle":
            img = self.images_idle[self.frame_index]
        elif self.state == "run":
            img = self.images_run[self.frame_index]
        else:  # jump
            img = self.images_idle[0]

        img.x = self.x + self.width // 2
        img.y = self.y + self.height // 2

        if not self.facing_right:
            img.angle = 0
            img._surf = pgzrun.actor.load(img._orig_surf).transform.flip(True, False)
        else:
            img.angle = 0

        img.draw()

    def move_left(self):
        self.vx = -4
        self.facing_right = False
        if self.on_ground:
            self.state = "run"

    def move_right(self):
        self.vx = 4
        self.facing_right = True
        if self.on_ground:
            self.state = "run"

    def stop(self):
        self.vx = 0
        if self.on_ground:
            self.state = "idle"

    def jump(self):
        if self.on_ground:
            self.vy = -10
            self.on_ground = False
            self.state = "jump"

# --- Classe inimiga ---
class Enemy:
    def __init__(self, x1, x2, y):
        self.images = [Actor(f"enemy_{i}") for i in range(1, 5)]
        self.x1 = x1
        self.x2 = x2
        self.x = x1
        self.y = y
        self.speed = 2
        self.frame_index = 0
        self.frame_delay = 7
        self.frame_count = 0
        self.moving_right = True
        self.rect = Rect(self.x, self.y, 50, 70)

    def update(self):
        if self.moving_right:
            self.x += self.speed
            if self.x > self.x2:
                self.moving_right = False
        else:
            self.x -= self.speed
            if self.x < self.x1:
                self.moving_right = True

        # Atualizar reto
        self.rect.topleft = (self.x, self.y)

        # Animar
        self.frame_count += 1
        if self.frame_count >= self.frame_delay:
            self.frame_count = 0
            self.frame_index = (self.frame_index + 1) % len(self.images)

    def draw(self):
        img = self.images[self.frame_index]
        img.x = self.x + 25
        img.y = self.y + 35
        img.draw()

# --- Classe de plataforma ---
class Platform:
    def __init__(self, x, y, width, height):
        self.rect = Rect(x, y, width, height)

    def draw(self):
        screen.draw.filled_rect(self.rect, "darkgreen")

# --- Classe de botão ---
class Button:
    def __init__(self, rect, text):
        self.rect = rect
        self.text = text

    def draw(self):
        screen.draw.filled_rect(self.rect, "grey")
        screen.draw.textbox(self.text, self.rect, color="white", fontsize=30)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# --- Inicializar objetos do jogo ---

player = Player()

enemies = [
    Enemy(200, 400, HEIGHT - 120),
    Enemy(500, 700, HEIGHT - 120)
]

platforms = [
    Platform(0, HEIGHT - 50, WIDTH, 50),
    Platform(150, HEIGHT - 150, 200, 20),
    Platform(450, HEIGHT - 250, 200, 20),
]

# Botões para menu
start_button = Button(Rect(300, 200, 200, 50), "Start Game")
sound_button = Button(Rect(300, 300, 200, 50), "Sound: ON")
quit_button = Button(Rect(300, 400, 200, 50), "Quit")

# --- Funções do jogo ---

def draw():
    screen.clear()
    if game_state == STATE_MENU:
        screen.draw.text("Bug Hero", center=(WIDTH // 2, 100), fontsize=60)
        start_button.draw()
        sound_button.draw()
        quit_button.draw()

    elif game_state == STATE_PLAYING:
        for plat in platforms:
            plat.draw()
        player.draw()
        for enemy in enemies:
            enemy.draw()
        # HUD
        screen.draw.text(f"Lives: {player.lives}", (10, 10), fontsize=30)
        screen.draw.text(f"X: {int(player.x)}", (10, 40), fontsize=20)

    elif game_state == STATE_GAMEOVER:
        screen.draw.text("Game Over!", center=(WIDTH // 2, HEIGHT // 2), fontsize=60, color="red")
        screen.draw.text("Press R to return to menu", center=(WIDTH // 2, HEIGHT // 2 + 50), fontsize=30)

    elif game_state == STATE_WIN:
        screen.draw.text("You Win!", center=(WIDTH // 2, HEIGHT // 2), fontsize=60, color="green")
        screen.draw.text("Press R to return to menu", center=(WIDTH // 2, HEIGHT // 2 + 50), fontsize=30)

def update():
    global game_state

    if game_state == STATE_PLAYING:
        player.update()
        for enemy in enemies:
            enemy.update()
        check_collisions()
        check_win_loss()

def on_key_down(key):
    if game_state == STATE_PLAYING:
        if key == keys.LEFT:
            player.move_left()
        elif key == keys.RIGHT:
            player.move_right()
        elif key == keys.SPACE:
            player.jump()

    if game_state in (STATE_GAMEOVER, STATE_WIN):
        if key == keys.R:
            reset_game()

def on_key_up(key):
    if game_state == STATE_PLAYING:
        if key in (keys.LEFT, keys.RIGHT):
            player.stop()

def on_mouse_down(pos):
    global game_state, sound_on

    if game_state == STATE_MENU:
        if start_button.is_clicked(pos):
            game_state = STATE_PLAYING
        elif sound_button.is_clicked(pos):
            sound_on = not sound_on
            sound_button.text = "Sound: ON" if sound_on else "Sound: OFF"
        elif quit_button.is_clicked(pos):
            exit()

def check_collisions():
    # Colisão da plataforma do jogador
    player.on_ground = False
    for plat in platforms:
        if player.rect.colliderect(plat.rect) and player.vy >= 0:
            if player.y + player.height <= plat.rect.y + 10:
                player.y = plat.rect.y - player.height
                player.vy = 0
                player.on_ground = True
                if player.state == "jump":
                    player.state = "idle"
                player.rect.topleft = (player.x, player.y)

    # Colisão jogador-inimigo
    for enemy in enemies:
        if player.rect.colliderect(enemy.rect):
            player.lives -= 1
            player.x = 50
            player.y = HEIGHT - 100
            if player.lives <= 0:
                global game_state
                game_state = STATE_GAMEOVER

def check_win_loss():
    global game_state
    # Condição de vitória: o jogador alcança a borda direita
    if player.x > WIDTH - player.width:
        game_state = STATE_WIN

def reset_game():
    global player, enemies, game_state
    player.lives = 3
    player.x = 50
    player.y = HEIGHT - 100
    player.vx = 0
    player.vy = 0
    game_state = STATE_MENU



import pgzrun
pgzrun.go()

