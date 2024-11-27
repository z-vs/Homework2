import unittest
from unittest.mock import patch, MagicMock
import configparser
from main import read_config, is_git_repository, get_commits_for_file, generate_mermaid_graph, generate_image_from_mermaid


class TestVisualizer(unittest.TestCase):

