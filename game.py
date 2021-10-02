import pygame, sys, random

#Function of game:
def draw_floor():    
    screen.blit(floor, (floor_x_pos,650))
    screen.blit(floor, (floor_x_pos + 432, 650))  
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom > 600:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (501,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop = (501,random_pipe_pos - 690))
    return bottom_pipe, top_pipe
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 3
    return pipes
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            print('Collise pipe')
            hit_sound.play()
            return False
        if bird_rect.top <= -75 or bird_rect.bottom >= 650:
            print('Over space')
            return False
    return True
def rotate_bird(bird_tmp):
    new_bird = pygame.transform.rotozoom(bird_tmp,-3* bird_movement, 1)
    return new_bird
def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (150, bird_rect.centery))
    return new_bird, new_bird_rect
def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (216, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (216, 100))
        screen.blit(score_surface, score_rect)
        
        high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center = (216, 600))
        screen.blit(high_score_surface, high_score_rect)
def update_high_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


pygame.mixer.pre_init(frequency = 44100, size = -16, channels = 2, buffer = 512) 
pygame.init()
screen = pygame.display.set_mode((432,768))
clock = pygame.time.Clock()

game_font = pygame.font.Font('04B_19.ttf', 40)

#Variable game
gravity = 0.25
bird_movement = 0
pipe_height = [300, 400 , 450]

game_play = True
game_active = False


score = 0
high_score = 0
#insert background:
bg = pygame.image.load('F:/Code_fun/Project_FlappyBird/FileGame/assets/background-night.png').convert()
bg = pygame.transform.scale2x(bg)
bg_x_pos = 0

#insert floor:
floor = pygame.image.load('F:/Code_fun/Project_FlappyBird/FileGame/assets/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0

#Create object bird:
bird_down = pygame.transform.scale2x(pygame.image.load('F:/Code_fun/Project_FlappyBird/FileGame/assets/yellowbird-downflap.png').convert_alpha())
bird_mid  = pygame.transform.scale2x(pygame.image.load('F:/Code_fun/Project_FlappyBird/FileGame/assets/yellowbird-midflap.png').convert_alpha())
bird_up   = pygame.transform.scale2x(pygame.image.load('F:/Code_fun/Project_FlappyBird/FileGame/assets/yellowbird-upflap.png').convert_alpha())
bird_list = [bird_down, bird_mid,  bird_up]
bird_index = 0
bird = bird_list[bird_index]

bird_rect = bird.get_rect(center = (216,484))

#Create timer-bird
bird_flap = pygame.USEREVENT + 1
pygame.time.set_timer(bird_flap, 100)


#Create pipe:
pipe_surface = pygame.image.load('F:/Code_fun/Project_FlappyBird/FileGame/assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
#Create timer-pipe:
spawn_pipe = pygame.USEREVENT
pygame.time.set_timer(spawn_pipe, 2000)

#Create game_state UI:
game_begin_surface = pygame.transform.scale2x(pygame.image.load('F:/Code_fun/Project_FlappyBird/FileGame/assets/message.png').convert_alpha())
game_begin_rect = game_begin_surface.get_rect(center = (216, 384))

game_over_surface = pygame.transform.scale2x(pygame.image.load('F:/Code_fun/Project_FlappyBird/FileGame/assets/gameover.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (216, 384))

#Insert music:
flap_sound = pygame.mixer.Sound('F:\Code_fun\Project_FlappyBird\FileGame\sound\sfx_wing.wav')
hit_sound = pygame.mixer.Sound('F:\Code_fun\Project_FlappyBird\FileGame\sound\sfx_hit.wav')
point_sound = pygame.mixer.Sound('F:\Code_fun\Project_FlappyBird\FileGame\sound\sfx_point.wav')

#Loop game:
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_play and not game_active:
                game_play = False
                game_active = True
                pipe_list.clear()
            if event.key == pygame.K_SPACE and game_active:
                print("Fly up!")
                bird_movement = 0
                bird_movement = -6.9
                flap_sound.play()
                
            if event.key == pygame.K_SPACE and not game_play and not game_active:
                game_play = True
                bird_rect.center = (216, 484)
                bird_movement = 0
                score = 0
                game_begin_rect.center = (216,432)
                
        if event.type == spawn_pipe:
            pipe_list.extend(create_pipe())
        if event.type == bird_flap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()
    #Draw background:
    
    screen.blit(bg, (bg_x_pos,0))
    if game_play:
        screen.blit(game_begin_surface, game_begin_rect)
    else:
        if game_active:
            rotated_bird = rotate_bird(bird)
            #Pipe move:
            pipe_list = move_pipe(pipe_list)
            #Draw pipe
            draw_pipe(pipe_list)
            
            #Draw score:
            score_display('main_game')
            #Increase score:
            for pipe in pipe_list:
                if pipe.centerx == bird_rect.centerx:
                    score += 0.5  
                    point_sound.play()          
            #Draw bird
            screen.blit(rotated_bird, bird_rect)   
            
            bird_movement += gravity    
            bird_rect.centery += bird_movement

            game_active = check_collision(pipe_list)
        else:
            screen.blit(game_over_surface, game_over_rect)
            high_score = update_high_score(score, high_score)
            score_display('game_over')
    draw_floor()
    floor_x_pos -= 1
    if floor_x_pos < -432:
        floor_x_pos = 0
    if bg_x_pos < -432:
        bg_x_pos = 0
    
    pygame.display.update()
    clock.tick(120)