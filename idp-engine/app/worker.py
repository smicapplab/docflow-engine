import os
import time

def main():
    redis_host = os.getenv("REDIS_HOST", "localhost")

    print("===================================")
    print(" Docflow Engine - Worker Started ")
    print("===================================")
    print(f"Connecting to Redis at: {redis_host}")
    print("Worker running... (heartbeat every 10s)")
    print("-----------------------------------")

    try:
        while True:
            print("Worker heartbeat...")
            time.sleep(10)
    except KeyboardInterrupt:
        print("Worker shutting down gracefully...")
        return


if __name__ == "__main__":
    main()
