from git import Repo
from git.exc import GitError
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='This script returns a tuple of all function names in a git repository and the corresponding weights')
    parser.add_argument('repo_path', type=str,
                    help='Path to git repository.')
    return parser.parse_args()

def itterate_changes(repo):
    for commit in repo.iter_commits():
        # The M flag in the iter_change_type method indicates that only modofications are itterated.
        diff = commit.diff()

        for change in diff.iter_change_type("M"):
            print(change)
            


def main():
    args = parse_args()
    repo = Repo(args.repo_path)
    itterate_changes(repo)
    

if __name__ == "__main__":
    main()