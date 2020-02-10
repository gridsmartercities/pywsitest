import unittest

from pywsitest import WSTimeoutError


class WSTimeoutErrorTests(unittest.TestCase):

    def test_receive_timeout_error(self):
        with self.assertRaises(WSTimeoutError):
            raise WSTimeoutError()
