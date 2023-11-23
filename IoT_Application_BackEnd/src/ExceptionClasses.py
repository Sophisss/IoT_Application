class IdAlreadyExistsError(Exception):
    def __init__(self, name):
        self.message = f'{name} with the same id already exists'
        self.type = "IdAlreadyExistsError"
        super().__init__(self.message)
    

class ItemNotPresentError(Exception):
    def __init__(self, name_entity):
        self.message = f'{name_entity} with the id is not in the database'
        self.type = 'ItemNotPresentError'
        super().__init__(self.message)
    

class EntitiesNotPresentError(Exception):
    def __init__(self, name_entity):
        self.message = f' No entities with name {name_entity} '
        self.type = 'ItemNotPresentError'
        super().__init__(self.message)
    
