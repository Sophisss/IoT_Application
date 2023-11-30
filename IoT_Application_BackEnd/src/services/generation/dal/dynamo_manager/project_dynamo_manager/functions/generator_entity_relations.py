def generate_entity_relations(entity: dict, link: dict) -> str:
    dispatch_table = {
        ('second_entity', 'one-to-many'): self.link_second_entity_one_to_many,
        ('first_entity', 'one-to-many'): self.link_first_entity_one_to_many,
        ('second_entity', 'many-to-one'): self.link_second_entity_many_to_one,
        ('first_entity', 'many-to-one'): self.link_first_entity_many_to_one,
        ('first_entity', 'many-to-many'): self.link_first_entity_many_to_many,
        ('second_entity', 'many-to-many'): self.link_second_entity_many_to_many,
        ('first_entity', 'one-to-one'): self.link_first_entity_one_to_one,
        ('second_entity', 'one-to-one'): self.link_second_entity_one_to_one
    }

    condition_key = (link['first_entity'], link['numerosity']) if link['first_entity'] == entity['name'] else (link['second_entity'], link['numerosity'])
    return dispatch_table[condition_key]()
