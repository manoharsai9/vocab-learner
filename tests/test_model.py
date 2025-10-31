# test_model_local.py
from vocab_learner import VocabularyModel
import os
import json

# Step 1: Reset everything (clean slate)

# Delete q_table.pkl if exists
if os.path.exists("q_table.pkl"):
    os.remove("q_table.pkl")
    print("Removed old q_table.pkl for fresh start.")

# Reset config and words
config_path = 'vocab_learner/data/config.json'
words_path = 'vocab_learner/data/words.json'

# Reset config: Remove 'video'
with open(config_path, 'r') as f:
    config = json.load(f)

if 'video' in config['hint_types']:
    config['hint_types'].remove('video')
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)
    print("Removed 'video' from config.json")

# Reset words: Remove 'video' and test word 100
with open(words_path, 'r') as f:
    words = json.load(f)

for word_id in list(words.keys()):
    if 'hints' in words[word_id] and 'video' in words[word_id]['hints']:
        del words[word_id]['hints']['video']
    if word_id == '100':
        del words[word_id]
        print("Removed test word ID 100 from words.json")

with open(words_path, 'w') as f:
    json.dump(words, f, indent=4)

print("Reset complete. Starting fresh test...")

# Load model (fresh Q-table)
model = VocabularyModel()

# Remove test word from q_table if exists
if 100 in model.q_table:
    del model.q_table[100]
    model.save_q_table()
    print("Removed test word ID 100 from q_table")

# Test: Get best hint for word 1
best_hint_type = model.get_best_hint_for_word(1)
print(f"Best hint type for word 1: {best_hint_type}")

hint_text = model.get_hint_text(1, best_hint_type)
print(f"Hint text: {hint_text}")

# Update Q-value
model.update_q_value(1, best_hint_type, reward=1)
print("Q-value updated.")

# Check overall best
overall_best = model.get_overall_best_hint()
print(f"Overall best hint: {overall_best}")

# Add new word (ID 100)
new_word = {
    "word": "test_word",
    "hints": {hint: f"Test {hint}." for hint in model.config['hint_types']},
    "summary": "Test summary",
    "choices": ["A", "B"],
    "correct_index": 0
}
model.add_new_word(100, new_word)
print("New word added (ID 100).")

# Add 'video' hint type
with open(config_path, 'r+') as f:
    config = json.load(f)
    if 'video' not in config['hint_types']:
        config['hint_types'].append('video')
        f.seek(0)
        json.dump(config, f, indent=4)
        f.truncate()
        print("Added 'video' to config.")

# Add video to all words
os.system("python tools/update_hints.py --new_hint video --default_text 'https://example.com/video/test.mp4'")

# Reload model
model = VocabularyModel()

# Test video hint
video_hint = model.get_hint_text(1, 'video')
print(f"Video hint for word 1: {video_hint}")

# Verify new word
print(f"New word summary: {model.get_word_data(100)['summary']}")

# Check q_table.pkl
print(f"q_table.pkl created? {os.path.exists('q_table.pkl')}")

# Display Q-table
print("\nDisplaying Q-table...")
os.system("python tools/display_q_table.py --q_table_path q_table.pkl")