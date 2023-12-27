def generate_readme(project_name: str) -> str:
    """
    This method generates the README.md file.
    :param project_name: The name of the project.
    :return: The README.md file.
    """
    return f"""# {project_name.upper()} PROJECT 

## Description

This project contains the generated code for the GraphQL API. GraphQL APIs provide a powerful and flexible interface for interacting with our system's data.

## Project Structure

The project is organized into the following modules:

- `src`: Contains the source code.
  - Inside the src directory, you will find the Lambdas for each entity and relationship.
  - `dal`: Contains the Data Access Layer (DAL) code, which facilitates interaction with the database.
  - `model`: Contains models for defining data.
  - `graphql`: Contains the resolver and graphql schema.
- `template`: Contains YAML templates for AWS resources.

## Getting Started

For deployment instructions, see the [Deployment Guide](./template/guide/deployment_guide.md).
    """
