from os import system
from os.path import exists
import argparse
import re
from collections import Counter

# Parses the command line arguments.
def parse_args():
    parser = argparse.ArgumentParser(description='This script returns a tuple of all function names in a git repository and the corresponding weights')
    parser.add_argument('repo_path', type=str,
                    help='Path to git repository.')
    return parser.parse_args()

# This function uses the get_commits.sh script to create a file with lines of function names in github's diff format.
def create_diff_file(repo_path):
    if not exists("./diffs.txt"):
        print("Creating diff file for repo at: " + repo_path)
        command = "./get_commits.sh -p " + repo_path + " > diffs.txt"
        system(command)
        print("Done and saved as diffs.txt")
    else:
        print('Diff file already exists')
    diff_file = open('diffs.txt', 'r')
    return diff_file

# This function uses regexes to parse a diff file and return,
# a dictionary holding the frequencies in which functions occur
# in the commit history. Only supports c function declaration for 
# now.
def calc_func_freqs(diff_file):
    funcs = []
    for line in diff_file:
        match = re.search(r'\b(\w+)\s+\(', line)
        if match:
            func_name = match.group(1)
            funcs.append(func_name)
    freqs = dict(Counter(funcs))
    freqs_sorted = dict(sorted(freqs.items(), key=lambda item: item[1], reverse=True))
    return freqs_sorted


def main():
    args = parse_args()
    diff_file = create_diff_file(args.repo_path)
    func_freqs = calc_func_freqs(diff_file)
    print(func_freqs)
    
    
    

if __name__ == "__main__":
    main()