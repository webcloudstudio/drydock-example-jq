from hashlib import sha256
from pathlib import Path
import subprocess


ASSET_HASHES = {
    "sources/INSTRUCTIONS.md": "1257c99beb99ebfca4a32b8e4aba86d8b6304cbfbf74cc6ef311cada4c0de734",
    "sources/builtin.jq": "b8a5fd9579be9b51c9a04e6620f8c1655539aa57eea33a84e202a8dea401f2a4",
    "sources/exclusions.txt": "0755022f0c2f339883aaa2668a10d6a11bc8f7c4a37b0743f213830d848a05d9",
    "sources/full_test.sh": "4df25cda12c2741ee02cb7e22d5e3b62161bd90fde948c88a675cb2a94e70fc5",
    "sources/jq-manual.txt": "92fc1c179ee6e33d75ffc1f24dd1f0b8ddf5ea666a51224be5088d9431cd8ab3",
    "sources/jq.test": "329689763b651096989bd8260b643731083fc5fd17f6bd7834d158713f738cbd",
    "sources/lexer.l": "cfb3af17a786df30d7e30dae5861b84747d4904f8ce7ae9ab9b48bde342ee7f3",
    "sources/parser.y": "803aa7c0b1acba2228e52d1de392fb51e60a7bbe23e42870aea1d62c43360c60",
    "sources/run_conformance.py": "c1b5be717d542f2d2dc4f4a694dd02ae8c8f84b25f15c6224fbb6a784abe7492",
}


def test_declared_assets_are_nonempty_and_byte_stable() -> None:
    for name, expected_hash in ASSET_HASHES.items():
        path = Path(name)
        assert path.is_file()
        assert path.stat().st_size > 0
        assert sha256(path.read_bytes()).hexdigest() == expected_hash


def test_scoring_entry_point_is_executable_by_sh() -> None:
    result = subprocess.run(
        ["sh", "sources/full_test.sh", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 127
