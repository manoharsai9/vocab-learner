from importlib.resources import files
import numpy as np
import pickle
from typing import Dict, List, Optional
import json
import random
import os

class VocabularyModel:
    """
    Q-learning based model for selecting vocabulary hints.
    Fully configurable via config.json — no hardcoding.
    """
    def __init__(
        self,
        config_path: Optional[str] = None,
        words_path: Optional[str] = None,
        q_table_path: Optional[str] = None,
        exploration_rate: Optional[float] = None,
    ):
        if config_path is None:
            config_path = str(files('vocab_learner.data') / 'config.json')
        self.config = self.load_config(config_path)

        # Override exploration rate if provided
        self.exploration_rate = exploration_rate if exploration_rate is not None else self.config.get('exploration_rate', 0.2)

        # Use config paths if not provided
        if words_path is None:
            words_path = self.config.get('words_file') or str(files('vocab_learner.data') / 'words.json')
        self.words = self.load_words(words_path)

        if q_table_path is None:
            q_table_path = self.config.get('q_table_file', 'q_table.pkl')
        self.q_table = self.load_q_table(q_table_path)

        self.flagged_words = set()

    def load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise ValueError(f"Config file not found: {config_path}")

    def load_words(self, words_path: str) -> Dict[int, Dict]:
        """Load words data from JSON file."""
        try:
            with open(words_path, 'r') as f:
                words = json.load(f)
            return {int(k): v for k, v in words.items()}
        except FileNotFoundError:
            raise ValueError(f"Words file not found: {words_path}")

    def load_q_table(self, q_table_path: str) -> Dict[int, Dict[str, float]]:
        """Load or initialize Q-table using initial_q_value from config."""
        try:
            with open(q_table_path, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            initial_q = self.config.get('initial_q_value', 0.1)
            q_table = {
                word_id: {
                    hint: initial_q for hint in self.config['hint_types']
                }
                for word_id in self.words.keys()
            }
            self.save_q_table(q_table_path, q_table)
            return q_table

    def save_q_table(self, q_table_path: Optional[str] = None, q_table: Optional[Dict] = None):
        """Save Q-table to file."""
        if q_table_path is None:
            q_table_path = self.config['q_table_file']
        if q_table is None:
            q_table = self.q_table
        with open(q_table_path, 'wb') as f:
            pickle.dump(q_table, f)

    def get_sorted_hints(self, word_id: int) -> List[str]:
        """Get hint types sorted by Q-value descending."""
        if word_id not in self.q_table:
            initial_q = self.config.get('initial_q_value', 0.1)
            self.q_table[word_id] = {hint: initial_q for hint in self.config['hint_types']}
            self.save_q_table()
        q_values = self.q_table[word_id]
        return sorted(q_values, key=q_values.get, reverse=True)

    def get_hint_text(self, word_id: int, hint_type: str) -> str:
        """Get hint text (or URL/path for multimodal hints) for a word and type."""
        if hint_type not in self.config['hint_types']:
            raise ValueError(f"Invalid hint type: {hint_type}")
        return self.words[word_id]['hints'][hint_type]

    def update_q_value(self, word_id: int, hint_type: str, reward: float):
        """Update Q-value using Q-learning formula."""
        if word_id not in self.q_table:
            initial_q = self.config.get('initial_q_value', 0.1)
            self.q_table[word_id] = {hint: initial_q for hint in self.config['hint_types']}

        current_q = self.q_table[word_id][hint_type]
        next_best_q = max(self.q_table[word_id].values())
        updated_q = current_q + self.config['alpha'] * (reward + self.config['gamma'] * next_best_q - current_q)
        self.q_table[word_id][hint_type] = updated_q
        self.save_q_table()

    def flag_word(self, word_id: int):
        """Flag a word as needing review."""
        self.flagged_words.add(word_id)

    def get_word_data(self, word_id: int) -> Dict:
        """Get full data for a word."""
        return self.words[word_id]

    def get_overall_best_hint(self) -> str:
        """Get the globally best hint type based on cumulative Q-values."""
        cumulative = {hint: 0.0 for hint in self.config['hint_types']}
        for word_q in self.q_table.values():
            for hint, q in word_q.items():
                cumulative[hint] += q
        return max(cumulative, key=cumulative.get)

    def get_best_hint_for_word(self, word_id: int) -> str:
        """Get best hint for a word with epsilon-greedy exploration."""
        if random.random() < self.exploration_rate:
            return random.choice(self.config['hint_types'])
        if word_id not in self.q_table:
            initial_q = self.config.get('initial_q_value', 0.1)
            self.q_table[word_id] = {hint: initial_q for hint in self.config['hint_types']}
            self.save_q_table()
        return max(self.q_table[word_id], key=self.q_table[word_id].get)

    def get_flagged_words(self) -> List[int]:
        """Get list of flagged words."""
        return list(self.flagged_words)

    def add_new_word(self, word_id: int, word_data: Dict):
        """Add a new word and initialize Q-table for it."""
        if word_id in self.words:
            raise ValueError(f"Word ID {word_id} already exists.")
        missing_hints = set(self.config['hint_types']) - set(word_data.get('hints', {}).keys())
        if missing_hints:
            raise ValueError(f"Missing hints for types: {missing_hints}")
        self.words[word_id] = word_data
        initial_q = self.config.get('initial_q_value', 0.1)
        self.q_table[word_id] = {hint: initial_q for hint in self.config['hint_types']}
        self.save_words()
        self.save_q_table()

    def save_words(self, words_path: Optional[str] = None):
        """Save words to file."""
        if words_path is None:
            words_path = self.config['words_file']
        with open(words_path, 'w') as f:
            json.dump({str(k): v for k, v in self.words.items()}, f, indent=4)

    def get_word_ids(self) -> List[int]:
        """Get list of all word IDs."""
        return list(self.words.keys())