import unittest
from unittest.mock import patch, MagicMock
import configparser
from main import main, load_config, get_commits_with_file, generate_mermaid_graph, generate_graph_image


class TestVisualizer(unittest.TestCase):

    @patch('configparser.ConfigParser')
    def test_load_config(self, mock_config_parser_class):
        mock_config_parser = MagicMock(spec=configparser.ConfigParser)
        mock_config_parser.read.return_value = None
        mock_config_parser.__getitem__.return_value = {
            'graph_tool': "C:\\path\\to\\mmdc.cmd",
            'repository_path': "C:\\path\\to\\repo",
            'output_image': "C:\\path\\to\\output.png",
            'file_path': "path\\to\\file.py"
        }
        mock_config_parser.sections.return_value = ['settings']
        with patch('configparser.ConfigParser', return_value=mock_config_parser):
            config = load_config("config2.ini")
        self.assertEqual(config['graph_tool'], "C:\\path\\to\\mmdc.cmd")
        self.assertEqual(config['repository_path'], "C:\\path\\to\\repo")
        self.assertEqual(config['output_image'], "C:\\path\\to\\output.png")
        self.assertEqual(config['file_path'], "path\\to\\file.py")

    @patch('git.Repo')
    def test_get_commits_with_file(self, mock_repo_class):
        mock_repo = MagicMock()
        mock_commit = MagicMock()
        mock_commit.hexsha = "123abc"
        mock_commit.parents = []
        mock_repo.iter_commits.return_value = [mock_commit]
        with patch('git.Repo', return_value=mock_repo):
            commits = get_commits_with_file("C:\\path\\to\\repo", "path\\to\\file.py")
        self.assertEqual(len(commits), 1)
        self.assertEqual(commits[0].hexsha, "123abc")

    def test_generate_mermaid_graph(self):
        mock_commit_1 = MagicMock()
        mock_commit_1.hexsha = "123abc"
        mock_commit_1.parents = []
        mock_commit_2 = MagicMock()
        mock_commit_2.hexsha = "456def"
        mock_commit_2.parents = [mock_commit_1]
        commits = [mock_commit_1, mock_commit_2]
        graph = generate_mermaid_graph(commits)
        expected_graph = 'graph LR\n    123abc --> 456def\n'
        self.assertEqual(graph, expected_graph)

    @patch('subprocess.run')
    def test_generate_graph_image(self, mock_subprocess_run):
        mock_subprocess_run.return_value = None
        graph_tool = "C:\\path\\to\\mmdc.cmd"
        graph_description = "graph LR\n    123abc --> 456def\n"
        output_image = "C:\\path\\to\\output.png"
        generate_graph_image(graph_tool, graph_description, output_image)
        mock_subprocess_run.assert_called_once_with([graph_tool, "-i", "temp.mmd", "-o", output_image])


    @patch('configparser.ConfigParser')
    def test_load_config_file_not_found(self, mock_config_parser_class):
        with self.assertRaises(FileNotFoundError):
            load_config("non_existent_config.ini")

    @patch('git.Repo')
    def test_get_commits_with_file_no_commits(self, mock_repo_class):
        mock_repo = MagicMock()
        mock_repo.iter_commits.return_value = []
        with patch('git.Repo', return_value=mock_repo):
            commits = get_commits_with_file("C:\\path\\to\\repo", "path\\to\\file.py")
        self.assertEqual(len(commits), 0)

    @patch('subprocess.run')
    def test_generate_graph_image_subprocess_error(self, mock_subprocess_run):
        mock_subprocess_run.side_effect = Exception("Subprocess failed")
        graph_tool = "C:\\path\\to\\mmdc.cmd"
        graph_description = "graph LR\n    123abc --> 456def\n"
        output_image = "C:\\path\\to\\output.png"
        with self.assertRaises(Exception):
            generate_graph_image(graph_tool, graph_description, output_image)


if __name__ == '__main__':
    unittest.main()
