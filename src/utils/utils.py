

def json2dict(path: str) -> dict:
    """
    Converts a JSON file to a dictionary.
    :param path: Path to the JSON file.
    :return: Dictionary representation of the JSON file.
    """
    import json
    with open(path, 'r') as file:
        return json.load(file)
    
def dict2json(data: dict, path: str):
    """
    Converts a dictionary to a JSON file.
    :param data: Dictionary to convert.
    :param path: Path where the JSON file will be saved.
    """
    import json
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)

def save_pkl_file(path: str, data):
    """
    Saves data to a pickle file.
    :param path: Path where the pickle file will be saved.
    :param data: Data to save.
    """
    import pickle
    with open(path, 'wb') as file:
        pickle.dump(data, file)

def load_pkl_file(path: str):
    """
    Loads data from a pickle file.
    :param path: Path to the pickle file.
    :return: Loaded data.
    """
    import pickle
    with open(path, 'rb') as file:
        return pickle.load(file)