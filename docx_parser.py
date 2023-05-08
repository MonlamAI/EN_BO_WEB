import docx
from pathlib import Path
from time import sleep
from collections import deque
import uuid
import os
from github_utils import github_publish,create_github_issue,close_github_issue,delete_repo



def split_docx(doc):
    splitted_files = []
    last_font_size = 0
    texts = []
    for i,cur_para in enumerate(doc.paragraphs):
        print(cur_para.text)
        print(len(cur_para.text))
        
        if cur_para.style.name == 'Heading 1':
            if cur_para.style.font.size != last_font_size and i != 0:
                splitted_files.append('\n'.join(texts))
                texts = []
        texts.append(cur_para.text)
        last_font_size = cur_para.style.font.size if len(cur_para.text)!=0 else last_font_size

    return splitted_files


def create_repo(text,repo_name):
    repo_path = f"./data/{repo_name}"
    Path(repo_path).mkdir(exist_ok=True, parents=True)
    text_path = f"{repo_path}/{repo_name}.txt"
    Path(text_path).write_text(text)
    create_readme(Path(repo_path))
    github_publish(
        path = repo_path,
        not_includes=[],
        org="MonlamAI",
        token = os.getenv("GITHUB_TOKEN")
    )
    issue = create_github_issue(Path(repo_path).name)
    close_github_issue(Path(repo_path).name,issue.number)
    return repo_path


def create_readme(path):
    result = "# EN_BO_WEB"
    readme_fn = path / "README.md"
    readme_fn.write_text(result)


def create_repos(texts):
    start_index = 7000
    repos = []
    langs = deque(["BO","EN"])
    for i,text in enumerate(texts):
        if i % 2 == 0 and i != 0:
            start_index += 1
        lang = langs.popleft()
        langs.append(lang)
        repo_name = f"{lang}{start_index}"
        repos.append(create_repo(text,repo_name))
    return repos

def main(docx_path):
    doc = docx.Document(docx_path)
    texts = split_docx(doc)
    repos = create_repos(texts)

if __name__ == "__main__":
    docx_path = "article_docx/03.བོད་འགྱུར་དྲ་རྩོམ།.docx"
    main(docx_path)
   

