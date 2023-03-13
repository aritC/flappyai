import pygame
import neat
import neat.nn
import time
import os
from bird import Bird
from pipe import Pipe
from base import Base

WIN_WIDTH = 500
WIN_HEIGHT = 800
GEN = 0

BG_IMG = pygame.transform.scale2x((pygame.image.load(os.path.join("assets","bg.png" ))))
pygame.font.init()
SCORE_FONT = pygame.font.SysFont("impact", 50)

def draw_window(win, birds, pipes, base, score):
    global GEN
    win.blit(BG_IMG, (0,0))
    for pipe in pipes:
        pipe.draw(win)
    
    text = SCORE_FONT.render("Score: "+str(score), 1, (255,255,255))
    win.blit(text, (WIN_WIDTH-10-text.get_width(), 10))

    gen = SCORE_FONT.render("Gen: "+str(GEN), 1, (255,255,255))
    win.blit(gen, (10, 10))

    base.draw(win)
    for bird in birds:
        bird.draw(win)
    pygame.display.update()


def eval_genomes(genomes, config):
    global GEN
    GEN += 1
    nets = []
    ge = []
    birds = []

    for _,g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)

        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)
 
    base = Base(730)
    pipes = [Pipe(600)]
    clock = pygame.time.Clock()
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    
    score = 0
    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 0 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else:
            run = False
            break
        
        for i,bird in enumerate(birds):
            bird.move()
            ge[i].fitness += 0.1

            output = nets[i].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5:
                bird.jump()
        
        add_pipe = False
        rem = []
        for pipe in pipes:
            for i,bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[i].fitness -= 1
                    birds.pop(i)
                    nets.pop(i)
                    ge.pop(i)
                
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True
            
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                    rem.append(pipe)
            pipe.move()

            if add_pipe:
                score += 1
                for g in ge:
                    g.fitness += 5
                pipes.append(Pipe(700))
                add_pipe = False
            
            for r in rem:
                pipes.remove(r)

            for i,bird in enumerate(birds):
                if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                    ge[i].fitness -= 1
                    birds.pop(i)
                    nets.pop(i)
                    ge.pop(i)
        
        if score > 50:
            break

        base.move()

        draw_window(win, birds, pipes, base, score)




def run(config_file):

    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes, 50)

    print('\nBest genome:\n{!s}'.format(winner))




if __name__ == "__main__":

    local_dir = os.path.dirname(__file__)
    config_file = os.path.join(local_dir, "config.txt")
    run(config_file)