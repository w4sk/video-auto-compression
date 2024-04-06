import subprocess

result = subprocess.run(['cmd', '/c', 'dir'], capture_output=True, text=True)

print(result.stdout)

if result.stderr:
    print(result.stderr)