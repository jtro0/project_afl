import argparse
import re
import subprocess
from os.path import join
from os import walk

# Parses the command line arguments.
def parse_args():
    parser = argparse.ArgumentParser(description='This script returns a tuple of all function names in a git repository and the corresponding weights')
    parser.add_argument('repo_path', type=str,
                    help='Path to git repository.')
    return parser.parse_args()

# This function traverses a repo and returns all function names according to a pattern
# that SHOULD represent most of the c type function declarations.
def search_funcs(directory):
    # This pattern finds a word that is followed up with a space and then a single quote.
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
                    for word in forbidden_words:
                        if word in line:
                            found = True
                        if not found:
                            match = re.search(pattern_func_name, line)
                            if match:
                                func_name = match.group(1)
                                print(func_name)
                                funcs.append(func_name)
                        
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
    
    funcs = search_funcs(args.repo_path)
    print(funcs)
    # for func in funcs:
    #     func_freq = run_command('cd ' + args.repo_path + '; git log --no-patch -L :' + func[0] + ':' + func[1] + ' | grep -c commit')
    #     weighted_funcs.append((func[0], func_freq))

    # print(weighted_funcs)

if __name__ == "__main__":
    main()