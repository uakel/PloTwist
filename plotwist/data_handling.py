"""
A submodule with lots of helper functions for handling data
"""
# Imports
from typing import Any, Dict, Generator, List
import numpy as np

# Classes
class NestedDict:
    """
    A class that provides quallity of life improvements
    for working with nested dictionaries.
    """
    def __init__(self, dictionary: Dict):
        self.dictionary = dictionary

    def __getitem__(self, key: str) -> Any:
        """
        Returns for a '/' separated key like 'a/b/c'
        the value in the nested dictionary at 
        dictionary['a']['b']['c'].

        'a/b/c' is called a key path.
        """
        if type(key) != str:
            raise TypeError(f"Key must be a string but "
                            f"is {type(key)}")
        visited = []
        current = self.dictionary
        for key in key.split('/'):
            if key not in current:
                raise KeyError(f"Key '{key}' not present "
                               f"in {'/'.join(visited)}")
            visited.append(key)
            current = current[key]
        if isinstance(current, dict):
            return NestedDict(current)
        try:
            return np.array(current)
        except:
            return current

    def subkeys(self, key: str) -> List[str]:
        """
        Returns the keys of the dictionary 
        located at the key path.
        """
        return list(self[key].dictionary.keys())

# Functions
def sspe_reader(
        path: str, 
        skip_cols: List[int] = []
    ) -> Generator[list[Any], None, None]:
    """
    Read a file in the Semicolon Separated Python 
    Expression (SSPE) format.

    Args:
        path (str): The path to the file.

    Yields:
        list: A list of values from
              the file contained in
              the current line.
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
                return_value = []
                # Otherwise, yield the  in the line
                for idx, value in enumerate(line.split(";")):
                    if idx in skip_cols:
                        continue
                    try:
                        return_value.append(eval(value, _globals, _locals))
                    except:
                        return_value.append(value)
                yield return_value
        

def make_dict_from_sspe(path: str, skip_if_contains: str | None = None) -> Dict[str, Dict[str, Any] | Any]:
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

    # Remove key paths that contain the skip_if_contains
    if skip_if_contains:
        cols_to_skip = [i for i, key_path in enumerate(key_paths) 
                        if skip_if_contains in key_path]
        reader = sspe_reader(path, cols_to_skip)
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

def make_nested_dict_from_sspe(
        path: str,
        skip_if_contains: str | None = None
    ) -> NestedDict:
    """
    Make a NestedDict class from a SSPE file. The first 
    line of the file should be the key paths for The
    nested dictionary. The rest of the lines should be
    the values for the keys.

    Args:
        path (str): The path to the file.
    
    Returns:
        NestedDict: The dictionary 
    """
    return NestedDict(make_dict_from_sspe(path, skip_if_contains))
