import argparse
import re
import subprocess
from os.path import join
from os import walk, chdir, getcwd

# Parses the command line arguments.
def parse_args():
    parser = argparse.ArgumentParser(description='This script returns a tuple of all function names in a git repository and the corresponding weights')
    parser.add_argument('repo_path', type=str,
                    help='Absolute path to git repository.')
    parser.add_argument('output_path', type=bool,
                    help='Enter either 1 if you want the file path in the output, otherwise 0.')
    return parser.parse_args()

# This function traverses a repo and returns all function names according to a pattern
def search_funcs(directory):
    # This pattern finds a word that is followed up with a space and then a single quote, in
    # a line that starts with FunctionDecl, to find all the function declarations in the ast.
    pattern_func_name = r".*FunctionDecl.*\b(\w+)\b(?=\s*')"
    #These are words that can't be in the ast dump.
    forbidden_words = ['extern', 'implicit', 'invalid', '__']
    
    funcs = []

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
                    # Check if one of the forbidden words is in the file.
                    for word in forbidden_words:
                        if word in line:
                            found = True
                    if not found:
                        match = re.search(pattern_func_name, line)
                        if match:
                            func_name = match.group(1)
                            funcs.append((func_name, file_path))
                        
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
    
    # Search for functions in the repo in repo_path.
    funcs = search_funcs(args.repo_path)
    for func in funcs:
        func_freq = int(run_command('cd ' + args.repo_path + '; git log --no-patch -L :' + func[0] + ':' + func[1] + ' 2>/dev/null | grep -c commit').strip())
        if args.file_path:
            weighted_funcs.append((func[0], func_freq, func[1]))
        else:
            weighted_funcs.append((func[0], func_freq))

    # Filter all the functions without a commit history out, and sort the relevant funcs by commits.
    weighted_funcs = list(filter(lambda x: x[1] != 0, weighted_funcs))
    weighted_funcs = sorted(weighted_funcs, key=lambda x: x[1])
    
    for func in weighted_funcs:
        print(func)

if __name__ == "__main__":
    main()