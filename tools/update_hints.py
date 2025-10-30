"""
Helper script to add a new hint type to words.json.
Usage: python update_hints.py --new_hint "example" --default_text "Default example."
"""
import json
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="Add new hint to words.json")
    parser.add_argument('--words_path', default='vocab_learner/data/words.json')
    parser.add_argument('--new_hint', required=True, help="New hint type (e.g., 'example')")
    parser.add_argument('--default_text', default="Placeholder text.", help="Default text for the new hint")
    args = parser.parse_args()

    if not os.path.exists(args.words_path):
        print(f"File not found: {args.words_path}")
        return

    with open(args.words_path, 'r') as f:
        words = json.load(f)

    for word_id, data in words.items():
        if args.new_hint not in data['hints']:
            data['hints'][args.new_hint] = args.default_text

    with open(args.words_path, 'w') as f:
        json.dump(words, f, indent=4)

    print(f"Added '{args.new_hint}' to all words.")

if __name__ == '__main__':
    main()