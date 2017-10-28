import gzip

try:
    import cPickle as pickle # pylint: disable=import-error
except ImportError:
    import pickle # pylint: disable=import-error


def save(NN, name):
    """ Save the current simulation state. """
    #filename = '{0}{1}'.format(name,1)
    filename = name
    print("Saving checkpoint to {0}".format(filename))

    with gzip.open(filename, 'w', compresslevel=5) as f:
        data = (NN)
        pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)

def restore(filename):
    """Resumes the simulation from a previous saved point."""
    with gzip.open(filename) as f:
        NN = pickle.load(f)
        
        return NN

def dump_NN_from_checkpoint(filename, savename):
    p = neat.Checkpointer.restore_checkpoint(filename)
    best_boi = p.run(play_tron.eval_genomes, 1)
    save(best_boi, savename)
