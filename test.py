import unittest
from unittest.mock import patch, MagicMock
import configparser
from main import read_config, is_git_repository, get_commits_for_file, generate_mermaid_graph, generate_image_from_mermaid


class TestVisualizer(unittest.TestCase):

    def test_read_config(self):
        config = configparser.ConfigParser()
        config.read_dict({
            'settings': {
                'graph_tool': 'C:\\path\\to\\graph_tool',
                'repository_path': 'C:\\path\\to\\repository',
                'output_image': 'C:\\path\\to\\output_image.png',
                'file_hash': '0d84766dcf4426dcd416471f849249440898b65c'
            }
        })
        self.assertEqual(config['settings']['graph_tool'], "C:\\path\\to\\graph_tool")
        self.assertEqual(config['settings']['repository_path'], "C:\\path\\to\\repository")
        self.assertEqual(config['settings']['output_image'], "C:\\path\\to\\output_image.png")
        self.assertEqual(config['settings']['file_hash'], "0d84766dcf4426dcd416471f849249440898b65c")

    @patch('subprocess.run')
    def test_is_git_repository(self, mock_run):
        mock_run.return_value = MagicMock(stdout="true", returncode=0)
        self.assertTrue(is_git_repository('C:\\path\\to\\repository'))

        mock_run.return_value = MagicMock(stdout="false", returncode=0)
        self.assertFalse(is_git_repository('C:\\path\\to\\repository'))

    @patch('subprocess.run')
    def test_get_commits_for_file(self, mock_run):
        mock_run.return_value = MagicMock(stdout="commit1\ncommit2\n", returncode=0)
        commits = get_commits_for_file('C:\\path\\to\\repository', '0d84766dcf4426dcd416471f849249440898b65c')

        self.assertEqual(commits, ['commit1', 'commit2'])

    def test_generate_mermaid_graph(self):
        commits = ['commit1', 'commit2', 'commit3']
        graph = generate_mermaid_graph(commits)

        self.assertIn("graph TD", graph)
        self.assertIn("commit1 --> commit2", graph)
        self.assertIn("commit2 --> commit3", graph)

    @patch('subprocess.run')
    def test_generate_image_from_mermaid(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        generate_image_from_mermaid("graph TD\n commit1 --> commit2", 'output_image.png', 'mmdc')
        mock_run.assert_called_with(['mmdc', '-i', 'graph.mmd', '-o', 'output_image.png'])


if __name__ == '__main__':
    unittest.main()
