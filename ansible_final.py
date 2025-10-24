import subprocess
import os

def showrun(ip):
    # read https://www.datacamp.com/tutorial/python-subprocess to learn more about subprocess
    command = [
        "ansible-playbook",
        "playbook.yaml",
        "--extra-vars",
        f"target_ip={ip}"
    ]
    result = subprocess.run(command, capture_output=True, text=True)

    print(result.stdout)
    print(result.stderr)

    output = result.stdout
    if "failed=0" in output:
        current_dir = os.getcwd()
        txt_files = [
            f for f in os.listdir(current_dir)
            if f.startswith("show_run_66070179_") and f.endswith(".txt")
        ]
        if txt_files:
            file_path = os.path.join(current_dir, txt_files[0])
            print("found backup")
            return file_path
        else:
            return "Error: No backup file found"
    else:
        return 'Error: Ansible'
