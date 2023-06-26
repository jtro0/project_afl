import argparse
import re
import subprocess
from os.path import join, abspath
from os import walk, chdir, getcwd
import sys

#These are words that can't be in the ast dump.
FORBIDDEN_WORDS = ['extern', 'implicit']


# Parses the command line arguments.
def parse_args():
    parser = argparse.ArgumentParser(description='This script returns a tuple of all function names in a git repository and the corresponding weights')
    parser.add_argument('repo_path', type=str,
                    help='Absolute path to git repository.')
    parser.add_argument('-p', '--path', action='store_true', help='''If flag is given the the program returns a pair of the function name, the frequency, 
                        and the file it got the function from. Otherwise only the first two''')
    return parser.parse_args()

def parse_file(input_file):
    lines = input_file.readlines()
    filtered_lines = [line for line in lines if 'include' not in line]

    # Write the filtered lines back to the file
    with open('intermediate_file', 'w') as file:
        file.writelines(filtered_lines)

# This function traverses a repo and returns all function names according to a pattern
def search_funcs(directory):
    # This pattern finds a word that is followed up with a space and then a single quote, in
    # a line that starts with FunctionDecl, to find all the function declarations in the ast.
    pattern_func_name = r".*FunctionDecl.*\b(\w+)\b(?=\s*')"
    
    func_path_pairs = []

    for root, dirs, files in walk(directory):
        for file_str in files:
            # Only find functions in .c files.
            if file_str[-2:] == '.c':
                file_path = join(root, file_str)
                # Excludes testing function from function list.
                if 'test' in file_path:
                    continue
                ast_funcs = run_command('clang -Xclang -ast-dump -fsyntax-only ' + file_path + ' 2>/dev/null | grep FunctionDecl')
                for line in ast_funcs.splitlines():
                    found = False
                    # Check if one of the forbidden words is in the line.
                    for word in FORBIDDEN_WORDS:
                        if word in line:
                            found = True
                    if not found:
                        match = re.search(pattern_func_name, line)
                        if match:
                            func_name = match.group(1)
                            func_path_pairs.append((func_name, file_path))
                        
    return list(set(func_path_pairs))

# Function that starts a subprocess.
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

    # Search for functions in the repo in repo_path.
    funcs = search_funcs(".")
    for func in funcs:
        func_freq = int(run_command('cd ' + args.repo_path + '; git log --no-patch -L :' + func[0] + ':' + func[1] + ' 2>/dev/null | grep -c commit').strip())
        if args.path:
            weighted_funcs.append((func[0], func_freq, func[1]))
        else:
            # print(func_freq)
            weighted_funcs.append((func[0], func_freq))
    chdir(orig_dir)
    # Filter all the functions without a commit history out, remove dups, and sort the relevant funcs by commits.
    weighted_funcs = list(filter(lambda x: x[1] != 0, weighted_funcs))
    weighted_funcs = list(set(weighted_funcs))
    weighted_funcs = sorted(weighted_funcs, key=lambda x: x[1])
    
    # for func in weighted_funcs:
    #     print(func)
    print(weighted_funcs)

if __name__ == "__main__":
    main()