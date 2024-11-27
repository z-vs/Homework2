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

