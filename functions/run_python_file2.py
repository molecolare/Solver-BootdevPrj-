import os
import subprocess
import json

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:

    try:
        abs_working_directory = os.path.abspath(working_directory)
        percorso = os.path.join(working_directory, file_path)
        abs_file_path = os.path.abspath(percorso)
        if not os.path.isdir(abs_working_directory):
                    return f'Error: "{working_directory}" is not a valid directory.'
        if not abs_file_path.startswith(abs_working_directory):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file.'

        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'

        # Costruisce il comando per eseguire il file
        command = ["python", abs_file_path]

        result = subprocess.run(
            command,
            cwd=abs_working_directory,
            timeout=30,
            capture_output=True,
            text=True
        )
        output = {}
        if result.returncode != 0:
                    output["error"] = f"Process exited with code {result.returncode}."
        if result.stdout:
                    output["stdout"] = result.stdout
        if result.stderr:
                    output["stderr"] = result.stderr

        return output if output else {"message": "No output produced."}
    except subprocess.TimeoutExpired:
            return {"error": "Execution timed out after 30 seconds."}
    except Exception as e:
                return {"error": str(e)}

    except subprocess.CalledProcessError as e:
        return f"Error: The command failed with return code {e.returncode}.\n{e.stderr}"
    except PermissionError:
            return f"Error: Permission denied for directory or file: {abs_working_directory}"
