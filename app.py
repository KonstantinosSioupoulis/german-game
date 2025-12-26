from flask import Flask, render_template, jsonify, request
import random
import os

app = Flask(__name__)

def load_translations():
    """Loads all translations from the files."""
    translations = {}
    for class_name in ['a1', 'a2']:
        filename = f"translations_{class_name}.txt"
        if os.path.exists(filename):
            class_translations = []
            with open(filename, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split('\t')
                    if len(parts) == 2:
                        class_translations.append({"german": parts[0], "greek": parts[1]})
            translations[class_name] = class_translations
    return translations

translations_by_class = load_translations()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_word')
def get_word():
    class_name = request.args.get('class', 'a1')
    translations = translations_by_class.get(class_name, [])
    if not translations:
        return jsonify({"error": "No translations found for this class."})

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
    class_name = request.args.get('class', 'a1')
    return jsonify({'count': len(translations_by_class.get(class_name, []))})

@app.route('/find_word', methods=['GET'])
def find_word():
    class_name = request.args.get('class', 'a1')
    translations = translations_by_class.get(class_name, [])
    search_term = request.args.get('term', '').lower()
    if not search_term:
        return jsonify({'index': -1})

    for i, translation in enumerate(translations):
        if search_term in translation['german'].lower():
            return jsonify({'index': i})

    return jsonify({'index': -1})


if __name__ == '__main__':
    app.run(debug=True)
