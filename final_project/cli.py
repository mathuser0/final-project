
"""Console script for final_project."""
import argparse
from luigi import build
from final_project.tasks.model_tasks import Analyze,Classify

import sys

def main():
    """Console script for final_project."""
    build([Analyze(), Classify(),
           # GetIndices(),
           ],local_scheduler = True )

    parser = argparse.ArgumentParser()
    parser.add_argument('_', nargs='*')
    args = parser.parse_args()

    print("Arguments: " + str(args._))
    print("Replace this message by putting your code into "
          "final_project.cli.main")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover