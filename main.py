import os
import sys

import uvicorn

sys.path.append(os.getcwd())

def main():
    uvicorn.run("src.main:app", host="0.0.0.0")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("stopped by user")
        exit(0)