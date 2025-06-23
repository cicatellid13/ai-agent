import os
from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))

    if not target_file_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(target_file_path, "r") as f:
            file_content_string = f.read()
            if len(file_content_string) > MAX_CHARS:
                return f'{file_content_string[:MAX_CHARS]} [...File "{file_path}" truncated at 10000 characters]'
            return file_content_string

    except Exception as e:
        return f"Error reading file content: {e}"