class Wall():

    def __init__(self, wall_type=0):
        '''
        Creates the default wall object
        '''
        self.wall_type = wall_type

    def __repr__(self):
        '''
        Return a string representation of the wall object,
        which is used to send the map to the user
        '''
        return "Wall()"
