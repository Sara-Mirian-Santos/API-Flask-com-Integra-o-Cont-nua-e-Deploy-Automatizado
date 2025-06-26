import pytest
from main import adicionar_produto, app, atualizar_produto, deletar_produto
from unittest.mock import MagicMock, patch

@pytest.fixture
def client():   #o client é criado para que eu possa acessar os endpoints
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_cursor() -> MagicMock:
    cursor = MagicMock()
    cursor.execute.return_value = {     #quando o comando execute é chamado, ele passa a utilizar os dados a seguir
        "id_produto": 1,
        "produto": "batata frita",
        "quantidade": 1,
        "sabor": "cheddar e bacon",
        "tamanho": "media"
    }
    return cursor

def test_atualizar_produto(client, mock_cursor):
    dados = {               #Dados que eu espero atualizar
        "id_produto": 3,
        "produto": "pizza",
        "quantidade": 1,
        "sabor": "queijo",
        "tamanho": "media"
    }

    # Conexão e o cursor do banco de dados
    with patch('main.mysql.connect') as mock_connect:   # ao adicionar o patch ('main.mysql.connect'), estou dizendo que eu quero modificar o "mysql.connect" que estou importando da "main" para que o "mock_connect" posso simular o "mysql.connect"
		# Transformo o conn e o cursor em objetos mocks
        # conn = mysql.connect()
		# cursor = conn.cursor()
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value

        response = client.put('/update', json=dados)                #simulo uma chamada
        chamada = atualizar_produto()
        resposta = chamada.get_json()
        assert resposta == 'Atualizado com sucesso!'  #verifico se foi atualizado com sucesso

def test_adicionar_produto(client, mock_cursor):
    dados = {
        "id_produto": 3,
        "produto": "batata frita",
        "quantidade": 1,
        "sabor": "queijo",
        "tamanho": "media"
    }

    # Conexão e o cursor do banco de dados
    with patch('main.mysql.connect') as mock_connect:
		# Transformo o conn e o cursor em objetos mocks
        # conn = mysql.connect()
		# cursor = conn.cursor()
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value

        response = client.post('/criar', json=dados)
        chamada = adicionar_produto()                #simulo uma chamada
        resposta = response.get_json()
        assert resposta == 'Produto adicionado com sucesso!'  #verifico se foi adicionado com sucesso

def test_deletar_produto(client, mock_cursor):
    produto_id = 3

    # Conexão e o cursor do banco de dados
    with patch('main.mysql.connect') as mock_connect:
		# Transformo o conn e o cursor em objetos mocks
        # conn = mysql.connect()
		# cursor = conn.cursor()
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value

        response = client.delete('/produtos/<id>')
        chamada = deletar_produto(3)         #simulo uma chamada
        resposta = chamada.get_json()
        assert resposta == 'Deletado com sucesso!'  #verifico se foi deletado com sucesso

#outra forma de fazer
        # response = client.delete('/produtos/<id>', json=produto_id)         #simulo uma chamada
        # resposta = response.get_json()
        # assert resposta == 'Deletado com sucesso!'  #verifico se foi deletado com sucesso