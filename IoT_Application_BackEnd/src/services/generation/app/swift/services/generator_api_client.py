from services.generation.attribute_type import AttributeType
from services.generation.utility_methods import get_links_associated
from services.generation.configuration_application.dal_resources.model.generator_model_link import \
    __search_primary_key_field
from services.generation.utility_methods import generate_resource_name


def generate_api_client(json: dict) -> str:
    """
    This method generate the code for the api client.
    :param json: the json with the data.
    :return: the code for the api client.
    """
    return f"""import Foundation
import Amplify

final class ApiClient {{

{__generate_api_client_entity_methods(json)}
{__generate_api_client_link_methods(json)}
}} 
"""


def __generate_api_client_entity_methods(json: dict) -> str:
    """
    This method generate the code for the entity methods.
    :param json: the json with the data.
    :return: the code for the entity methods.
    """
    to_return = ""
    for entity in json['entities']:
        entity_id = entity['primary_key'][0]
        entity_id_type = next(
            (AttributeType[field['type']].value for field in entity['fields'] if field['name'] == entity_id),
            None)
        link_associated_first_entity, link_associated_second_entity = get_links_associated(entity, json['links'])
        entities_associated = __get_entity_associated(json['entities'], link_associated_first_entity,
                                                      link_associated_second_entity)
        for api in entity['API']:
            match api['type']:
                case "DELETE":
                    par = {
                        entity_id: entity_id_type
                    }
                    to_return += __generate_api_client_delete(par, api['name'])
                case "GET_ALL":
                    to_return += __generate_api_client_get_all(api['name'], entity, entities_associated)
                case "GET":
                    par = {
                        entity_id: entity_id_type
                    }
                    to_return += __generate_api_client_get(api['name'], entity, par, entities_associated)
                case "POST":
                    parameters = {
                        entity_id: entity_id_type
                    }
                    for par in api['parameters']:
                        parameters[par] = next(
                            (AttributeType[field['type']].value for field in entity['fields'] if field['name'] == par),
                            None)
                    to_return += __generate_api_client_post(api['name'], parameters)
                case "PUT":
                    to_return += __generate_api_client_put(api['name'], entity, link_associated_first_entity,
                                                           link_associated_second_entity)

    return to_return


def __generate_api_client_link_methods(json: dict) -> str:
    """
    This method generate the code for the link methods.
    :param json: the json with the data.
    :return: the code for the link methods.
    """
    to_return = ""
    for link in json['links']:
        link_fields = [*__search_primary_key_field(json['entities'], link)]
        par = {
            link_fields[0]['name']: AttributeType[link_fields[0]['type']].value,
            link_fields[1]['name']: AttributeType[link_fields[1]['type']].value
        }
        for api in link['API']:
            match api['type']:
                case "DELETE":
                    to_return += __generate_api_client_delete(par, api['name'])
                case "GET":
                    to_return += __generate_api_client_get(api['name'], link, par)
                case "POST":
                    for par_ in api['parameters']:
                        par[par_] = next(
                            (AttributeType[field['type']].value for field in link['fields'] if field['name'] == par_),
                            None)
                    to_return += __generate_api_client_post(api['name'], par)
                case "PUT":
                    for par_ in link['fields']:
                        par[par_['name']] = par_['type']
                    to_return += __generate_api_client_put_link(generate_resource_name(link), api['name'], par)
    return to_return


def __generate_api_client_put(api_name: str, entity: dict, link_associated_first_entity, link_associated_second_entity) -> str:
    parameters = __generate_parameters_links(link_associated_first_entity, link_associated_second_entity)
    return f'''
    func {api_name}({entity['name'].lower()}:{entity['name']}{"," if parameters else ""} {', '.join(f"{key}: {value}" for key, value in parameters.items())}) async -> Result<String, Error> {{

        {__generate_conditions(link_associated_first_entity, link_associated_second_entity)}
        {__generate_mutation_create(api_name, entity, link_associated_first_entity + link_associated_second_entity)}
        {__generate_request(api_name, 'String', True)}
  }}
    '''


def __generate_api_client_put_link(name: str, api_name: str, par: dict) -> str:
    return f'''
    func {api_name}({", ".join(f"{key}: {value}" for key, value in par.items())}) async -> Result<String, Error> {{

        let mutation = """\n         mutation {api_name}(
                  {name}:{{
                  {__generate_parameter_create_link(par)}
                  }}
               ) 
          }}
         """

    {__generate_variables(*par.keys())}
    {__generate_request(api_name, 'String', True)}
    }} 

'''


def __generate_api_client_delete(parameters: dict, api_name: str) -> str:
    par = ", ".join(f"{key}: {value}!" for key, value in parameters.items())
    par_ = ", ".join(f"${key}: {value}!" for key, value in parameters.items())
    par__ = ", ".join(f"{key}: ${value}" for key, value in parameters.items())
    return f'''   
    func {api_name}({par}) async -> Result<String, Error> {{

        let mutation = """\n         mutation {api_name}({par_}) {{
               {api_name}({par__})
         }}
         """

    {__generate_variables(*parameters.keys())}
    {__generate_request(api_name, 'String', True)}
    }} 

'''


def __generate_api_client_post(api_name: str, parameters: dict) -> str:
    return f'''
    func {api_name}({", ".join(f"{key}: {value}" for key, value in parameters.items())}) async -> Result<String, Error> {{

        let mutation = """
        mutation {api_name}({",  ".join(f"${key}: {value}" for key, value in parameters.items())}) {{
            {api_name}({",  ".join(f"{key}: ${value}" for key, value in parameters.items())})
        }}
    """

    {__generate_variables(*parameters.keys())}
    {__generate_request(api_name, 'String', True)}
    }} 

'''


def __generate_api_client_get(api_name: str, item: dict, parameters: dict, entity_associated=None) -> str:
    name = generate_resource_name(item)
    par = ", ".join(f"{key}: {value}!" for key, value in parameters.items())
    to_return = ""
    to_return += "\n            ".join(field["name"] for field in item["fields"])
    return f'''    
    func {api_name}({par}) async -> Result<{name}, Error> {{

    let query = """\n        query {api_name}{{
            {api_name}{{({par})
            {__generate_fields_query(item['fields'], entity_associated) if entity_associated else to_return}
         }}
      }}
      """

    {__generate_variables(*parameters.keys())}
    {__generate_request(api_name, f"{name}", False)}
    }} 

    '''


def __generate_api_client_get_all(api_name: str, entity: dict, entities_associated: list) -> str:
    return f'''    
    func {api_name}() async -> Result<[{entity['name']}], Error> {{

    let query = """\n        query {api_name}{{
            {api_name}{{
            {__generate_fields_query(entity['fields'], entities_associated)}
         }}
      }}
      """

    {__generate_request(api_name, f"[{entity['name']}]", False)}
    }} 

    '''


def __generate_fields_query(fields_entity: list, entities: list) -> str:
    to_return = "\n            ".join(field['name'] for field in fields_entity)
    for entity in entities:
        fields_entity_associated = "\n              ".join(field['name'] for field in entity['fields'])
        to_return += f"""\n            {entity['name']}{{
              {fields_entity_associated}
            }}"""
    return to_return


def __generate_variables(*variables) -> str:
    var = ",  ".join(f'"{variable}": {variable}' for variable in variables)
    return f"""    let variables: [String:Any] = [{var}]"""


def __generate_request(api_name: str, response_type, is_mutation) -> str:
    return f"""    do {{
            let request = GraphQLRequest<{response_type}> (
                document: {'mutation' if is_mutation else 'query'},
                responseType: {response_type}.self,
                decodePath: "{api_name}")
            let response = try await Amplify.API.{'mutate' if is_mutation else 'query'}(request: request)
{__generate_response_error()} """


def __generate_response_error() -> str:
    """
    This method generate the code for the response error.
    :return: the code for the response error.
    """
    return f"""            
            switch response {{
            case .success(let data):
                return .success(data)
            case .failure(let error):
                return .failure(error)
            }}
        }}
        catch let error as APIError{{
            return ErrorsService.buildAPIErrorResult(error: error)
        }}
        catch {{
            return .failure(GenericCommError.decodeEncode)
        }}"""


def __generate_mutation_create(api_name: str, item: dict, links: list) -> str:
    name = generate_resource_name(item)
    name_links = ""
    for link in links:
        name_links += f"""\\({link['first_entity'].lower()}_{link['second_entity'].lower()}_link)
        """
    return f'''
        let mutation = """
               mutation {api_name}{{
               {api_name}(
               {name}:{{
                {__gen_p(item['fields'], name.lower())}}}
                {name_links}
               )
        }}    
        """
            '''


def __generate_parameter_create_link(par) -> str:
    return "\n                  ".join(
        f"{key}: \\({key})" if value in ['integer', 'float'] else f'{key}: "\\({value})"' for key, value in par.items())


def __generate_conditions(link_associated_first_entity, link_associated_second_entity) -> str:
    to_return = ""
    for link in link_associated_first_entity:
        if link['numerosity'] in ['one-to-many', 'many-to-many']:
            to_return += __gen_condition_many(link, link['second_entity'], link['primary_key'][1])
        else:
            to_return += __gen_condition_one(link, link['primary_key'][1])
    for link in link_associated_second_entity:
        if link['numerosity'] in ['one-to-many', 'many-to-many']:
            to_return += __gen_condition_one(link, link['primary_key'][0])
        else:
            to_return += __gen_condition_many(link, link['first_entity'], link['primary_key'][0])
    return to_return


def __gen_condition_many(link: dict, name: str, primary_key) -> str:
    first_entity, second_entity = link['first_entity'], link['second_entity']
    return f'''
        var {first_entity.lower()}_{second_entity.lower()}_link = ""
        if !{first_entity.lower()}{second_entity.lower()}.isEmpty {{
             {first_entity.lower()}{second_entity.lower()}_link.append("""
             {first_entity}{second_entity}: [
                     \\({first_entity.lower()}{second_entity}.map {{ {name.lower()} in
                     """
                     {{
                        {primary_key}: \\({name.lower()}.{primary_key})
                        {__gen_p(link['fields'], first_entity.lower() + second_entity)}     }}
                     """
                 }}.joined(separator: ",\\n")
        )
             ]
        """
            )
        }}    
            '''


def __gen_condition_one(link: dict, primary_key) -> str:
    first_entity, second_entity = link['first_entity'], link['second_entity']
    return f'''
        let {first_entity.lower()}_{second_entity.lower()}_link = {first_entity.lower()}_{second_entity.lower()}.map {{  {first_entity.lower()}{second_entity} in
            """
            {first_entity}{second_entity}: {{
                {primary_key}: \\({first_entity.lower()}{second_entity}.{primary_key})
                {__gen_p(link['fields'], f"{first_entity.lower()}{second_entity}")}}}
            """
        }} ?? ""
        '''


def __gen_p(fields: list, name: str) -> str:
    backslash = '\\'
    to_return = ""
    for field in fields:
        type_f = True if field['type'] in ['integer', 'float'] else False
        if field['required']:
            to_return += f"""{field["name"]}:{backslash if type_f else f'"{backslash}'}({name}.{field["name"]}){f'' if type_f else '"'}
                """
        else:
            to_return += f"""{field["name"]}:{backslash if type_f else f'{backslash}'}({name}.{field["name"]} != "" ? "{backslash}"{backslash}({name}.{field["name"]}!){backslash}"" : "null")
                """
    return to_return


def __generate_parameters_links(link_associated_first_entity, link_associated_second_entity) -> dict:
    parameters = dict()
    for link in link_associated_first_entity:
        name = f"{link['first_entity'].lower()}_{link['second_entity'].lower()}"
        name_l = f"{link['first_entity']}{link['second_entity']}"
        parameters[name] = f'[{name_l}]' if link['numerosity'] in ['one-to-many', 'many-to-many'] else f'{name_l}?'
    for link in link_associated_second_entity:
        name = f"{link['first_entity'].lower()}_{link['second_entity'].lower()}"
        name_l = f"{link['first_entity']}{link['second_entity']}"
        parameters[name] = f'[{name_l}]' if link['numerosity'] in ['many-to-one', 'many-to-many'] else f'{name_l}?'
    return parameters


def __get_entity_associated(entities: list, link_associated_first_entity, link_associated_second_entity) -> list:
    entities_associated = list()
    for link in link_associated_first_entity:
        entities_associated.append(
            next((entity for entity in entities if entity['name'] == link['second_entity']), None))
    for link in link_associated_second_entity:
        entities_associated.append(
            next((entity for entity in entities if entity['name'] == link['first_entity']), None))
    return entities_associated
