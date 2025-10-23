import os
import tempfile

def save_uploaded_file(uploaded_file):
    """
    Save an uploaded CSV file to a temporary directory
    and return its local path.
    """
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path
