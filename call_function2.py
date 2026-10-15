import json
from collections.abc import Callable
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.get_files_info import write_file

available_functions = [
    schema_get_files_info,
    {
        "type": "function",
        "function": {
            "name": "get_file_content",
            "description": "Legge il contenuto di un file specificato.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Il percorso del file da leggere.",
                    },
                },
                "required": ["file_path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_python_file",
            "description": "Esegue un file Python con argomenti opzionali.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Il percorso del file Python da eseguire.",
                    },
                    "args": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Argomenti opzionali da passare al file Python.",
                    },
                },
                "required": ["file_path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Scrive o sovrascrive il contenuto di un file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Il percorso del file da scrivere.",
                    },
                    "content": {
                        "type": "string",
                        "description": "Il contenuto da scrivere nel file.",
                    },
                },
                "required": ["file_path", "content"],
            },
        },
    },
]

function_map: dict[str, Callable[..., dict]] = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}

def call_function(tool_call, verbose: bool = False) -> dict:
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments or "{}")

    if verbose:
        print(f" - Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    # Aggiungi working_directory agli argomenti
    function_args["working_directory"] = "./calculator"

    # Verifica se la funzione esiste nella mappatura
    if function_name not in function_map:
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": f"Error: Unknown function: {function_name}",
        }

    # Esegui la funzione
    try:
        result = function_map[function_name](**function_args)
        result_message = {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result),  # Converti il risultato in stringa JSON
            }

            # Verifica che il contenuto non sia vuoto
        if not result_message["content"]:
                raise ValueError("Il risultato della funzione è vuoto.")

        if verbose:
                print(f"-> {result_message['content']}")

        return result_message
    except Exception as e:
            return {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": f"Error: {str(e)}",
            }
