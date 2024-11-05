import os


def get_path_from_context(file_name: str = "") -> str:
    """Returns the path to the blacklist file, going up one directory level."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    grandparent_dir = os.path.dirname(os.path.dirname(current_dir))
    file_path = os.path.join(grandparent_dir, file_name)
    return file_path


print(get_path_from_context())
