import sys

from client import Client

def main() -> None:
    
    opts = [o for o in sys.argv[1:] if o.startswith("-")]
    
    # show help message
    if "-h" in opts or "--help" in opts:
        Client.__doc__
        raise SystemExit()


if __name__ == "__main__":
    main()