import json
from pathlib import Path

from conventional_commit_cli.calculate import calculate_bump, calculate_new_version
from conventional_commit_cli.validate import parse


def test__parse__correct_type_and_breaking():
    current_file_path = Path(__file__)
    test_data_path = current_file_path.parent / "data"

    for test_file in test_data_path.glob("*.json"):
        with open(test_file) as in_f:
            test_data = json.load(in_f)

            parsed_message = parse(test_data["message"])
            assert parsed_message.header["type"] == test_data["type"]
            assert parsed_message.breaking["flag"] == test_data["breaking_flag"]
            assert parsed_message.breaking["token"] == test_data["breaking_token"]
            assert parsed_message.header["scope"] == test_data["scope"]


def test__calculate__correct_bump():
    current_file_path = Path(__file__)
    test_data_path = current_file_path.parent / "data"

    for test_file in test_data_path.glob("*.json"):
        with open(test_file) as in_f:
            test_data = json.load(in_f)

            parsed_message = parse(test_data["message"])
            bump = calculate_bump(parsed_message)

            assert bump == test_data["bump"]


def test__calculate__new_version():
    current_file_path = Path(__file__)
    test_data_path = current_file_path.parent / "data"

    for test_file in test_data_path.glob("*.json"):
        with open(test_file) as in_f:
            test_data = json.load(in_f)

            parsed_message = parse(test_data["message"])
            bump = calculate_bump(parsed_message)

            new_version = calculate_new_version(test_data["old_version"], bump)

            assert str(new_version) == test_data["new_version"]
