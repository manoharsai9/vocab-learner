# Vocab Learner

A modular Python package for Q-learning based adaptive vocabulary hints. Scalable for new hint types, including multimodal (videos, PDFs, images).

## Installation

```bash
pip install git+https://github.com/manoharsai9/vocab-learner.git
```

For API:
```bash
pip install 'vocab_learner[api]'
```

## Quick Start

```python
from vocab_learner import VocabularyModel

model = VocabularyModel()
best_hint = model.get_best_hint_for_word(1)
print(best_hint)
```

## Features

- Q-learning with epsilon-greedy exploration.
- Configurable params (alpha, gamma, rewards, exploration_rate).
- Scalable hints via `config.json` (no code changes).
- Multimodal support (URLs/paths for media).
- Flask API (`examples/app.py`).
- Bulk hint updater (`tools/update_hints.py`).
- Q-table visualizer (`tools/display_q_table.py`).
- Unit tests (`tests/test_model.py`).

## Adding Hint Types

1. Update `config.json`:
   ```json
   "hint_types": ["context", "dialogue", "story", "video"]
   ```

2. Bulk update words:
   ```bash
   python tools/update_hints.py --new_hint video --default_text "https://example.com/video/placeholder.mp4"
   ```

## Run API

```bash
python examples/app.py --port 5001
```

Test:
```bash
curl http://127.0.0.1:5001/get_overall_best_hint
```

## Core Functions/Endpoints

### get_best_hint_type (Best Hint)

POST `/get_best_hint_type` with `{"word_id": 1}` → `{"best_hint_type": "context"}`

### get_sorted_hints (Ranked Hints)

POST `/get_ranked_hint_type` with `{"word_id": 1, "rank": 0}` → `{"hint_type": "context"}`

### update_model (Learn Feedback)

POST `/update_model` with `{"word_id": 1, "hint_type": "context", "is_correct": true}` → `{"status": "success"}`

## Integration

```python
model = VocabularyModel()
hint_type = model.get_best_hint_for_word(1)
hint = model.get_hint_text(1, hint_type)

# Render (e.g., if 'video', embed hint URL)

model.update_q_value(1, hint_type, reward=1 if correct else -0.5)
```

## Run Tests

```bash
pip install -e .
python -m unittest discover -s tests
```

## Project Structure

```
vocab-learner/
├── LICENSE
├── README.md
├── setup.py
├── vocab_learner/
│   ├── __init__.py
│   ├── model.py
│   └── data/
│       ├── config.json
│       └── words.json
├── examples/app.py
├── tools/
│   ├── update_hints.py
│   └── display_q_table.py
└── tests/test_model.py
```

## License

MIT – free to use/modify.

*Advancing adaptive learning through AI. Part of Scafwording ecosystem.*