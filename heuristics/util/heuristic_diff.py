import argparse
import re
import subprocess
from os.path import join, abspath
from os import walk, chdir, getcwd
import sys

# Parses the command line arguments.
def parse_args():
    parser = argparse.ArgumentParser(description='This script returns a tuple of all function names in a git repository and the corresponding weights')
    parser.add_argument('repo_path', type=str,
                    help='Path to git repository.')
    return parser.parse_args()

# This function traverses a repo and returns all function names according to a pattern
# that SHOULD represent most of the c type function declarations.
def search_funcs(directory):
    pattern = '^\s*(?:(?:inline|static)\s+){0,2}(?!else|typedef|return)\w+\s+\*?\s*(\w+)\s*\([^0]+\)\s*;?'

    funcs = []

    for root, dirs, files in walk(directory):
        for file_str in files:
            if file_str[-2:] == '.c' or file_str[-2] == '.h':
                file_path = join(root, file_str)
                # Excludes testing function from function list.
                if 'test' in file_path:
                    continue
                file = open(file_path, 'r')
                for line in file:
                    match = re.search(pattern, line)
                    if match:
                        func_name = match.group(1)
                        funcs.append((func_name, file_path))
    # print(funcs)
    return funcs

# Function that starts a subprocess, mostly used to check the git logs.
def run_command(command):    
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output = process.communicate()[0]
    output = output.decode('utf-8')

    return output


def main():
    args = parse_args()
    weighted_funcs = []
    orig_dir = getcwd()
    chdir(join(orig_dir, args.repo_path))
    funcs = search_funcs(".")
    for func in funcs:
        func_freq = run_command('git log --no-patch -L :' + func[0] + ':' + func[1] + ' | grep -c commit')
        # print(func_freq)
        weighted_funcs.append((func[0], int(func_freq)))
    chdir(orig_dir)
    print(weighted_funcs)

if __name__ == "__main__":
    main()