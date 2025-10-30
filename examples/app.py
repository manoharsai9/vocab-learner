from flask import Flask, request, jsonify
from vocab_learner import VocabularyModel

app = Flask(__name__)
model = VocabularyModel()

@app.route('/get_hint', methods=['POST'])
def get_hint():
    data = request.json
    word_id = int(data['word_id'])
    hint_type = data['hint_type']
    word_data = model.get_word_data(word_id)
    hint_text = model.get_hint_text(word_id, hint_type)
    return jsonify({
        'word': word_data['word'],
        'hint': hint_text,
        'choices': word_data['choices']
    })

@app.route('/update_model', methods=['POST'])
def update_model():
    data = request.json
    word_id = int(data['word_id'])
    hint_type = data['hint_type']
    is_correct = data['is_correct']

    rewards = model.config.get('rewards', {'correct': 1.0, 'incorrect': -0.5})
    reward = rewards['correct'] if is_correct else rewards['incorrect']
    model.update_q_value(word_id, hint_type, reward)

    if not is_correct:
        model.flag_word(word_id)

    return jsonify({'status': 'success'})

@app.route('/get_best_hint_type', methods=['POST'])
def get_best_hint_type():
    data = request.json
    word_id = int(data['word_id'])
    best_hint_type = model.get_best_hint_for_word(word_id)
    return jsonify({'best_hint_type': best_hint_type})

@app.route('/get_overall_best_hint', methods=['GET'])
def get_overall_best_hint():
    best_hint_type = model.get_overall_best_hint()
    return jsonify({'overall_best_hint_type': best_hint_type})

@app.route('/get_flagged_words', methods=['GET'])
def get_flagged_words():
    flagged_words = model.get_flagged_words()
    return jsonify({'flagged_words': flagged_words})

@app.route('/add_new_word', methods=['POST'])
def add_new_word():
    data = request.json
    word_id = int(data['word_id'])
    word_data = data['word_data']
    model.add_new_word(word_id, word_data)
    return jsonify({'status': 'success', 'message': 'New word added successfully'})

@app.route('/get_all_words', methods=['GET'])
def get_all_words():
    word_ids = model.get_word_ids()
    return jsonify({'word_ids': word_ids})

@app.route('/get_ranked_hint_type', methods=['POST'])
def get_ranked_hint_type():
    data = request.json
    try:
        word_id = int(data.get('word_id'))
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid or missing word_id'}), 400
    try:
        rank = int(data.get('rank', 0))
    except (TypeError, ValueError):
        rank = 0
    word_qs = model.q_table.get(word_id, {})
    is_new_word = all(q == 0.1 for q in word_qs.values()) if word_qs else True
    if is_new_word:
        best_hint = model.get_overall_best_hint()
        return jsonify({'hint_type': best_hint})
    sorted_hint_types = model.get_sorted_hints(word_id)
    if 0 <= rank < len(sorted_hint_types):
        return jsonify({'hint_type': sorted_hint_types[rank]})
    return jsonify({'hint_type': sorted_hint_types[0]})

if __name__ == '__main__':
    app.run(debug=True)