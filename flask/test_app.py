from app import app
import pytest

aplicacao = app.test_client()

def login(client, username):
    return client.post('/usuario/login', data=dict(
        usuario=username,
        senha='123456'
    ), follow_redirects=True)

def logout(client):
    return client.get('/usuario/logout', follow_redirects=True)

@pytest.fixture
def client():
    return (aplicacao)

@pytest.fixture
def preparacao():
    app.config['WTF_CSRF_ENABLED'] = False
    yield
    app.config['WTF_CSRF_ENABLED'] = True

def test_0_principal(client):
    rv = client.get('/',follow_redirects=True)
    assert 200 == rv.status_code

def test_1_principal(client):
    rv = client.get('/',follow_redirects=True)
    assert b'Nome de usu' in rv.data
    assert b'Senha:' in rv.data

@pytest.mark.usefixtures('preparacao')
def test_2_login(client):
    rv = login(client,'Master')
    assert b'autenticado com sucesso' in rv.data

@pytest.mark.usefixtures('preparacao')
def test_3_login_errado(client):
    rv = login(client,'UsuarioNaoExistente')
    assert b'rio e/ou senha' in rv.data

def test_4_dispositivo_cadastrar_get(client):
    rv = client.get('/dispositivo/cadastrar',follow_redirects=True)
    assert b'Nome do dispositivo' in rv.data

def test_5_dispositivo_listar(client):
    rv = client.get('/dispositivo/listar',follow_redirects=True)
    assert rv.status_code==200

def test_6_usuario_cadastrar_get(client):
    rv = client.get('/usuario/cadastrar',follow_redirects=True)
    assert b'Nome de usu' in rv.data

def test_7_usuario_listar(client):
    rv = client.get('/usuario/listar',follow_redirects=True)
    assert rv.status_code==200

def test_8_dispositivo_alugar_get(client):
    rv = client.get('/dispositivo/alugar',follow_redirects=True)
    assert b'Nome de quem pega emprestado' in rv.data

def test_9_dispositivo_listar_locacoes(client):
    rv = client.get('/dispositivo/listar_locacoes',follow_redirects=True)
    assert rv.status_code==200
    