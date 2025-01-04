import pygame
import sys
import random

# Pygame'i başlat
pygame.init()

# Ekran boyutları
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Flappy Bird")

# Kuş görsellerini yükle
bird_image = pygame.image.load("assets/sultan_papagani.png")
bird_image = pygame.transform.scale(bird_image, (50, 50))  # Görseli boyutlandır

bird_image2 = pygame.image.load("assets/sultan_papagani2.png")
bird_image2 = pygame.transform.scale(bird_image2, (50, 50))  # İkinci görseli boyutlandır

mountain_image = pygame.image.load("assets/mountain.png")
cloud_image = pygame.image.load("assets/cloud.png")
# Görselleri boyutlandır (istenen boyutlara göre ayarlayın)
mountain_image = pygame.transform.scale(mountain_image, (100, 400))  # Örnek boyut
cloud_image = pygame.transform.scale(cloud_image, (200, 200))  # Örnek boyut

# Renkler
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
# Her seviye için farklı yeşil tonları (açıktan koyuya)
PIPE_COLORS = {
    1: (144, 238, 144),  # Açık yeşil
    2: (34, 139, 34),    # Orta yeşil
    3: (0, 100, 0),      # Koyu yeşil
    4: (0, 80, 0),       # Daha koyu yeşil
    5: (0, 60, 0)        # En koyu yeşil
}
RED = (255, 0, 0)
SKY_BLUE = (135, 206, 235)

# Kuş pozisyonu
bird_x, bird_y = 100, 300
velocity = 0
gravity = 0.5
jump = -10

# Oyun seviyesi ve zorluk
level = 1
pipes_passed = 0
PIPES_PER_LEVEL = 3  # Her seviye için 3 çubuk
total_pipes_spawned = 0  # Toplam oluşturulan boru sayısı

# Engel parametreleri
pipe_width = 50
pipe_gaps = {
    1: 400,  # En kolay seviye
    2: 350,  # Biraz daha zor
    3: 300,  # Orta zorluk
    4: 250,  # Zor
    5: 200   # En zor seviye
}  # Her seviye için farklı boşluk mesafeleri
pipe_x = WIDTH
pipe_height = random.randint(150, 400)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 0)  # Başlangıçta zamanlayıcıyı kapalı tut

def start_pipe_spawn():
    pygame.time.set_timer(SPAWNPIPE, 3000)  # Zamanlayıcıyı başlat

def stop_pipe_spawn():
    pygame.time.set_timer(SPAWNPIPE, 0)  # Zamanlayıcıyı durdur

# Puan
score = 0
font = pygame.font.Font(None, 36)

def create_pipe():
    height = random.randint(200, 400)
    bottom_pipe = pygame.Rect(WIDTH, height, pipe_width, HEIGHT - height)
    
    # Seviye 1'de sadece alt borular
    if level == 1:
        return [bottom_pipe]
    
    # Diğer seviyelerde üst ve alt borular
    gap = pipe_gaps[level]
    top_pipe = pygame.Rect(WIDTH, 0, pipe_width, height - gap)
    return [bottom_pipe, top_pipe]


def move_pipes(pipes):
    for pipe in pipes:
        pipe.x -= 3
    return [pipe for pipe in pipes if pipe.x > -pipe_width]

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.y == 0:  # Üst boru (bulut)
            # Bulutun alt kısmı borunun yüksekliğine göre ayarlanıyor
            cloud_y = pipe.height - cloud_image.get_height()
            screen.blit(cloud_image, (pipe.x, cloud_y))
        else:  # Alt boru (dağ)
            # Dağ görselini borunun genişliğine göre ortalama
            mountain_x = pipe.x - (mountain_image.get_width() - pipe_width) // 2
            screen.blit(mountain_image, (mountain_x, pipe.y))

def check_collision(pipes, bird_rect):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return True
    if bird_rect.top <= 0 or bird_rect.bottom >= HEIGHT:
        return True
    return False

def reset_game():
    global game_active, bird_y, velocity, score, level, pipes_passed, total_pipes_spawned
    game_active = True
    pipe_list.clear()
    bird_y = 300
    velocity = 0
    score = 0
    level = 1
    pipes_passed = 0
    total_pipes_spawned = 0
    start_pipe_spawn()  # Oyun başladığında zamanlayıcıyı başlat

# Oyun döngüsü
running = True
game_active = True
start_pipe_spawn()  # İlk başlangıçta zamanlayıcıyı başlat

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                velocity = jump
            if event.key == pygame.K_SPACE and not game_active:
                reset_game()
        if event.type == SPAWNPIPE and game_active:
            if total_pipes_spawned < PIPES_PER_LEVEL and len(pipe_list) < PIPES_PER_LEVEL:
                pipe_list.extend(create_pipe())
                total_pipes_spawned += 1
                if total_pipes_spawned >= PIPES_PER_LEVEL:
                    stop_pipe_spawn()  # Yeterli boru oluşturulduğunda zamanlayıcıyı durdur

    if game_active:
        # Fizik
        velocity += gravity
        bird_y += velocity

        # Engelleri hareket ettir
        old_pipe_count = len(pipe_list)
        pipe_list = move_pipes(pipe_list)
        
        # Geçilen boruları say
        if old_pipe_count > len(pipe_list):
            pipes_passed += 1
            score += 1
            
            # Seviye kontrolü
            if pipes_passed >= PIPES_PER_LEVEL and level < 5:  # 5 seviyeye kadar çıkabilir
                level += 1
                pipes_passed = 0
                total_pipes_spawned = 0
                start_pipe_spawn()  # Yeni seviyede zamanlayıcıyı başlat

        # Çarpışma kontrolü
        bird_rect = pygame.Rect(bird_x - 25, bird_y - 25, 50, 50)

        if check_collision(pipe_list, bird_rect):
            game_active = False
            stop_pipe_spawn()  # Oyun bittiğinde zamanlayıcıyı durdur

    # Ekranı temizle ve çizim yap
    screen.fill(SKY_BLUE)
    
    if game_active:
        # Kuş - Zıplama durumuna göre farklı görsel kullan
        if velocity < 0:  # Yukarı doğru hareket (zıplama)
            screen.blit(bird_image2, (bird_x - 25, bird_y - 25))
        else:  # Aşağı doğru hareket (düşme)
            screen.blit(bird_image, (bird_x - 25, bird_y - 25))
        
        # Engeller
        draw_pipes(pipe_list)
        # Skor ve Seviye
        score_text = font.render(f'Skor: {score}', True, WHITE)
        level_text = font.render(f'Seviye: {level}', True, WHITE)
        pipes_text = font.render(f'Borular: {pipes_passed}/{PIPES_PER_LEVEL}', True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 50))
        screen.blit(pipes_text, (10, 90))
    else:
        # Oyun bitiş ekranı
        game_over_text = font.render('OYUN BİTTİ - TEKRAR BAŞLAMAK İÇİN BOŞLUK', True, WHITE)
        score_text = font.render(f'Skor: {score}', True, WHITE)
        level_text = font.render(f'Ulaşılan Seviye: {level}', True, WHITE)
        screen.blit(game_over_text, (WIDTH//2 - 200, HEIGHT//2))
        screen.blit(score_text, (WIDTH//2 - 50, HEIGHT//2 + 50))
        screen.blit(level_text, (WIDTH//2 - 70, HEIGHT//2 + 100))

    pygame.display.flip()
    clock.tick(30)  # FPS
