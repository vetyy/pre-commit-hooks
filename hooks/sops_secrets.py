import argparse
import json
import logging
import sys
from typing import Optional, Sequence

import ruyaml as yaml

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


def check_file(filename):
    with open(filename, 'rb') as f:
        if filename.endswith((".yml", ".yaml")):
            decoder = yaml.safe_load
        elif filename.endswith(".json"):
            decoder = json.load
        else:
            raise Exception("Unsupported file type, only JSON or YAML is allowed")

        try:
            data = decoder(f)
        except Exception as e:
            raise Exception(f"Failed to decode file '{filename}': {e}")

        if not isinstance(data, dict) or 'sops' not in data:
            raise Exception(f"Trying to commit unencrypted SOPS file '{filename}'")


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--files', nargs='+', help='Encrypted files to check.', required=True)
    args = parser.parse_args(argv)

    retval = 0
    for f in args.files:
        try:
            check_file(f)
        except Exception as e:
            logger.error(e)
            retval = 1

    return retval


if __name__ == '__main__':
    raise SystemExit(main())
