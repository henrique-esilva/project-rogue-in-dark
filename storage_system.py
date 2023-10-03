
class StorageSystem:
    # a simple to use and complete class for storage items
    # this class wasn't made for direct management of behaviors
    maximum_length = int(-1)
    holding = []

    def configure_length(self, length: int):
        self.maximum_length = length

    def already_contains( self, item ):
        if item in self.holding:
            return item
        else:
            return False

    def add_item( self, item ):
        self.holding.append( item )

    def remove_item( self, item ):
        if item in self.holding:
            return self.holding.remove(item)
        else:
            return False

    def remove_item_by_pos( self, index ):
        return self.holding.pop( index )

    def is_full( self ):
        if self.maximum_length == -1 or len(self.holding) < self.maximum_length:
            return False
        elif len(self.holding) >= self.maximum_length:
            return True
    
    def is_empty( self ):
        if len(self.holding)==0:
            return True
        return False

    def get_free_slots( self ):
        if self.maximum_length == -1:
            return 10000
        else:
            return self.maximum_length - len(self.holding)