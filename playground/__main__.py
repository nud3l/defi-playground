import traceback
from playground.core import Blockchain

def main():
    ganache = Blockchain()
    try:
        ganache.read_output()
    except KeyboardInterrupt:
        print("\nShutting down DeFi Playground.")
        ganache.terminate()
    except Exception:
        msg = traceback.format_exc()
        print(msg)
        ganache.terminate()

if __name__ == "__main__":
    main()
