import os
def read_file(filepath: str) -> dict:
    try:
        with open(filepath, 'r') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")
    except Exception as e:
        raise Exception(f"Error reading file: {e}")

def list_files(directory: str) -> dict:
    try:
        return os.listdir(directory)
    except Exception as e:
        raise Exception(f"Error listing files: {e}")
        
def write_file(filepath: str, content: str) -> dict:
    try:
        with open(filepath, 'w') as file:
            file.write(content)
        return {"status": "success", "message": "File written successfully"}
    except Exception as e:
        raise Exception(f"Error writing file: {e}")
    
def search_file(directory: str, query: str) -> dict:
    try:
        return [file for file in os.listdir(directory) if query in file]
    except Exception as e:
        raise Exception(f"Error searching file: {e}")
    