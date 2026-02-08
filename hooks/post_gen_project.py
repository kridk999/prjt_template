import shutil
from pathlib import Path
import logging
from keyword import iskeyword

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)


project_name = "{{cookiecutter.project_name}}"
python_version = "{{cookiecutter.python_version}}"
deps_manager = "{{cookiecutter.deps_manager}}"
torch_device = "{{cookiecutter.torch_device}}"

logger.info(f"Project name: {project_name}")
logger.info(f"Python version: {python_version}")
logger.info(f"Dependencies manager: {deps_manager}")
logger.info(f"PyTorch device: {torch_device}")

# Check if the project name is a valid Python identifier and is lowercase, as this will cause syntax errors when trying to import the project
if not project_name.isidentifier() or not project_name.islower():
    raise ValueError(
        "\n"
        "Project name must be a valid project name, meaning that it must be a valid Python name and also be lowercase."
        " This means that it must not contain spaces or special characters, and must not start with a number."
        " In general it is best to use only lowercase letters and underscores."
        " You can read more about Python naming conventions for packages here:"
        " https://peps.python.org/pep-0008/#package-and-module-names"
        "\n",
    )
    
# Check if the project name is a built-in keyword, as this will cause syntax errors when trying to import the project
if iskeyword(project_name):
    raise ValueError(
        "Project name must not be a built-in keyword, as it will cause syntax errors.",
    )

# Rename and remove files and folders based on the selected dependencies manager and PyTorch device
if deps_manager == "uv":
    logger.info("Renaming files and folders for the uv template.")
    Path("requirements_noTorch.txt").unlink()
    Path("requirements_cu124.txt").unlink()
    Path("requirements_cpu.txt").unlink()
    Path("requirements_dev.txt").unlink()
    Path("pyproject_pip.toml").unlink()
    if torch_device == "cpu/mps":
        Path("pyproject_uv_cu124.toml").unlink()
        Path("pyproject_uv_noTorch.toml").unlink()
        Path("pyproject_uv_cpu.toml").rename("pyproject.toml")
    elif torch_device == "cuda":
        Path("pyproject_uv_cpu.toml").unlink()
        Path("pyproject_uv_noTorch.toml").unlink()
        Path("pyproject_uv_cu124.toml").rename("pyproject.toml")
    else:
        Path("pyproject_uv_cpu.toml").unlink()
        Path("pyproject_uv_cu124.toml").unlink()
        Path("pyproject_uv_noTorch.toml").rename("pyproject.toml")
elif deps_manager == "pip":
    logger.info("Renaming files and folders for the pip template.")
    Path("pyproject_uv_cu124.toml").unlink()
    Path("pyproject_uv_noTorch.toml").unlink()
    Path("pyproject_uv_cpu.toml").unlink()
    if torch_device == "cpu/mps":
        Path("requirements_cu124.txt").unlink()
        Path("requirements_noTorch.txt").unlink()
        Path("requirements_cpu.txt").rename("requirements.txt")
    elif torch_device == "cuda":
        Path("requirements_cpu.txt").unlink()
        Path("requirements_noTorch.txt").unlink()
        Path("requirements_cu124.txt").rename("requirements.txt")
    else:
        Path("requirements_cpu.txt").unlink()
        Path("requirements_cu124.txt").unlink()
        Path("requirements_noTorch.txt").rename("requirements.txt")
        
############################################################################