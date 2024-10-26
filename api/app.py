from flask import Flask, request, jsonify
import requests
import json
from functools import lru_cache

app = Flask(__name__)

# URL dos arquivos JSON no Dropbox
dropbox_url_pag = 'https://www.dropbox.com/scl/fi/3oxqqhu54196cc97eh2nh/banners.json?rlkey=ub80nfxrldnczuwgrfomf6sg0&st=4s2atc41&dl=1'
dropbox_url_link = 'https://www.dropbox.com/scl/fi/v2fuahx8uxcar2edrkk8m/Filmes_Series.json?rlkey=mjw8j0iw5047eofkcm2wkqwbo&st=ldnznh1z&dl=1'

def carregar_dados_json(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            dados = json.loads(response.content)
            return dados
        else:
            return []
    except Exception as e:
        print(f"Erro ao carregar JSON: {e}")
        return []

@app.route('/api/filmes-series', methods=['GET'])
def filmes_series():
    # Carregar dados do JSON do Dropbox
    data = carregar_dados_json(dropbox_url_pag)

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

# Implementação do cache para a rota de extração do link
@lru_cache(maxsize=100)  # Configurando o cache para 100 filmes
def get_filme_link(id_filme):
    data = carregar_dados_json(dropbox_url_link)
    for filme in data:
        if filme['id'] == id_filme:
            return filme
    return None

@app.route('/api/filme-link', methods=['GET'])
def filme_link():
    id_filme = request.args.get('id')
    if not id_filme:
        return jsonify({'error': 'ID do filme é obrigatório'}), 400

    filme = get_filme_link(id_filme)
    if filme:
        return jsonify({'filme': filme})
    else:
        return jsonify({'error': 'Filme não encontrado'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
