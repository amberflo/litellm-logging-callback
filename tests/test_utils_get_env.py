import os
import unittest
from unittest.mock import patch

from amberflo.utils import get_env, positive_int, boolean


class TestUtilsGetEnv(unittest.TestCase):
    @patch.dict(os.environ, {"KEY": "value"})
    def test_key_exists(self):
        value = get_env("KEY")
        self.assertEqual(value, "value")

    @patch.dict(os.environ, {})
    def test_key_no_exists_no_required(self):
        value = get_env("KEY")
        self.assertIsNone(value)

    @patch.dict(os.environ, {})
    def test_key_no_exists_required(self):
        with self.assertRaises(ValueError):
            get_env("KEY", required=True)

    @patch.dict(os.environ, {})
    def test_key_no_exists_required_with_default(self):
        value = get_env("KEY", "default", required=True)
        self.assertEquals(value, "default")

    @patch.dict(os.environ, {"KEY": "10"})
    def test_key_positive_int(self):
        value = get_env("KEY", validate=positive_int)
        self.assertEqual(value, 10)

    @patch.dict(os.environ, {"KEY": "invalid"})
    def test_key_not_a_positive_int(self):
        with self.assertRaises(ValueError):
            get_env("KEY", validate=positive_int)

    @patch.dict(os.environ, {"KEY": "true"})
    def test_key_boolean(self):
        value = get_env("KEY", validate=boolean)
        self.assertEqual(value, True)
