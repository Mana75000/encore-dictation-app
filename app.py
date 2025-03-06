from flask import Flask, render_template, request, jsonify
import difflib

app = Flask(__name__)  # No need to specify template_folder, it's default

# The correct dictation text (you can modify this)
CORRECT_TEXT = "La conquête de l'espace est un rêve ancien de l'humanité."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    user_text = request.json.get("text", "").strip()
    corrections = highlight_differences(user_text, CORRECT_TEXT)
    return jsonify({"corrected": corrections})

def highlight_differences(user_input, correct_text):
    """Compares user input with correct text and highlights mistakes."""
    user_words = user_input.split()
    correct_words = correct_text.split()
    
    diff = difflib.ndiff(correct_words, user_words)
    result = []
    
    for word in diff:
        if word.startswith("- "):  # Missing word
            result.append(f'<span style="color:red; text-decoration:line-through;">{word[2:]}</span>')
        elif word.startswith("+ "):  # Extra word
            result.append(f'<span style="color:blue;">{word[2:]}</span>')
        else:
            result.append(word[2:])  # Correct word

    return " ".join(result)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
