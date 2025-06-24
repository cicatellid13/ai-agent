import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))

    if not target_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_file_path):
        return f'Error: File "{file_path}" not found.'
    
    if not target_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try: 
        execution = subprocess.run(["python3", target_file_path], 
                                   timeout=30, 
                                   capture_output=True, 
                                   text=True,
                                   cwd=abs_working_dir)

        if execution.returncode != 0:
            return (
                f'STDOUT: {execution.stdout} \n STDERR: {execution.stderr}\n'
                f'Process exited with code {execution.returncode}'
            )
        if len(execution.stdout.strip()) == 0:
            return (
                f'STDOUT: {execution.stdout} \n STDERR: {execution.stderr}\n'
                f'No output produced.'
            )
        
        return (
                f'STDOUT: {execution.stdout} \n STDERR: {execution.stderr}'
            )

    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_get_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes python file in specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The python file to be executed, relative to the working directory.",
            ),
        },
    ),
)

