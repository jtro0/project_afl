import argparse
import re
import subprocess
from os.path import join, dirname
from os import walk

#These are words that can't be in the ast dump.
FORBIDDEN_WORDS = ['extern', 'implicit']
FUNC_NAME_PATTERN = r".*FunctionDecl.*\b(\w+)\b(?=\s*')"



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

# This function creates an alternative version of the input file without #ifdefs.
def create_anti_ifdef(input_file_path):
    ifdef_depth = 0
    intermed_file = ''
    output_file_path = dirname(input_file_path) + '/intermediate_file.c'

    source_code = open(input_file_path, 'r')
    count = 0
    for line in source_code:
        if not (line.strip().startswith('#') and 'if' in line):
            intermed_file += line
    
    with open(output_file_path, 'w') as file:
        file.write(intermed_file)

# Fin
def parse_funcs(file_path):
    funcs = []

    ast_funcs = run_command('clang -Xclang -ast-dump -fsyntax-only ' + file_path + ' 2>/dev/null | grep FunctionDecl')
    for line in ast_funcs.splitlines():
        found = False
        # Check if one of the forbidden words is in the line.
        for word in FORBIDDEN_WORDS:
            if word in line:
                found = True
        if not found:
            match = re.search(FUNC_NAME_PATTERN, line)
            if match:
                func_name = match.group(1)
                funcs.append(func_name)
    return funcs

# This function traverses a repo and returns all function names according to a pattern
def search_funcs(directory):
    # This pattern finds a word that is followed up with a space and then a single quote, in
    # a line that starts with FunctionDecl, to find all the function declarations in the ast.
    
    func_path_pairs = []

    for root, dirs, files in walk(directory):
        for file_str in files:
            # Only find functions in .c files.
            if file_str[-2:] == '.c':
                file_path = join(root, file_str)
                intermed_file_path = join(root, 'intermediate_file.c')
                # Excludes testing function from function list.
                if 'test' in file_path:
                    continue
                funcs = parse_funcs(file_path)
                for func in funcs:
                    func_path_pairs.append((func, file_path))
                funcs = parse_funcs(intermed_file_path)
                for func in funcs:
                    func_path_pairs.append((func, file_path))
                         
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

    # Search for functions in the repo in repo_path.
    funcs = search_funcs(args.repo_path)
    for func in funcs:
        func_freq = int(run_command('cd ' + args.repo_path + '; git log --no-patch -L :' + func[0] + ':' + func[1] + ' 2>/dev/null | grep -c commit').strip())
        if args.path:
            weighted_funcs.append((func[0], func_freq, func[1]))
        else:
            weighted_funcs.append((func[0], func_freq))

    # Filter all the functions without a commit history out, remove dups, and sort the relevant funcs by commits.
    weighted_funcs = list(filter(lambda x: x[1] != 0, weighted_funcs))
    weighted_funcs = list(set(weighted_funcs))
    weighted_funcs = sorted(weighted_funcs, key=lambda x: x[1])
    
    for func in weighted_funcs:
        print(func)

if __name__ == "__main__":
    main()