class Asset(object):
    """
    Asset class with specified attributes "id" and "price".
    """
    
    def __init__(self, id, price):
        self.id = id
        self.price = price
        
    def print_id(self):
        print("The ID of the asset is: %s" %(self.id))
        
