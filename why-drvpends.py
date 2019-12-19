#!/usr/bin/env python3

import json
import argparse
from pprint import pprint
from functools import lru_cache
from typing import List, Union, Any, Generator
import subprocess


def debug(msg: str):
    # print(msg)
    pass


req_calls: int = 0


@lru_cache(maxsize=4096)
def requisites(drv: str) -> List[str]:
    global req_calls
    req_calls += 1
    debug(f"requisite_calls: {req_calls}")

    proc = subprocess.run(
        ["nix", "show-derivation", drv], capture_output=True, check=True
    )
    result = json.loads(proc.stdout)[drv]

    return list(result["inputDrvs"].keys())


spelunk_calls: int = 0


@lru_cache(maxsize=4096)
def spelunk(package_drv: str, dependency_drv: str) -> Generator[List[str], None, None]:
    global spelunk_calls
    spelunk_calls += 1
    debug(f"spelunk_calls: {spelunk_calls}")

    debug(f"{package_drv} -> {dependency_drv}")

    for path in requisites(package_drv):
        if path == dependency_drv:
            yield [path]
        else:
            for p in spelunk(path, dependency_drv):
                yield [package_drv] + p


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("package_drv")
    parser.add_argument("dependency_drv")
    parser.add_argument("--flame", action="store_true")
    args = parser.parse_args()

    for route in spelunk(args.package_drv, args.dependency_drv):
        if args.flame:
            print("{stack} 1".format(stack=";".join(route)))
        else:
            level = -1
            for step in route:
                level += 1
                print("{indent}=> {step}".format(indent="  " * level, step=step))
            print()


if __name__ == "__main__":
    main()
