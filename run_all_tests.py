import subprocess
import sys
from pathlib import Path


TEST_FILES = [
    "3dotsmenuclick.py",
    "addquicklinks.py",
    "addsearch.py",
    "applaunch.py",
    "cashbackopenclose.py",
    "customadd.py",
    "customcancel.py",
    "help_feedback.py",
    "nativebannerredirection.py",
    "news.py",
    "ntpwidgetclick.py",
    "ntpwidgetrefresh.py",
    "playwallopenclose.py",
    "removefromrecents.py",
    "rewardshome.py",
    "rewardsopen.py",
    "scrolltotopclick.py",
    "searchbarclick.py",
    "themechange.py",
]


def run_test(script_path):
    print(f"\n========== RUNNING: {script_path.name} ==========", flush=True)
    result = subprocess.run([sys.executable, str(script_path)], cwd=script_path.parent)

    if result.returncode == 0:
        print(f"========== PASSED: {script_path.name} ==========", flush=True)
        return True

    print(f"========== FAILED: {script_path.name} ==========", flush=True)
    return False


def main():
    base_dir = Path(__file__).resolve().parent
    passed = []
    failed = []

    for file_name in TEST_FILES:
        script_path = base_dir / file_name

        if not script_path.exists():
            print(f"\nSKIPPED: {file_name} was not found", flush=True)
            failed.append(file_name)
            continue

        if run_test(script_path):
            passed.append(file_name)
        else:
            failed.append(file_name)

    print("\n========== FINAL SUMMARY ==========", flush=True)
    print(f"Passed: {len(passed)}", flush=True)
    print(f"Failed: {len(failed)}", flush=True)

    if failed:
        print("\nFailed files:", flush=True)
        for file_name in failed:
            print(f"- {file_name}", flush=True)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
