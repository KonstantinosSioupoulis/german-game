from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

def load_translations(filename="translations.txt"):
    """Loads translations from a file."""
    translations = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                translations.append({"german": parts[0], "greek": parts[1]})
    return translations

translations = load_translations()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_word')
def get_word():
    if not translations:
        return jsonify({"error": "No translations found."})

    mode = request.args.get('mode', 'random')
    if mode == 'serial':
        index = int(request.args.get('index', 0))
        if 0 <= index < len(translations):
            return jsonify(translations[index])
        else:
            return jsonify(translations[0]) # Loop back to the start
    else: # random mode
        return jsonify(random.choice(translations))

@app.route('/get_word_count', methods=['GET'])
def get_word_count():
    return jsonify({'count': len(translations)})

@app.route('/find_word', methods=['GET'])
def find_word():
    search_term = request.args.get('term', '').lower()
    if not search_term:
        return jsonify({'index': -1})

    for i, translation in enumerate(translations):
        if search_term in translation['german'].lower():
            return jsonify({'index': i})

    return jsonify({'index': -1})


if __name__ == '__main__':
    app.run(debug=True)
