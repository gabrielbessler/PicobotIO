class Item():
    def __init__(self, itemId):
        '''
        Creates a new item (single-time consumable)
        '''
        self.type = itemId

    def __repr__(self):
        '''
        Return a string representation of the item object,
        which is used to send the map to the user
        '''
        return "Item(" + str(self.type) + ")"
