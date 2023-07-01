import argparse
import re
import subprocess
from os.path import join, abspath, dirname
from os import walk
import datetime
from datetime import datetime, getcwd
import sys

#These are words that can't be in the ast dump.
FORBIDDEN_WORDS = ['extern', 'implicit']
FUNC_NAME_PATTERN = r".*FunctionDecl.*\b(\w+)\b(?=\s*')"

# Parses the command line arguments.
def parse_args():
    parser = argparse.ArgumentParser(description='This script returns a tuple of all function names in a git repository and the corresponding weights in accordance to the chosen heuristic')
    parser.add_argument('repo_path', type=str,
                    help='Absolute path to git repository.')
    parser.add_argument('-H', '--heuristic', type=int, required=True, help="Give the heuristic number. 1: number of commits, 2: Time since last commit.")
    parser.add_argument('-p', '--path', action='store_true', help='''If flag is given the the program returns a pair of the function name, the frequency, 
                        and the file it got the function from. Otherwise only the first two -- Only applicable for heurstic 1''')
    parser.add_argument('-r', '--ranked', action='store_true', help='''If you want the rank of the functions instead of the weight give this flag''')
    return parser.parse_args()

# This function creates an alternative version of the input file without #ifdefs.
def create_anti_ifdef(input_file_path):
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

# Expects a line with a date in the format git log gives, outputs a python datetime object encoded to an integer.
def parse_date_line(line):
    date_string = " ".join(line.split()[1:])
    date_format = "%a %b %d %H:%M:%S %Y %z"
    date = datetime.strptime(date_string, date_format)
    encoded_date = int(date.timestamp())
    return encoded_date

# Assumes sorted inputs
def heuristic_to_rank(weighted_funcs, output_path):
    counter = 0
    ranked_funcs = []
    for func in weighted_funcs:
        counter += 1
        if output_path:
            ranked_funcs.append((func[0], counter, func[2]))
        else:
            ranked_funcs.append((func[0], counter))

    return ranked_funcs

# Uses the amount of commits per function.
def heuristic_0(repo_path, output_paths, funcs):
    weighted_funcs = []
    orig_dir = getcwd()
    chdir(join(orig_dir, args.repo_path))

    # Search for functions in the repo in repo_path.
    funcs = search_funcs(".")
    for func in funcs:
        func_freq = int(run_command('git log --no-patch -L :' + func[0] + ':' + func[1] + ' 2>/dev/null | grep -c commit').strip())
        if output_paths:
            weighted_funcs.append((func[0], func_freq, func[1]))
        else:
            # print(func_freq)
            weighted_funcs.append((func[0], func_freq))
    return weighted_funcs

# Uses the date of the most recent commit.
def heuristic_1(repo_path, output_paths, funcs):
    weighted_funcs = []
    for func in funcs:
        date_line = run_command('cd ' + repo_path + '; git log --no-patch -L :' + func[0] + ':' + func[1] + ' 2>/dev/null | grep -m 1 Date:').strip()
        if date_line != '':
            date = parse_date_line(date_line)
            if output_paths:
                weighted_funcs.append((func[0], date, func[1]))
            else:
                weighted_funcs.append((func[0], date))
    return weighted_funcs

def main():
    args = parse_args()

    # Search for functions in the repo in repo_path.
    funcs = search_funcs(args.repo_path)
    if args.heuristic == 0:
        output_funcs = heuristic_0(args.repo_path, args.path, funcs)
    elif args.heuristic == 1:
        output_funcs = heuristic_1(args.repo_path, args.path, funcs)
    

    # Filter all the functions without a commit history out, remove dups, and sort the relevant funcs by commits.
    output_funcs = list(filter(lambda x: x[1] != 0, output_funcs))
    output_funcs = list(set(output_funcs))
    output_funcs = sorted(output_funcs, key=lambda x: x[1])
    # Ranks the function on the weight gained from the heuristic.
    if args.ranked:
        output_funcs = heuristic_to_rank(output_funcs, args.path)

    print(output_funcs)

if __name__ == "__main__":
    main()