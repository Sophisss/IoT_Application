def generate_exception_lambda() -> str:
    """
    This function generates the exception lambda.
    :return: the exception lambda.
    """
    return """
    except (InvalidApiError, IdAlreadyExistsError, ItemNotPresentError,
            InternalServerError) as e:
        return {'errors': {'message': str(e.message),
                'type': str(e.__class__.__name__)}}

    except Exception as e:
        return {'errors': {'message': str(e),
                'type': str(e.__class__.__name__)}}"""
