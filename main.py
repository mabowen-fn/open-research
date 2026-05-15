# main.py
import subprocess
import sys


def main():
    print("==============================================")
    print("  OpenClaw Automated Survey Paper Generator   ")
    print("==============================================\n")

    # Step 1: Fetch
    print("[1/2] Launching Paper Fetcher...")
    fetch_res = subprocess.run([sys.executable, "src/paper_fetcher.py"])
    if fetch_res.returncode != 0:
        print("Error encountered while fetching papers.")
        return

    # Step 2: Synthesis & Polish
    print("\n[2/2] Launching Synthesis & Polishing Pipeline...")
    pipeline_res = subprocess.run([sys.executable, "src/pipeline.py"])
    if pipeline_res.returncode != 0:
        print("Error encountered during pipeline generation.")
        return


if __name__ == "__main__":
    main()
