from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from datetime import datetime
import os

print(f"Current working directory: {os.getcwd()}")
print(f"Files in directory: {os.listdir()}")
app = Flask(__name__)
CORS(app, resources={r"/submit_feedback": {"origins": "*"}})

# Configure for production
PORT = int(os.getenv('PORT', 5000))
CSV_PATH = os.getenv('CSV_PATH', 'feedbacks.csv')

# Criar DataFrame vazio se o arquivo não existir
if not os.path.exists(CSV_PATH):
    df = pd.DataFrame(columns=['timestamp', 'rating', 'comment', 'name', 'email'])
    df.to_csv(CSV_PATH, index=False)
else:
    df = pd.read_csv(CSV_PATH)

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    try:
        # Receber dados do formulário
        data = request.json
        
        # Criar novo registro
        new_feedback = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'rating': int(data.get('rating', 0)),
            'comment': data.get('comment', ''),
            'name': data.get('name', ''),
            'email': data.get('email', '')
        }

        # Adicionar ao DataFrame
        global df
        df = pd.concat([df, pd.DataFrame([new_feedback])], ignore_index=True)
        
        # Salvar no arquivo CSV
        df.to_csv(CSV_PATH, index=False)
        
        return jsonify({'status': 'success', 'message': 'Feedback recebido!'}), 200
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
