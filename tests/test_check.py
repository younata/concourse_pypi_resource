import json
from unittest import TestCase, mock

from lib.check import check, main


@mock.patch("lib.check.urlopen")
class TestCheck(TestCase):
    def test_returns_last_version_in_pypi_if_existing_version_unspecified(self, mock_urlopen):
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
                {"version": "3.0"}
            ]
        )

        mock_urlopen.assert_called_once_with("https://pypi.python.org/pypi/foo/json")

    def test_returns_versions_in_pypi_more_recent_and_equal_to_existing_if_existing_version_specified(self, mock_urlopen):
        mock_urlopen.return_value.read.return_value = json.dumps(
            {"releases": {
                "1.0": {},
                "1.2": {},
                "2.1rc1": {},
                "3.0": {},
            }}
        )

        self.assertEqual(
            check("foo", {"version": "2.1rc1"}),
            [
                {"version": "3.0"},
                {"version": "2.1rc1"}
            ]
        )


@mock.patch("lib.check.print")
@mock.patch("lib.check.check", return_value=[])
@mock.patch("lib.check.sys.stdin")
class TestMain(TestCase):
    def test_when_only_source_is_given_it_parses_stdin_as_json_and_passes_source_to_check(self, mock_stdin, mock_check, _):
        mock_stdin.read.return_value = '{"source": {"package": "tox"}}'

        main()

        mock_check.assert_called_once_with(package_name="tox", existing_version=None)

    def test_when_both_source_and_version_is_given_it_parses_stdin_as_json_and_passes_both_to_check(self, mock_stdin, mock_check, _):
        mock_stdin.read.return_value = json.dumps({
            "source": {"package": "tox"},
            "version": {"version": "3.0"}
        })

        main()

        mock_check.assert_called_once_with(package_name="tox", existing_version={"version": "3.0"})

    def test_when_version_is_given_but_is_none_it_parses_stdin_as_json_and_passes_version_as_none_to_check(self, mock_stdin, mock_check, _):
        mock_stdin.read.return_value = json.dumps({
            "source": {"package": "tox"},
            "version": None
        })

        main()

        mock_check.assert_called_once_with(package_name="tox", existing_version=None)

    def test_when_check_finishes_prints_result_as_json_to_stdout(self, mock_stdin, mock_check, mock_print):
        mock_stdin.read.return_value = '{"source": {"package": "tox"}}'
        mock_check.return_value = [{"version": "1.0"}]

        main()

        mock_print.assert_called_once_with('[{"version": "1.0"}]')
