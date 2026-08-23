"""Focused coverage for the TEXT-004 date and time filters."""

import json
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).parents[1]


def run_jq(program: str, input_value: object, *, timezone: str = "UTC") -> tuple[int, list[object]]:
    environment = {**os.environ, "TZ": timezone}
    result = subprocess.run(
        [str(ROOT / "jq"), "-c", program],
        input=json.dumps(input_value) + "\n",
        capture_output=True,
        text=True,
        env=environment,
        check=False,
    )
    return result.returncode, [json.loads(line) for line in result.stdout.splitlines()]


def test_iso_date_aliases_round_trip_in_utc() -> None:
    assert run_jq("fromdate", "2015-03-05T23:51:47Z") == (0, [1425599507])
    assert run_jq("fromdateiso8601", "2015-03-05T23:51:47Z") == (0, [1425599507])
    assert run_jq("todate", 1425599507) == (0, ["2015-03-05T23:51:47Z"])
    assert run_jq("todateiso8601", 1425599507) == (0, ["2015-03-05T23:51:47Z"])


def test_broken_down_time_filters_use_jq_calendar_shape() -> None:
    broken_down = [2015, 2, 5, 23, 51, 47, 4, 63]
    assert run_jq('strptime("%Y-%m-%dT%H:%M:%SZ")', "2015-03-05T23:51:47Z") == (0, [broken_down])
    assert run_jq('strftime("%Y-%m-%dT%H:%M:%SZ")', broken_down) == (0, ["2015-03-05T23:51:47Z"])
    assert run_jq('strflocaltime("%Y-%m-%dT%H:%M:%SZ")', broken_down) == (0, ["2015-03-05T23:51:47Z"])
    assert run_jq("gmtime", 1425599507) == (0, [broken_down])
    assert run_jq("localtime", 1425599507) == (0, [broken_down])
    assert run_jq("mktime", [2024, 8, 21]) == (0, [1726876800])


def test_date_filters_return_runtime_failure_for_invalid_input() -> None:
    assert run_jq("fromdate", 3)[0] == 5
    assert run_jq("todate", "not-a-number")[0] == 5
    assert run_jq("mktime", ["year", 0, 1])[0] == 5
