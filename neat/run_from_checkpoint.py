import neat
import play_tron

p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')

best_bois = p.run(play_tron.eval_genomes, 1)