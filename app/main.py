import argparse
from app.database import init_db
from app.services.news_service import run_pipeline
from app.scheduler import run_forever
def main():
    parser = argparse.ArgumentParser(); parser.add_argument("command", choices=["init-db", "run-once", "worker"], default="run-once", nargs="?"); args = parser.parse_args()
    if args.command == "init-db": init_db(); print("Database initialized")
    elif args.command == "run-once": print(f"Inserted {run_pipeline()} new items")
    else: run_forever()
if __name__ == "__main__": main()
