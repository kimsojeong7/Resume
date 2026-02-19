import requests
import os

# ====== 설정 ======
GITHUB_USERNAME = "your_username"
REPO_NAME = "your_repo"
BRANCH = "main"
TOKEN = "your_personal_access_token"  # 보안상 실제 업로드 시 환경변수 추천
OUTPUT_FILE = "contents.html"
# ==================

API_URL = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents"

headers = {
    "Authorization": f"token {TOKEN}"
}

def fetch_contents(url):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def generate_html(contents):
    html = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>Repository Contents</title>
<style>
body {
    font-family: Arial;
    background: #0f172a;
    color: white;
    padding: 40px;
}
h1 { color: #38bdf8; }
ul { list-style: none; padding: 0; }
li { margin: 10px 0; }
a {
    color: #38bdf8;
    text-decoration: none;
}
a:hover { text-decoration: underline; }
.folder { color: #facc15; }
</style>
</head>
<body>
<h1>📂 Repository Contents</h1>
<ul>
"""

    for item in contents:
        name = item["name"]
        item_type = item["type"]

        if item_type == "dir":
            html += f'<li class="folder">📁 {name}/</li>\n'

        elif item_type == "file" and name.endswith(".html"):
            page_url = f"https://{GITHUB_USERNAME}.github.io/{REPO_NAME}/{name}"
            html += f'<li>📄 <a href="{page_url}" target="_blank">{name}</a></li>\n'

    html += """
</ul>
</body>
</html>
"""
    return html


def main():
    contents = fetch_contents(API_URL)
    html_content = generate_html(contents)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"{OUTPUT_FILE} 생성 완료!")


if __name__ == "__main__":
    main()
