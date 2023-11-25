def generate_requirements() -> str:
    """
    This function generates the requirements.txt file.
    :return: The requirements.txt file.
    """
    return """boto3==1.28.79
pydantic~=2.5.1
    """