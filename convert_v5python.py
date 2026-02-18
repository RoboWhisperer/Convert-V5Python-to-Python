import json
import os
import sys
from datetime import datetime

def convert_v5python(input_file):
    # Load the JSON data from the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Extract the Python code from 'textContent'
    code = data.get('textContent', '')
    if not code:
        raise ValueError("No 'textContent' found in the input file.")
    
    # Determine the project name from the file name
    base_name = os.path.basename(input_file)
    name = base_name.replace('.v5python', '')
    
    # Ensure the name is not empty
    if not name:
        name = 'UnnamedProject'
    
    project_dir = name
    
    # Create the project directory and subdirectories
    os.makedirs(os.path.join(project_dir, 'src'), exist_ok=True)
    os.makedirs(os.path.join(project_dir, '.vscode'), exist_ok=True)
    
    # Write the Python code to src/main.py
    main_py_path = os.path.join(project_dir, 'src', 'main.py')
    with open(main_py_path, 'w', encoding='utf-8') as f:
        f.write(code)
    
    # Prepare the vex_project_settings.json content
    creation_date = datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p")
    slot = data.get('slot', 1) + 1
    sdk_version = 'V5_1_0_1_25'
    
    settings = {
        "extension": {
            "version": "0.7.2025041600",
            "json": 2
        },
        "project": {
            "name": name,
            "description": "",
            "creationDate": creation_date,
            "platform": "V5",
            "language": "python",
            "slot": slot,
            "sdkVersion": sdk_version,
            "python": {
                "main": "src/main.py"
            }
        }
    }
    
    # Write the settings to .vscode/vex_project_settings.json
    settings_path = os.path.join(project_dir, '.vscode', 'vex_project_settings.json')
    with open(settings_path, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=4)
    
    # Write the extensions.json file
    extensions = {
        "recommendations": [
            "ms-python.python"
        ]
    }
    extensions_path = os.path.join(project_dir, '.vscode', 'extensions.json')
    with open(extensions_path, 'w', encoding='utf-8') as f:
        json.dump(extensions, f, indent=4)
    
    # Write the settings.json file
    stub_path = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming', 'Code', 'User', 'globalStorage', 'vexrobotics.vexcode', 'sdk', 'python', 'V5', 'V5_1_0_1_25', 'vexv5', 'stubs')
    workspace_settings = {
        "python.analysis.stubPath": stub_path,
        "python.analysis.diagnosticMode": "workspace",
        "python.analysis.typeCheckingMode": "basic"
    }
    settings_json_path = os.path.join(project_dir, '.vscode', 'settings.json')
    with open(settings_json_path, 'w', encoding='utf-8') as f:
        json.dump(workspace_settings, f, indent=4)
    
    print(f"Project '{name}' created successfully in directory '{project_dir}'.")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python convert_v5python.py <input_file.v5python>")
        sys.exit(1)
    input_file = sys.argv[1]
    if not os.path.isfile(input_file):
        print(f"Error: File '{input_file}' does not exist.")
        sys.exit(1)
    try:
        convert_v5python(input_file)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
