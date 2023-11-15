from template_lambdas import *
from utility_methods import read_json, put_s3_object
import os


def generation_configuration(data):
    result_configuration = []
    table = data['awsConfig']['dynamo']['tables'][0]
    table_parameters = data['parameters']
    result_configuration.append(template_configuration_dynamo.format(table_name=table['tableName'],
                                                                     separator=table_parameters['id_separator'],
                                                                     single_entity_storage_keyword=table_parameters[
                                                                         'single_entity_storage_keyword'],
                                                                     sort_key=table['sort_key']['name'],
                                                                     partition_key=table['partition_key']['name']
                                                                     ))
    return ''.join(result_configuration)


def generation_lambdas_handler(data):
    stringa = ''.join(
        [template_lambda_handler.format(name_entity=entity['name'], primary_key=entity["primary_key"][0],
                                        match="match event['field']:" if entity["API"] else '',
                                        methods=''.join(generate_all_methods(entity, data)))
         for
         entity in data['entities']])
    return stringa


def generate_all_methods(entity, data):
    methods_code = []
    for api in entity['API']:
        primary_key = entity['primary_key'][0]
        match api['type']:
            case 'GET':
                methods_code.append(generate_method_get(api, primary_key, entity['name'], data))
            case 'DELETE':
                methods_code.append(generate_method_delete(api, primary_key, entity['name']))
            case 'PUT':
                methods_code.append(generate_method_create(api, primary_key, entity['name']))
    return methods_code


def generate_method_get(api, primary_key, name, data):
    option = []
    for link in data['links']:
        if name == link['first_entity']:
            option = option_template_for_link.format(primary_key=primary_key,
                                                     name_entity=name, second_entity=link['second_entity'])
    return template_method_for_get.format(name_method=api["name"], primary_key=primary_key,
                                          name_entity=name, option=option if option else '')


def generate_method_delete(api, primary_key, name):
    return template_method_for_delete.format(name_method=api["name"], primary_key=primary_key, name_entity=name)


def generate_method_create(api, primary_key, name):
    return template_method_for_create.format(name_method=api["name"], primary_key=primary_key, name_entity=name)


def generation_lambdas_handler_link(data):
    stringa = ''.join(
        [template_lambda_handler_link.format(first_entity=link['first_entity'], second_entity=link['second_entity'],
                                             partition_key=link["primary_key"][0],
                                             sort_key=link['primary_key'][1],
                                             match="match event['field']:" if link["API"] else '',
                                             methods=''.join(generate_all_methods_link(link)))
         for
         link in data['links']])
    return stringa


def generate_all_methods_link(link):
    methods_code = []
    for api in link['API']:
        partition_key = link['primary_key'][0]
        sort_key = link['primary_key'][1]
        match api['type']:
            case 'GET':
                methods_code.append(generate_method_get_link(api['name'], partition_key, sort_key))
            case 'DELETE':
                methods_code.append(generate_method_delete_link(api['name'], partition_key, sort_key))
            case 'PUT':
                methods_code.append(generate_method_create_link(api['name'], partition_key, sort_key))
    return methods_code


def generate_method_get_link(api_name, partition_key, sort_key):
    return template_method_for_get_link.format(name_method=api_name, partition_key=partition_key, sort_key=sort_key)


def generate_method_create_link(api_name, partition_key, sort_key):
    return template_method_for_create_link.format(name_method=api_name, partition_key=partition_key, sort_key=sort_key)


def generate_method_delete_link(api_name, partition_key, sort_key):
    return template_method_for_delete_link.format(name_method=api_name, partition_key=partition_key, sort_key=sort_key)


def generate_lambda_code(bucket_name, folder_name):
    data = read_json()
    file_name = 'api.py'
    key = os.path.join(folder_name, file_name)

    put_s3_object(bucket_name, key, file_result_template.format(configuration_dynamo=generation_configuration(data),
                                                                lambdas=generation_lambdas_handler(data),
                                                                lambdas_link=generation_lambdas_handler_link(data)))
