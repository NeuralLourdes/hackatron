
class tree_node:

    def __init__(self,field,score,p_orientation,p_position,n_orientation,n_position):
        self.subnodes=[]
        self.score=score
        self.field=field
        self.p_orientation=p_orientation
        self.p_position=p_position
        self.n_orientation=n_orientation
        self.n_position=n_position

    def add_node(self,node):
        self.subnodes.append(node)