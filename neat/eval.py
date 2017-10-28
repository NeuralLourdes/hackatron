"""
2-input XOR example -- this is most likely the simplest possible example.
"""

from __future__ import print_function
import os
import neat
#import visualize
import random
import tron
import numpy as np

gameSize = [20,20]

# extract map close to head of snake/tron
def transform_map(gameMap, heads, rotation):
    visual_range = 5
    visual_map = np.empty([visual_range, visual_range])
    
    x_head = heads[0][0]
    y_head = heads[0][1]
    for x_offset in range(visual_range):
        for y_offset in range(visual_range):
            x_pos = x_head - 2 + x_offset
            y_pos = y_head - 2 + y_offset
            if x_pos >= 0 and x_pos < gameSize[0] and y_pos >= 0 and y_pos < gameSize[1]:
                visual_map[x_offset, y_offset] = gameMap[x_pos, y_pos]
            else:
                visual_map[x_offset, y_offset] = -1

    print(gameMap)
    print(visual_map)
    


def evolve(game, net1, net2):
    gameState = game.get_game_state()
    gameMap = np.array(gameState[1])

    #print(gameState)
    transform_map(gameMap, gameState[2], gameState[3])

    # get decisions
    gameMap = gameMap.flatten()
    output1 = net1.activate(gameMap)
    output2 = net2.activate(gameMap)

    def pick(x):
        return {
            0: tron.ACTION_STRAIGHT,
            1: tron.ACTION_TURN_RIGHT,
            2: tron.ACTION_TURN_LEFT,
        }[x]

    # set decisions
    game.set_action(0, pick(np.argmax(output1)))
    game.set_action(1, pick(np.argmax(output2)))

    return game


def game_outcome(net1, net2):
    game = tron.TronGame(width = gameSize[0], height = gameSize[1])

    finished = False
    while not finished:
        evolve(game, net1, net2)

        gameState = game.get_game_state()
        finished = gameState[0]
            
    winners = gameState[4]

    if(winners[0] and not winners[1]):
        #print("PLAYER 2 has WON")
        return 2
    if(not winners[0] and winners[1]):
        #print("PLAYER 1 has WON")
        return 1
    else:
        return 0

def demo_game(net1, net2):
    print("PLAYING DEMO GAME!")

    game = tron.TronGame(width = 20, height = 20)

    finished = False
    while not finished:
        evolve(game, net1, net2)

        gameState = game.get_game_state()
        finished = gameState[0]

    gameState = game.get_game_state()
    print(gameState)


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = 0.0

    for genome_id1, genome1 in genomes:
        for genome_id2, genome2 in genomes:
            if genome_id1 > genome_id2:

                net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
                net2 = neat.nn.FeedForwardNetwork.create(genome2, config)
                
                fight = game_outcome(net1, net2)

                if fight == 1:
                    genome1.fitness += 1
                    genome2.fitness -= 1
                elif fight == 2:
                    genome1.fitness -= 1
                    genome2.fitness += 1

def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 300 generations.
    generations = 20
    winner = p.run(eval_genomes, generations)

    # Display the winning genome.
    #print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    print('\nOutput:')
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    
    demo_game(winner_net, winner_net)    
    

    '''
    node_names = {-1:'A', -2: 'B', 0:'A XOR B'}
    visualize.draw_net(config, winner, True, node_names=node_names)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)
    '''
    #p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    #p.run(eval_genomes, 10)


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward')
    run(config_path)