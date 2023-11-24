from Services.Generation.DAL.Model.generator_model import generate_header_model, generate_model_fields


def generate_model_entity(model_name, fields):
    return f"""{generate_header_model()}

class {model_name}(BaseModel):
    {generate_model_fields(fields)}
"""
