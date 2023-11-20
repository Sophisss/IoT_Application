def generator_exception():
    return f"""
class IdAlreadyExistsError(Exception):
    def __init__(self, name_entity, id_value):
        self.message = f'{{name_entity}} with the same ID {{id_value}} already exists'
        self.type = "IdAlreadyExistsError"
        super().__init__(self.message)


class ItemNotPresentError(Exception):
    def __init__(self, name_entity, id_value):
        self.message = f'{{name_entity}} with the ID {{id_value}} is not in the database'
        self.type = 'ItemNotPresentError'
        super().__init__(self.message)


class EntitiesNotPresentError(Exception):
    def __init__(self, name_entity):
        self.message = f' No entities with name {{name_entity}} '
        self.type = 'ItemNotPresentError'
        super().__init__(self.message)
"""
