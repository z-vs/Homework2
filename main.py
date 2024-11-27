import subprocess
import configparser


def read_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def is_git_repository(repo_path):
    command = f"git -C {repo_path} rev-parse --is-inside-work-tree"
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip() == "true"
    except subprocess.CalledProcessError:
        return False


def get_commits_for_file(repo_path, file_hash):
    command = f"git -C {repo_path} log --pretty=format:'%H' --name-only --diff-filter=AM {file_hash}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    commits = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    return commits


def generate_mermaid_graph(commits):
    mermaid_graph = "graph TD\n"
    for i, commit in enumerate(commits[:-1]):
        mermaid_graph += f"    {commit} --> {commits[i+1]}\n"
    return mermaid_graph


def generate_image_from_mermaid(graph_description, output_image, graph_tool_path):
    with open('graph.mmd', 'w') as f:
        f.write(graph_description)
    subprocess.run([graph_tool_path, '-i', 'graph.mmd', '-o', output_image])


def main():
    config = read_config('config2.ini')
    graph_tool = config['settings']['graph_tool']
    repo_path = config['settings']['repository_path']
    output_image = config['settings']['output_image']
    file_hash = config['settings']['file_hash']
    commits = get_commits_for_file(repo_path, file_hash)

    if not commits:
        print("No commits found with the specified file hash.")
        return

    graph_description = generate_mermaid_graph(commits)

    generate_image_from_mermaid(graph_description, output_image, graph_tool)
    print(f"Graph successfully generated and saved to {output_image}")


if __name__ == "__main__":
    main()
