import argparse
import pickle
import numpy as np
from tabulate import tabulate  # Optional; pip install tabulate if wanted

def main():
    parser = argparse.ArgumentParser(description="Display Q-table as a formatted table.")
    parser.add_argument('--q_table_path', default='q_table.pkl', help="Path to q_table.pkl")
    args = parser.parse_args()

    # Load Q-table
    try:
        with open(args.q_table_path, 'rb') as f:
            q_table = pickle.load(f)
    except FileNotFoundError:
        print(f"Error: {args.q_table_path} not found.")
        return

    # Get all hint types (from first word)
    if not q_table:
        print("Q-table is empty.")
        return
    hint_types = list(next(iter(q_table.values())).keys())

    # Prepare data for table
    table_data = []
    for word_id, hints in sorted(q_table.items()):
        row = [word_id] + [f"{hints.get(hint, 'N/A'):.3f}" for hint in hint_types]
        table_data.append(row)

    # Headers
    headers = ["Word ID"] + hint_types

    # Print as nice table (use tabulate if installed, else simple print)
    try:
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
    except NameError:
        # Fallback to simple aligned print
        print(" | ".join(headers))
        print("-" * (len(" | ".join(headers))))
        for row in table_data:
            print(" | ".join(map(str, row)))

if __name__ == '__main__':
    main()