from flask import Flask, jsonify
import requests
import json
from functools import lru_cache

app = Flask(__name__)

# URL do arquivo JSON no Dropbox
dropbox_url = 'https://www.dropbox.com/scl/fi/v2fuahx8uxcar2edrkk8m/Filmes_Series.json?rlkey=mjw8j0iw5047eofkcm2wkqwbo&st=ldnznh1z&dl=1'

# Cache para armazenamento de dados JSON
@lru_cache(maxsize=1)  # Cache com capacidade para 1 arquivo JSON
def carregar_dados_com_cache():
    try:
        response = requests.get(dropbox_url)
        if response.status_code == 200:
            dados = json.loads(response.content)
            return dados
        else:
            return []
    except Exception as e:
        print(f"Erro ao carregar JSON: {e}")
        return []

@app.route('/api/cache-filmes', methods=['GET'])
def cache_filmes():
    # Carregar dados do cache
    data = carregar_dados_com_cache()
    return jsonify(data)

@app.route('/api/filmes-series', methods=['GET'])
def filmes_series():
    # Carregar dados do cache para paginação
    data = carregar_dados_com_cache()

    # Parâmetros de paginação
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 25))

    # Cálculo da paginação
    start = (page - 1) * per_page
    end = start + per_page

    # Obter a página de dados
    paginated_data = data[start:end]

    # Retornar dados paginados
    return jsonify({
        'page': page,
        'per_page': per_page,
        'total': len(data),
        'data': paginated_data
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
