"""
Utils for reading SSPE files and data handling.
"""
# Imports
from typing import Any, Dict, Generator, List

# Functions
def sspe_reader(path: str) -> Generator[list[Any], None, None]:
    """
    Read a file in the Semicolon Separated Python 
    Expression (SSPE) format.

    Args:
        path (str): The path to the file.

    Yields:
        list: A list of values from
              the file.
    """
    # Make dictionaries for the _global and _local
    # namespaces to be used for the eval and exec
    # functions.
    _globals = {}
    _locals = {}
    # Open the file.
    with open(path) as file:
        for line in file:
            # If the line starts with a "!" character,
            # execute the line as a Python command in
            # the _globals and _locals namespaces.
            if line[0] == "!":
                exec(line[1:], _globals, _locals)
            else:
                # Otherwise, yield the  in the line
                yield [eval(value, _globals, _locals) 
                       for value in line.split(";")]
        
def make_dict_from_sspe(path: str) -> Dict[str, Dict[str, Any] | Any]:
    """
    Make a nested dictionary from a SSPE file. The first 
    line of the file should be the key paths for The
    nested dictionary. The rest of the lines should be
    the values for the keys.

    Args:
        path (str): The path to the file.
    
    Returns:
        dict: The dictionary 
    """
    # Get the key paths from the header
    reader = sspe_reader(path)
    key_paths = [path.split('/') 
                 for path in next(reader)]
    # Initialize the dictionary
    dictionary = {}
    # Iterate over the key paths and values
    for values in reader:
        for key_path, value in zip(key_paths, values):
            current = dictionary
            for key in key_path[:-1]:
                current = current.setdefault(key, {})
            if key_path[-1] in current:
                current[key_path[-1]].append(value)
            else:
                current[key_path[-1]] = [value]
    return dictionary

# Classes
class NestedDict:
    """
    A class for nested dictionaries with handy access
    through path strings.
    """
    def __init__(self, dictionary: Dict):
        self.dictionary = dictionary

    def __getitem__(self, key: str) -> Any:
        current = self.dictionary
        for key in key.split('/'):
            if key not in current:
                raise KeyError(f"Key '{key}' not found.")
            current = current[key]
        if isinstance(current, dict):
            return NestedDict(current)
        return current

    def subkeys(self, key: str) -> List[str]:
        return list(self[key].dictionary.keys())
