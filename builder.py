import os
import platform

import PyInstaller.__main__ as pyinstaller

import argparser
import cloner


def list_python_scripts(package):
    package_path = package.__path__[0]  # Get the package's directory path
    python_files = []
    for dirpath, dirnames, filenames in os.walk(package_path):
        for filename in filenames:
            if filename.endswith('.py'):
                relative_path = os.path.relpath(os.path.join(dirpath, filename), package_path)
                module_path = os.path.splitext(relative_path)[0].replace(os.sep, '.')
                python_files.append(module_path)

    return python_files


hidden_imports = list_python_scripts(argparser)
hidden_imports = [f"{argparser.__name__}.{file}" for file in hidden_imports]

excluded_files = ["*.env",
                  ".env",
                  "**/.env"]
pyinstaller_commands = ["--onefile",
                        "--name",
                        f"cloner-{platform.system()}"]

for hidden_import in hidden_imports:
    pyinstaller_commands.append("--hidden-import")
    pyinstaller_commands.append(f"{hidden_import}")
for excluded_file in excluded_files:
    pyinstaller_commands.append("--exclude")
    pyinstaller_commands.append(f"{excluded_file}")

pyinstaller_commands.append(f"{cloner.__name__}.py")

print(f"Command preview: \npyinstaller {' '.join(pyinstaller_commands)}")
pyinstaller.run(pyinstaller_commands)
