import configparser
import git
import subprocess
import os


def load_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)

    graph_tool = config['settings']['graph_tool']
    repository_path = config['settings']['repository_path']
    output_image = config['settings']['output_image']
    file_path = config['settings']['file_path']

    return {
        'graph_tool': graph_tool,
        'repository_path': repository_path,
        'output_image': output_image,
        'file_path': file_path
    }


def get_commits_with_file(repository_path, file_path):
    repo = git.Repo(repository_path)
    commits = []
    for commit in repo.iter_commits(paths=file_path):
        commits.append(commit)
    return commits



def generate_mermaid_graph(commits):
    mermaid_graph = 'graph LR\n'
    commit_map = {}

    for commit in commits:
        commit_map[commit.hexsha] = commit

    for commit in commits:
        for parent in commit.parents:
            if parent.hexsha not in commit_map:
                commit_map[parent.hexsha] = parent
            mermaid_graph += f'    {parent.hexsha} --> {commit.hexsha}\n'

    return mermaid_graph


def generate_graph_image(graph_tool, graph_description, output_image):
    with open("temp.mmd", "w") as f:
        f.write(graph_description)

    command = [graph_tool, "-i", "temp.mmd", "-o", output_image]
    subprocess.run(command, check=True)

    os.remove("temp.mmd")


def main(config_path):
    config = load_config(config_path)

    commits = get_commits_with_file(config['repository_path'], config['file_path'])

    if not commits:
        print("Не найдено коммитов с данным файлом.")
        return

    graph_description = generate_mermaid_graph(commits)

    try:
        generate_graph_image(config['graph_tool'], graph_description, config['output_image'])
        print(f"Граф зависимостей успешно сгенерирован и сохранен в {config['output_image']}")
    except Exception as e:
        print(f"Ошибка при генерации графа: {e}")



if __name__ == "__main__":
    config_path = "config2.ini"
    main(config_path)
