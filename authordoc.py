# Christiano Blairoy Fernandes
# 23f2004927
# 6 April 2026
# authordoc.py

import os
from datetime import datetime

# --- Configuration ---
NAME = "Christiano Blairoy Fernandes"
STUDENT_ID = "23f2004927"
# Formats as "DD Month YYYY"
CURRENT_DATE = datetime.now().strftime("%-d %B %Y")


def make_header(relative_path):
    if relative_path.endswith(".html"):
        return (
            f"<!--\n"
            f"  {NAME}\n"
            f"  {STUDENT_ID}\n"
            f"  {CURRENT_DATE}\n"
            f"  {relative_path}\n"
            f"-->\n\n"
        )
    else:
        return f"# {NAME}\n# {STUDENT_ID}\n# {CURRENT_DATE}\n# {relative_path}\n\n"


def update_headers():
    for root, dirs, files in os.walk("."):
        # Skip the virtual environment and git folders
        if ".venv" in root or ".git" in root:
            continue

        for file in files:
            if file.endswith(".py") and file != "header_script.py" or file.endswith(".html"):
                file_path = os.path.join(root, file)

                # Get the path relative to the root (e.g., 'models/drive.py')
                relative_path = os.path.relpath(file_path, ".")

                header = make_header(relative_path)

                with open(file_path, "r") as f:
                    content = f.read()

                # Safety check: Don't add if the name is already near the top
                if f"{NAME}" in content[:100]:
                    print(f"Skipping: {relative_path} (Header already exists)")
                    continue

                with open(file_path, "w") as f:
                    f.write(header + content)
                print(f"Updated:  {relative_path}")


if __name__ == "__main__":
    update_headers()