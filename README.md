# Vocab Learner

A modular Python package for a **Q-learning based adaptive vocabulary hint system**.  
Designed to be **easily integrated** into any app (like https://scafwording.app) and **scalable** to new hint types, including multimodal ones like videos, PDFs, images, audio, or interactive elements.

---

## Installation

```bash
pip install git+https://github.com/manoharsai9/vocab-learner.git
```

For the API example:
```bash
pip install 'vocab_learner[api]'
```

---

## Quick Start

```python
from vocab_learner import VocabularyModel

model = VocabularyModel()
best_hint = model.get_best_hint_for_word(1)
print(best_hint)
```

---

## Features

- Q-learning with epsilon-greedy exploration for adaptive hint selection
- Auto-initializes Q-table for new words and hint types
- Scalable: add new hint types (e.g., text, video, PDF, image) via `config.json` — no code changes required
- Supports multimodal hints: store URLs or paths for videos, PDFs, images, etc., and the model learns their effectiveness
- Includes Flask API example (`examples/app.py`) for easy backend integration
- Helper script to bulk-add hints (`tools/update_hints.py`)
- Unit tests for reliability (`tests/test_model.py`)
- Q-table visualization tool (`tools/display_q_table.py`) for inspecting learned values.

---

## Adding New Hint Types (Including Multimodal)

The system is fully scalable to any hint type, such as `video`, `pdf`, `image`, or even `audio`. No Python code modifications needed — just update JSON files.

1. Edit `vocab_learner/data/config.json` → add to `"hint_types"`:
   ```json
   "hint_types": ["context", "dialogue", "story", "video", "pdf", "image"]
   ```

2. Update `words.json` → add the new keys under each word's `"hints"` (e.g., URLs or paths):
   ```json
   "hints": {
     "context": "Context: The storm suddenly abated.",
     "video": "https://youtube.com/watch?v=abate_example",
     "pdf": "https://example.com/abate_lesson.pdf",
     "image": "https://example.com/images/abate.png"
   }
   ```

3. Use the helper script for bulk updates:
   ```bash
   python tools/update_hints.py --new_hint video --default_text "https://example.com/video/placeholder.mp4"
   ```

The Q-table will automatically initialize and learn from rewards for these new types. Your app can render them accordingly (e.g., embed videos, display PDFs).

---

## Integration

Use in your app (e.g., Scafwording, flashcards, games, or edtech tools):
```python
model = VocabularyModel(config_path='my_config.json')
hint_type = model.get_best_hint_for_word(word_id=1)
hint_text = model.get_hint_text(word_id=1, hint_type=hint_type)

# Example rendering logic
if hint_type == 'video':
    # Embed video from hint_text (URL)
    pass
elif hint_type == 'pdf':
    # Display PDF from hint_text
    pass
else:
    # Show text
    print(hint_text)

# Update after user interaction
reward = 1 if user_correct else -0.5
model.update_q_value(word_id=1, hint_type=hint_type, reward=reward)
```

---

## Project Structure

```
vocab-learner/
├── LICENSE
├── MANIFEST.in
├── README.md
├── setup.py
├── .gitignore
├── vocab_learner/
│   ├── __init__.py
│   ├── model.py
│   └── data/
│       ├── config.json
│       └── words.json
├── examples/
│   └── app.py
├── tools/
│   └── update_hints.py
└── tests/
    └── test_model.py
```

---

## License

[MIT License](LICENSE) – free to use, modify, and integrate.

---

*Part of the Scafwording ecosystem – advancing adaptive, multimodal learning through AI. Open-sourced to enable broader innovation in edtech.*