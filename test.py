import unittest
from unittest.mock import patch, MagicMock
import configparser
import subprocess
import os
import git
from main import load_config, get_commits_with_file, generate_mermaid_graph, generate_graph_image


class TestGraphGenerator(unittest.TestCase):

    @patch('configparser.ConfigParser.read')
    def test_load_config(self, mock_read):
        mock_read.return_value = None
        config_data = {
            'settings': {
                'graph_tool': 'mermaid-cli',
                'repository_path': '/path/to/repo',
                'output_image': 'output.png',
                'file_path': 'src/example.py'
            }
        }
        mock_config = MagicMock()
        mock_config.__getitem__.side_effect = config_data.__getitem__

        with patch('configparser.ConfigParser', return_value=mock_config):
            config = load_config("config.ini")
            self.assertEqual(config['graph_tool'], 'mermaid-cli')
            self.assertEqual(config['repository_path'], '/path/to/repo')
            self.assertEqual(config['output_image'], 'output.png')
            self.assertEqual(config['file_path'], 'src/example.py')

    @patch('git.Repo')
    def test_get_commits_with_file(self, mock_repo):
        mock_commit = MagicMock()
        mock_commit.hexsha = 'abc123'
        mock_repo.return_value.iter_commits.return_value = [mock_commit]

        commits = get_commits_with_file('/path/to/repo', 'src/example.py')
        self.assertEqual(len(commits), 1)
        self.assertEqual(commits[0].hexsha, 'abc123')

    def test_generate_mermaid_graph(self):
        commit1 = MagicMock()
        commit1.hexsha = 'abc123'
        commit1.parents = []

        commit2 = MagicMock()
        commit2.hexsha = 'def456'
        commit2.parents = [commit1]

        graph = generate_mermaid_graph([commit1, commit2])
        expected_graph = 'graph LR\n    abc123 --> def456\n'
        self.assertEqual(graph, expected_graph)

    @patch('subprocess.run')
    @patch('os.remove')
    def test_generate_graph_image(self, mock_remove, mock_run):
        mock_run.return_value = None

        graph_description = 'graph LR\n    a --> b\n'
        generate_graph_image('mermaid-cli', graph_description, 'output.png')

        mock_run.assert_called_once_with(['mermaid-cli', '-i', 'temp.mmd', '-o', 'output.png'], check=True)
        mock_remove.assert_called_once_with("temp.mmd")


if __name__ == '__main__':
    unittest.main()
