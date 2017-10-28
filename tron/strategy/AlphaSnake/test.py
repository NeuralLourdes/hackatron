from strategy.AlphaSnake.alphaSnakeStrategy import alphaSnakeStrategy
import numpy as np

ass = alphaSnakeStrategy(0,30,30)

m1 = np.matrix([[1,1,1,0], [0,0,1,0], [0,2,0,0], [0,2,2,2]])
p1head = (1,2)
p2head = (2,1)

#print(np.shape(ass.load_data("1509212508.1820977")))

