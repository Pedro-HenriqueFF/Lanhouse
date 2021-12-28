from flask import Flask
from waitress import serve
from flask import render_template
from flask import request,url_for,redirect,flash,make_response
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
import logging
import os
import datetime
from cadastroM import cadastroM
from usuarioForm import UsuarioForm
from locaForm import LocarForm
from flask_session import Session
from flask import session
from formLogin import LoginForm
import hashlib
import json
from flask_json import FlaskJSON, JsonError, json_response, as_json

app = Flask(__name__)
bootstrap = Bootstrap(app)
CSRFProtect(app)
CSV_DIR = '/flask/'

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)
app.config['WTF_CSRF_SSL_STRICT'] = False
Session(app)
FlaskJSON(app)
app.config['JSON_ADD_STATUS'] = False

logging.basicConfig(filename=CSV_DIR + 'app.log', filemode='w', format='%(asctime)s %(name)s - %(levelname)s - %(message)s',level=logging.DEBUG)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + CSV_DIR + 'bd.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True

from database import db
db.init_app(app)

from usuario import Usuario
from maquinas import Maquina
from locacao import Locacao

@app.before_first_request
def inicializar_bd():
    #db.drop_all()
    db.create_all()

@app.route('/')
def root():
    if session.get('autenticado',False)==False:
        return (redirect(url_for('login')))
    return (render_template('index.html'))
        
@app.route('/maquina/cadastrar',methods=['POST','GET'])
def cadastrar_chave():
    if session.get('autenticado',False)==False:
        return (redirect(url_for('login')))
    form = cadastroM()
    if form.validate_on_submit():
        #PROCESSAMENTO DOS DADOS RECEBIDOS
        novaMaquina = Maquina(nome=request.form['nome'])
        db.session.add(novaMaquina)
        db.session.commit()
        flash('Maquina cadastrada com sucesso!')
        return(redirect(url_for('root')))
    return (render_template('form.html',form=form,action=url_for('cadastrar_chave')))

@app.route('/maquina/listar')
def listar_chaves():
    maquinas = Maquina.query.order_by(Maquina.nome).all()
    return(render_template('maquinas.html',maquinas=maquinas))

@app.route('/usuario/listar')
def listar_usuarios():
    if session.get('autenticado',False)==False:
        return (redirect(url_for('login')))
    usuarios = Usuario.query.order_by(Usuario.nome).all()
    return(render_template('usuarios.html',usuarios=usuarios))

@app.route('/usuario/cadastrar',methods=['POST','GET'])
def cadastrar_usuario():
    if session.get('autenticado',False)==False:
        return (redirect(url_for('login')))
    form = UsuarioForm()
    if form.validate_on_submit():
        #PROCESSAMENTO DOS DADOS RECEBIDOS
        nome = request.form['nome']
        username = request.form['username']
        email = request.form['email']
        telefone = request.form['telefone']
        senha = request.form['senha']
        senhahash = hashlib.sha1(senha.encode('utf8')).hexdigest()
        novoUsuario = Usuario(nome=nome,username=username,email=email,telefone=telefone,senha=senhahash)
        db.session.add(novoUsuario)
        db.session.commit()
        flash(u'Usuário cadastrado com sucesso!')
        return(redirect(url_for('root')))
    return (render_template('form.html',form=form,action=url_for('cadastrar_usuario')))

@app.route('/maquina/locar',methods=['POST','GET'])
def emprestar_chave():
    if session.get('autenticado',False)==False:
        return (redirect(url_for('login')))
    form = LocarForm()
    maquinas = Maquina.query.filter(Maquina.disponivel==True).order_by(Maquina.nome).all()
    form.maquina.choices = [(c.id,c.nome) for c in maquinas]
    if form.validate_on_submit():
        #IMPLEMENTAÇÃO DO CADASTRO DO EMPRÉSTIMO
        nome = request.form['nome']
        maquina = int(request.form['maquina'])
        novoEmprestimo = Locacao(id_usuario=1,id_maquina=maquina,nome_pessoa=nome)
        chaveAlterada = Maquina.query.get(maquina)
        chaveAlterada.disponivel = False
        db.session.add(novoEmprestimo)
        db.session.commit()
        return(redirect(url_for('root')))
    return(render_template('form.html',form=form,action=url_for('emprestar_chave')))

@app.route('/maquina/listar_emprestimos')
def listar_emprestimos():
    locacoes = Locacao.query.order_by(Locacao.data_emprestimo.desc()).all()
    return(render_template('emprestimos.html',locacoes=locacoes))

@app.route('/maquina/devolver/<id_emprestimo>',methods=['GET','POST'])
def devolver_chave(id_emprestimo):
    if session.get('autenticado',False)==False:
        return (redirect(url_for('login')))
    id_emprestimo = int(id_emprestimo)
    emprestimo = Locacao.query.get(id_emprestimo)
    emprestimo.data_devolucao = datetime.datetime.now()
    maquina = Maquina.query.get(emprestimo.id_chave)
    maquina.disponivel = True
    db.session.commit()
    return (redirect(url_for('root')))

@app.route('/emprestimo/remover/<id_emprestimo>',methods=['GET','POST'])
def remover_emprestimo(id_emprestimo):
    if session.get('autenticado',False)==False:
        return (redirect(url_for('login')))
    id_emprestimo = int(id_emprestimo)
    emprestimo = Locacao.query.get(id_emprestimo)
    id_chave = emprestimo.id_chave
    maquina = Maquina.query.get(id_chave)
    maquina.disponivel = True
    db.session.delete(emprestimo)
    db.session.commit()
    return (redirect(url_for('root')))

@app.route('/usuario/login',methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #PROCESSAMENTO DOS DADOS RECEBIDOS
        usuario = request.form['usuario']
        senha = request.form['senha']
        senhahash = hashlib.sha1(senha.encode('utf8')).hexdigest()
        #Verificar se existe alguma linha na tabela usuários com o login e senha recebidos
        linha = Usuario.query.filter(Usuario.username==usuario,Usuario.senha==senhahash).all()
        if (len(linha)>0): #"Anota" na sessão que o usuário está autenticado
            session['autenticado'] = True
            session['usuario'] = linha[0].id
            flash(u'Usuário autenticado com sucesso!')
            resp = make_response(redirect(url_for('root')))
            if 'contador' in request.cookies:
                contador = int(request.cookies['contador'])
                contador = contador + 1
            else:
                contador = 1
            resp.set_cookie('contador',str(contador))
            return(resp)
        else: #Usuário e senha não conferem
            flash(u'Usuário e/ou senha não conferem!')
            resposta = make_response(redirect(url_for('login')))
            if 'contador2' in request.cookies:
                contador2 = int(request.cookies['contador2'])
                contador2 = contador2 + 1
            else:
                contador2 = 1
            resposta.set_cookie('contador2',str(contador2)) 
            return(resposta)
    return (render_template('form.html',form=form,action=url_for('login')))

@app.route('/usuario/logout',methods=['POST','GET'])
def logout():
    session.clear()
    return(redirect(url_for('login')))

'''
rotas com JSON
'''

@app.route('/chave/listar/json')
def listar_chaves_json():
    chaves = Chave.query.order_by(Chave.nome).all()
    resultado = json.dumps([ row.asdict() for row in chaves ])
    return(resultado)

@app.route('/chave/situacao/<nome>')
def chave_situacao(nome):
    chave = Chave.query.filter(Chave.nome==nome).first()
    if chave is not None:
        if chave.disponivel:
            resultado = json_response(situacao="DISPONIVEL")
        else:
            #Procurar pra quem está emprestada
            emprestimo = Emprestimo.query.filter(Emprestimo.id_chave==chave.id).order_by(Emprestimo.id.desc()).first()
            #"Montar" a resposta
            resultado = json_response(situacao="EMPRESTADA",nome=emprestimo.nome_pessoa)
    else:
        resultado = json_response(situacao="CHAVE INEXISTENTE")

    return(resultado)

@app.route('/chave/teste')
def chave_teste():
    #return(json_response(aplicacao="Flask",versao="2.0",data="28/09/2021"))
    chaves = Chave.query.order_by(Chave.nome).all()
    lista_chaves = []
    for chave in chaves:
        linha = {"nome": chave.nome, "disponivel": chave.disponivel}
        lista_chaves.append(linha)
    resultado = json.dumps([linha for linha in lista_chaves])
    return(resultado)

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=80, url_prefix='/app')

