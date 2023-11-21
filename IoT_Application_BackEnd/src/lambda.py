from DynamoClass import DynamoDBManager
from ExceptionClasses import IdAlreadyExistsError, ItemNotPresentError, EntitiesNotPresentError

dynamodb_manager = DynamoDBManager('IoT', ':', 'PK', 'SK',
                                   'registry', 'SK-PK')


def lambda_handler_Device(event, context):
    try:
        match event['field']:

            case 'createDevice':
                response, id_entity = dynamodb_manager.create_device(event['arguments']['Device'])
                if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                    response = f"Device with id {id_entity} created"

            case 'deleteDevice':
                response, device_id = dynamodb_manager.delete_device(event['arguments']['device_id'])
                if not response:
                    raise ItemNotPresentError('Device', device_id)
                response['device_id'] = response.pop(dynamodb_manager.get_partition_key_table())

            case 'getDeviceById':
                device_id = dynamodb_manager.create_id('Device', event['arguments']['device_id'])
                response = dynamodb_manager.get_item(device_id)
                if not response:
                    raise ItemNotPresentError('Device', device_id)
                response['device_id'] = response.pop(dynamodb_manager.get_partition_key_table())

                if 'Building' in event['projection']:
                    res = dynamodb_manager.get_items_with_secondary_index('Building', device_id)
                    res = res[0][dynamodb_manager.get_partition_key_table()]
                    res = dynamodb_manager.get_item(res)
                    res['building_id'] = res.pop(dynamodb_manager.get_partition_key_table())
                    response['Building'] = res

            case 'getDevices':
                response = dynamodb_manager.get_items_with_secondary_index('Device')
                if not response:
                    raise EntitiesNotPresentError('Device')
                for item in response:
                    item['device_id'] = item.pop(dynamodb_manager.get_partition_key_table())

            case _:
                response = 'error'

    except (IdAlreadyExistsError, ItemNotPresentError, EntitiesNotPresentError) as err:
        return {'errors': {'message': err.message,
                           'type': err.type}
                }
    else:
        return response


def lambda_handler_Building(event, context):
    try:
        match event['field']:

            case 'createBuilding':
                response, id_entity = dynamodb_manager.create_building(event['arguments']['Building'])
                if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                    response = f"Building with id {id_entity} created"

            case 'deleteBuilding':
                response, building_id = dynamodb_manager.delete_building(event['arguments']['building_id'])
                if not response:
                    raise ItemNotPresentError('Building', building_id)
                response['building_id'] = response.pop(dynamodb_manager.get_partition_key_table())

            case 'getBuildingById':
                building_id = dynamodb_manager.create_id('Building', event['arguments']['building_id'])
                response = dynamodb_manager.get_item(building_id)
                if not response:
                    raise ItemNotPresentError('Building', building_id)
                response['building_id'] = response.pop(dynamodb_manager.get_partition_key_table())

                if 'Device' in event['projection']:
                    res = dynamodb_manager.get_items(building_id, 'Device')
                    items_result = []
                    for item in res:
                        item = dynamodb_manager.get_item(item[dynamodb_manager.get_sort_key_table()])
                        item['device_id'] = item.pop(dynamodb_manager.get_partition_key_table())
                        items_result.append(item)
                    response['Device'] = items_result

            case 'getBuildings':
                response = dynamodb_manager.get_items_with_secondary_index('Building')
                if not response:
                    raise EntitiesNotPresentError('Building')
                for item in response:
                    item['building_id'] = item.pop(dynamodb_manager.get_partition_key_table())

            case _:
                response = 'error'

    except (IdAlreadyExistsError, ItemNotPresentError, EntitiesNotPresentError) as err:
        return {'errors': {'message': err.message,
                           'type': err.type}
                }
    else:
        return response


def lambda_handler_BuildingDevice(event, context):
    match event['field']:


        case 'createLinkDeviceBuilding':
            response = dynamodb_manager.create_link_building_device(event['arguments'])
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                response = f"Link created"

        case 'deleteLinkDeviceBuilding':
            # response = dynamodb_manager.delete_link_building_device(event['arguments']['building_id'], event['arguments']['device_id'])
            # response['building_id'] = response.pop(dynamodb_manager.get_partition_key_table())
            # response['device_id'] = response.pop(dynamodb_manager.get_sort_key_table())
            # response = list(response.values())

        case 'getLinkBuildingDevice':
            # building_id = dynamodb_manager.create_id_entity('Building', 'building_id', event['arguments'])
            # device_id = dynamodb_manager.create_id_entity('Device', 'device_id', event['arguments'])
            # response = dynamodb_manager.get_item(building_id, device_id)
            # response['building_id'] = response.pop(dynamodb_manager.get_partition_key_table())
            # response['device_id'] = response.pop(dynamodb_manager.get_sort_key_table())
            # response = list(response.values())

        case 'updateLinkBuildingDevice':  # TODO
            response = 'ddd'

        case _:
            response = 'error'
    return response
