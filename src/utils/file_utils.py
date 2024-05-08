import yaml


def load_yaml(file_path: str) -> dict:
    """Load YAML file and return the data as a dictionary."""
    print(f"Loading config from {file_path}")
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)
    return data
