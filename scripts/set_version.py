import re

# Load the version number from the pyproject.toml file
with open('pyproject.toml', 'r') as f:
    contents = f.read()
    version = re.search(r'^version = "([\d\.]+)"', contents, re.MULTILINE).group(1)

# Replace the version placeholder in the source code file with the actual version number
source_file = 'lib/version.py'

with open(source_file, 'w') as f:
    f.write(f'VERSION: str = "{version}"\n')

print(f'Version number set to {version}')
