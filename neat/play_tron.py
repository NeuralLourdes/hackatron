import numpy as np
import neat
import random

import tron

gameSize = [20,20]


# extract map close to head of snake/tron
def transform_map(gameMapRaw, heads, rotation):
    head1 = np.array(heads[0]).T
    head2 = np.array(heads[1]).T

    heads = [head1, head2]

    gameMapRaw[heads[0][1], heads[0][0]] = 3
    gameMapRaw[heads[1][1], heads[1][0]] = 3

    visual_range = 7

    def extract(gameMap, pick, head, rotation):
        visual_map = np.empty([visual_range, visual_range], dtype=int)

        x_head = head[0]
        y_head = head[1]

        for y_offset in range(visual_range):
            for x_offset in range(visual_range):
                x_pos = x_head - int(visual_range)/2 + x_offset
                x_pos = int(x_pos + 1)
                y_pos = y_head - int(visual_range)/2 + y_offset
                y_pos = int(y_pos + 1)
                if x_pos >= 0 and x_pos < gameSize[0] and y_pos >= 0 and y_pos < gameSize[1]:
                    val = gameMap[y_pos, x_pos]      

                    def pick(x):
                        return {
                            0: 0,
                            1: 1,
                            2: 1,
                            3: 3,
                        }[x]

                    visual_map[y_offset, x_offset] = pick(val)
                else:
                    visual_map[y_offset, x_offset] = 1

        visual_map = np.rot90(visual_map, k = int(rotation/90))
        return visual_map
    
    visual_map1 = extract(gameMapRaw, 1, head1, rotation[0])
    visual_map2 = extract(gameMapRaw, 2, head2, rotation[1])

    return [visual_map1, visual_map2]

def calc_next_action(game, player, net):
    gameState = game.get_game_state()
    gameMap = np.array(gameState[1])

    visualMap = transform_map(gameMap, gameState[2], gameState[3])

    # get decisions
    output = net.activate(visualMap[player].flatten())

    def pick(x):
        return {
            0: tron.ACTION_STRAIGHT,
            1: tron.ACTION_TURN_RIGHT,
            2: tron.ACTION_TURN_LEFT,
        }[x]

    return pick(np.argmax(output))
    

def evolve(game, net1, net2):
    gameState = game.get_game_state()
    gameMap = np.array(gameState[1])

    visualMap = transform_map(gameMap, gameState[2], gameState[3])

    # get decisions
    output1 = net1.activate(visualMap[0].flatten())
    output2 = net2.activate(visualMap[1].flatten())

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


class genome_parallel:
    def __init__(self, best_net, ref_net1, ref_net2):
        self.best_net = best_net
        self.ref_net1 = ref_net1
        self.ref_net2 = ref_net2

    def eval_fn(self, genome, config):
        fitness = 0

        testnet = neat.nn.FeedForwardNetwork.create(genome, config)
        bestnet = neat.nn.FeedForwardNetwork.create(self.best_net, config)
        
        def fight(opponet, fitness):
            fight = game_outcome(testnet, opponet)

            if fight == 1:
                fitness += 1
            elif fight == 2:
                fitness -= 1

            return fitness

        fitness = fight(bestnet, fitness)
        fitness = fight(self.ref_net1, fitness)
        fitness = fight(self.ref_net2, fitness)

        return fitness


