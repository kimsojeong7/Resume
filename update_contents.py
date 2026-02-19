import requests
import os
from datetime import datetime

GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
REPO_NAME = os.getenv("REPO_NAME")
BRANCH = "main"

API_URL = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents"

def fetch_recursive(path=""):
    url = f"{API_URL}/{path}"
    response = requests.get(url)
    response.raise_for_status()
    items = response.json()

    html_files = []

    for item in items:
        if item["type"] == "dir":
            html_files.extend(fetch_recursive(item["path"]))
        elif item["type"] == "file" and item["name"].endswith(".html"):
            html_files.append(item["path"])

    return html_files


def generate_html(file_list):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    html = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>Repository Contents</title>
<style>
body {{
    font-family: 'Segoe UI';
    background: linear-gradient(135deg,#0f172a,#020617);
    color: #e2e8f0;
    padding: 50px;
}}
h1 {{
    color: #38bdf8;
    margin-bottom: 20px;
}}
ul {{
    list-style:none;
    padding:0;
}}
li {{
    background:#1e293b;
    padding:15px;
    margin:10px 0;
    border-radius:10px;
    transition:0.3s;
}}
li:hover {{
    transform:translateX(10px);
    background:#24324a;
}}
a {{
    color:#38bdf8;
    text-decoration:none;
}}
.footer {{
    margin-top:40px;
    font-size:14px;
    color:#64748b;
}}
</style>
</head>
<body>

<h1>📂 Repository HTML Contents</h1>
<ul>
"""

    for file in sorted(file_list):
        page_url = f"https://{GITHUB_USERNAME}.github.io/{REPO_NAME}/{file}"
        html += f'<li>📄 <a href="{page_url}" target="_blank">{file}</a></li>\n'

    html += f"""
</ul>

<div class="footer">
자동 업데이트 시간: {now}
</div>

</body>
</html>
"""
    return html


def main():
    files = fetch_recursive()
    html_content = generate_html(files)

    with open("contents.html", "w", encoding="utf-8") as f:
        f.write(html_content)


if __name__ == "__main__":
    main()
