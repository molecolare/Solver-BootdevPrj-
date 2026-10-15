# functions/get_files_info.py
import os
import json

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    """
    Validates if the target directory is within the working_directory and returns a string
    with the contents of the directory if valid.

    Args:
        working_directory: The absolute or relative path to the working directory.
        directory: The target directory to validate (can be relative to working_directory).

    Returns:
        A string indicating success or failure, with the directory contents if successful.
    """
    try:

        # Ottieni il percorso assoluto della working_directory
        working_dir_abs = os.path.abspath(working_directory)

        # Costruisci il percorso completo al target directory
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        # Verifica se il target_dir è all'interno della working_directory
        if os.path.commonpath([working_dir_abs, target_dir]) != working_dir_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Verifica se il target_dir è effettivamente una directory
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        # Leggi i file nella directory
        items = []
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)
            is_dir = os.path.isdir(item_path)
            file_size = os.path.getsize(item_path) if not is_dir else 0
            items.append((item, file_size, is_dir))

        # Costruisci l'output formattato
        output_lines = [f"Result for '{directory}' directory:"]
        for name, size, is_dir in items:
            output_lines.append(f"  - {name}: file_size={size} bytes, is_dir={is_dir}")

        return "\n".join(output_lines)

    except Exception as e:
        return f'Error: {str(e)}'
def write_file(working_directory: str, file_path: str, content: str) -> str:
    """
    Writes content to a file within the working_directory.

    Args:
        working_directory: The absolute or relative path to the working directory.
        file_path: The path to the file to write (can be relative to working_directory).
        content: The content to write to the file.

    Returns:
        A string indicating success or failure.
    """
    try:
        # Ottieni il percorso assoluto della working_directory
        working_dir_abs = os.path.abspath(working_directory)

        # Costruisci il percorso completo al file
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Verifica se il file è all'interno della working_directory
        if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
            # Verifica se il percorso punta a una directory esistente
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # Crea le directory necessarie se non esistono
        os.makedirs(os.path.dirname(target_file), exist_ok=True)

        # Scrivi il contenuto nel file
        with open(target_file, "w") as f:
            f.write(content)

        # Restituisci un messaggio di successo
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: {str(e)}'
