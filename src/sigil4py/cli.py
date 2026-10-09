"""CRONE: minimal public CLI. Does not launch external runtimes."""
import argparse
import json

def main(argv=None):
    parser = argparse.ArgumentParser(prog="sigil4py-check")
    parser.add_argument("--status", action="store_true", help="show typed kernel status")
    args = parser.parse_args(argv)
    if args.status:
        print(json.dumps({"schema":"SIGIL_CRONE_CLI_V1","core":"SOURCE_ONLY",
                          "sympy":"OPTIONAL","c_extension":"NOT_VERIFIED",
                          "safe_to_ship":False,"verdict":"HOLD_QUNO"},sort_keys=True))
    else:
        parser.print_help()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
