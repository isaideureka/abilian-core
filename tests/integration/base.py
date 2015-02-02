"""
Base TestCase for integration tests.
"""

# Don't remove
import fix_path  # noqa

import os

from abilian.testing import BaseTestCase

from .config import TestConfig

BASEDIR = os.path.dirname(__file__)


class IntegrationTestCase(BaseTestCase):
  config_class = TestConfig
  no_login = False
