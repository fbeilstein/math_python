import os
import sys
import shutil
import subprocess
import argparse
import json

def find_problem_dir(repo_root, problem_name):
    for root, dirs, files in os.walk(repo_root):
        if problem_name in dirs:
            return os.path.join(root, problem_name)
    return None

def grade_student(problem_dir, student_file):
    # Backup original
    orig_tasks = os.path.join(problem_dir, "implementation_tasks.py")
    backup_tasks = orig_tasks + ".bak"
    if os.path.exists(orig_tasks):
        shutil.copy2(orig_tasks, backup_tasks)
    
    try:
        shutil.copy2(student_file, orig_tasks)
        
        # We need a custom runner to get machine-readable output
        runner_code = """import os
import unittest
import json
import sys

loader = unittest.TestLoader()
suite = loader.discover('tests')
runner = unittest.TextTestRunner(stream=open(os.devnull, 'w'), verbosity=0)
result = runner.run(suite)

output = {
    'testsRun': result.testsRun,
    'failures': len(result.failures),
    'errors': len(result.errors),
    'passed': result.testsRun - len(result.failures) - len(result.errors)
}
print(json.dumps(output))
"""
        runner_path = os.path.join(problem_dir, "_temp_runner.py")
        with open(runner_path, 'w') as f:
            f.write(runner_code)
        
        proc = subprocess.run([sys.executable, "_temp_runner.py"], cwd=problem_dir, capture_output=True, text=True, timeout=10)
        os.remove(runner_path)
        
        try:
            # Parse the last line as JSON (in case students leave print statements)
            lines = [line for line in proc.stdout.strip().split('\\n') if line]
            res = json.loads(lines[-1])
            return res
        except (json.JSONDecodeError, IndexError):
            return {"error": "CRASH", "details": proc.stderr or proc.stdout}

    except subprocess.TimeoutExpired:
        return {"error": "TIMEOUT", "details": "Execution exceeded 10 seconds"}
    finally:
        if os.path.exists(backup_tasks):
            shutil.move(backup_tasks, orig_tasks)
        elif os.path.exists(orig_tasks):
            os.remove(orig_tasks)

def main():
    parser = argparse.ArgumentParser(description="Batch grade student submissions")
    parser.add_argument("problem_name", help="Name of the problem folder (e.g. optical_problem)")
    parser.add_argument("submissions_dir", help="Directory containing student folders")
    args = parser.parse_args()

    repo_root = os.path.abspath(os.path.dirname(__file__))
    problem_dir = find_problem_dir(repo_root, args.problem_name)
    
    if not problem_dir:
        print(f"Error: Could not find problem '{args.problem_name}'")
        sys.exit(1)
        
    tests_dir = os.path.join(problem_dir, 'tests')
    if not os.path.exists(tests_dir):
        print(f"Error: No tests/ directory found in {problem_dir}")
        sys.exit(1)

    print(f"\\nGRADING: {args.problem_name}")
    print("─" * 60)
    print(f"{'Student':<20} | {'Passed':<6} | {'Total':<6} | {'Status'}")
    print("─" * 60)
    
    for student_dir in sorted(os.listdir(args.submissions_dir)):
        s_path = os.path.join(args.submissions_dir, student_dir)
        if not os.path.isdir(s_path):
            continue
            
        task_file = os.path.join(s_path, "implementation_tasks.py")
        if not os.path.exists(task_file):
            print(f"{student_dir:<20} | {'-':<6} | {'-':<6} | NO FILE")
            continue
            
        res = grade_student(problem_dir, task_file)
        
        if "error" in res:
            print(f"{student_dir:<20} | {'-':<6} | {'-':<6} | {res['error']}")
        else:
            passed = res['passed']
            total = res['testsRun']
            status = "OK" if passed == total else "FAIL"
            print(f"{student_dir:<20} | {passed:<6} | {total:<6} | {status}")
            
    print("─" * 60)

if __name__ == '__main__':
    main()
