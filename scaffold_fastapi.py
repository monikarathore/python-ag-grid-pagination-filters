import os
import subprocess
import sys
import venv

# Define the folder and files structure
structure = {
    "app": {
        "__init__.py": "",
        "main.py": """from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
""",
        "routers": {
            "__init__.py": "",
            "example.py": """from fastapi import APIRouter

router = APIRouter()

@router.get("/example")
def get_example():
    return {"message": "This is an example route"}
"""
        },
        "models": {
            "__init__.py": "",
            "example.py": """from pydantic import BaseModel

class Example(BaseModel):
    id: int
    name: str
"""
        },
        "services": {
            "__init__.py": ""
        },
        "db": {
            "__init__.py": "",
            "database.py": "# Database connection setup goes here"
        },
        "core": {
            "__init__.py": "",
            "config.py": "# App configuration goes here"
        },
        "utils": {
            "__init__.py": "",
            "helpers.py": "# Utility functions go here"
        }
    }
}

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            with open(path, "w") as file:
                file.write(content)

def create_venv_and_requirements(venv_dir="venv"):
    print("🔧 Creating virtual environment...")
    venv.create(venv_dir, with_pip=True)

    # Create requirements.txt
    requirements = ["fastapi", "uvicorn[standard]"]
    with open("requirements.txt", "w") as f:
        f.write("\n".join(requirements))

    print("📦 requirements.txt created.")

    # Install dependencies in the virtual environment
    pip_path = os.path.join(venv_dir, "Scripts" if os.name == "nt" else "bin", "pip")
    print("⬇️ Installing packages...")
    subprocess.check_call([pip_path, "install", "-r", "requirements.txt"])
    print("Virtual environment setup complete.")

# Run the script to create the structure
if __name__ == "__main__":
    create_structure(".", structure)
    create_venv_and_requirements()
    print("FastAPI project structure created!")
