from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# URL do arquivo JSON no Dropbox
dropbox_url = 'https://firebasestorage.googleapis.com/v0/b/venusvmax-aa14f.appspot.com/o/Filmes_Series.json?alt=media&token=800708c1-f01a-48a5-8980-4c9d2faa5ee7'

def carregar_dados_json():
    try:
        # Fazer o download do arquivo JSON
        response = requests.get(dropbox_url)
        if response.status_code == 200:
            # Carregar o conteúdo JSON
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
    data = carregar_dados_json()

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
