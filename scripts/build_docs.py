import os
from util import (
    get_image,
    image_mapper,
    load_cached_difficulties,
    save_cached_difficulties,
    get_problem_difficulty,
)

# If you want to exclude some files from language icons, keep this
file_whitelist = {"bnn_accuracy.py", "testing_tool.py", "unununion_find.py"}


def build_problem_table():
    difficulty_cache = load_cached_difficulties()
    problem_rows = []

    # Iterate through files in the 'solutions' directory
    for file in sorted(os.listdir("solutions")):
        file_path = os.path.join("solutions", file)

        # Check if it's a valid solution file
        if os.path.isfile(file_path):
            ext = file.split(".")[-1]
            if ext in image_mapper:
                pid = file.split(".")[0]  # Problem ID from file name

                kattis_url = f"https://open.kattis.com/problems/{pid}"
                repo_url = (
                    "https://github.com/simonwinther/kattis-cp/tree/main/solutions/"
                    f"{file}"
                )

                # Get problem difficulty, either from cache or by fetching from Kattis
                difficulty = get_problem_difficulty(pid, difficulty_cache)

                # Language icon linking to GitHub solution (or empty if whitelisted)
                if file not in file_whitelist:
                    lang_icon = (
                        f'<a href="{repo_url}" target="_blank">'
                        f'<img alt="{ext}" src="{get_image(ext)}" /></a>'
                    )
                else:
                    lang_icon = ""

                # Generate a table row for the problem
                row = f"""
                <tr>
                    <td><a href="{kattis_url}">{pid.replace('_', ' ').title()}</a></td>
                    <td>{pid}</td>
                    <td>{difficulty}</td>
                    <td class="language-icon">{lang_icon}</td>
                </tr>"""
                # If you ever want a separate GitHub icon instead, you can use:
                # <td class="language-icon"><a href="{repo_url}"><img alt="GitHub" src="{github_icon}" /></a></td>

                problem_rows.append(row)

    # Save the updated difficulties cache
    save_cached_difficulties(difficulty_cache)

    return problem_rows


def insert_problems_into_html():
    with open("docs/index.html", "r", encoding="utf8") as f:
        lines = f.readlines()

    start_marker = "<!-- START_PROBLEM -->"
    end_marker = "<!-- END_PROBLEM -->"

    start_index, end_index = None, None
    for i, line in enumerate(lines):
        if start_marker in line:
            start_index = i
        if end_marker in line:
            end_index = i
            break

    if start_index is not None and end_index is not None:
        problem_rows = build_problem_table()
        lines = lines[: start_index + 1] + problem_rows + lines[end_index:]

    with open("docs/index.html", "w", encoding="utf8") as f:
        f.writelines(lines)


# Run the script
if __name__ == "__main__":
    insert_problems_into_html()

