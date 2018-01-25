import json
from unittest import TestCase, mock

from lib.check import check


class TestCheck(TestCase):
    @mock.patch("lib.check.urlopen")
    def test_returns_all_versions_in_pypi_if_existing_version_unspecified(self, mock_urlopen):
        mock_urlopen.return_value.read.return_value = json.dumps(
            {"releases": {
                "1.0": {},
                "1.2": {},
                "2.1rc1": {},
                "3.0": {},
            }}
        )

        self.assertEqual(
            check("foo", None),
            [
                "3.0",
                "2.1rc1",
                "1.2",
                "1.0",
            ]
        )

        mock_urlopen.assert_called_once_with("https://pypi.python.org/pypi/foo/json")

    @mock.patch("lib.check.urlopen")
    def test_returns_all_versions_in_pypi_if_existing_version_specified(self, mock_urlopen):
        mock_urlopen.return_value.read.return_value = json.dumps(
            {"releases": {
                "1.0": {},
                "1.2": {},
                "2.1rc1": {},
                "3.0": {},
            }}
        )

        self.assertEqual(
            check("foo", "2.1rc1"),
            [
                "3.0",
                "2.1rc1"
            ]
        )
