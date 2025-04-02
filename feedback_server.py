
from flask import Flask, request, jsonify
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)

# Caminho para o arquivo CSV
FEEDBACK_FILE = 'feedbacks.csv'

# Criar DataFrame vazio se o arquivo não existir
if not os.path.exists(FEEDBACK_FILE):
    df = pd.DataFrame(columns=['timestamp', 'rating', 'comment', 'name', 'email'])
    df.to_csv(FEEDBACK_FILE, index=False)
else:
    df = pd.read_csv(FEEDBACK_FILE)

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
        df.to_csv(FEEDBACK_FILE, index=False)
        
        return jsonify({'status': 'success', 'message': 'Feedback recebido!'}), 200
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
