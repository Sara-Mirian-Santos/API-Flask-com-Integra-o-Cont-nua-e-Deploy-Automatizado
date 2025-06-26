import pymysql
import mysql.connector
from app import app
from config import mysql
from flask import jsonify, request
# from flask import flash, request
from auth import auth_required

def check_database_connection():    #testa a conexão com o banco
    try:
        conn = mysql.connect()
        conn.close()
        return True                 #se foi possivel conectar ao banco escreve true em check_database_connection
    except Exception as e:
        print(f"Erro ao conectar o banco de dados: {e}")
        return False                #se não foi possivel conectar ao banco escreve false em check_database_connection

@app.route('/health')
def healthcheck():
    db_status = check_database_connection()
    if db_status:                   #verifica o status da variavel check_database_connection
        return jsonify({'api-status': 'api ok', 'status': '200', 'database': 'connected'})
    else:
        return jsonify({'api-status': 'api com erro', 'status': '503', 'database': 'not connected'})    #status 503 = serviço não disponível

@app.route('/criar', methods=['POST'])

def adicionar_produto():
    try:        
        _json = request.json
        _produto = _json['produto']
        _tamanho = _json['tamanho']
        _sabor = _json['sabor']
        _quantidade = _json['quantidade']	
        if _produto and _tamanho and _sabor and _quantidade and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)		
            sqlQuery = "INSERT INTO catalogo (produto, tamanho, sabor, quantidade) VALUES(%s, %s, %s, %s)"
            bindData = (_produto, _tamanho, _sabor, _quantidade)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify('Produto adicionado com sucesso!')
            response.status_code = 200
            return response
        else:
            return showMessage()
    except Exception as e:
        print(e)
    # finally:
    #     cursor.close() 
    #     conn.close()
     
@app.route('/busca', methods=['GET'])
@auth_required
def buscar():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM catalogo")
        catRow = cursor.fetchall()
        response = jsonify(catRow)
        response.status_code = 200
        return response
    except Exception as e:
        # print(e)
        reponse = jsonify({"Message": f"{e}"})
        return reponse
    # finally:
    #     cursor.close()
    #     conn.close() 

@app.route('/busca_produto/<int:id>')
def buscar_produtos(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM catalogo WHERE id_produto = %s", id)
        empRow = cursor.fetchone()
        response = jsonify(empRow)
        response.status_code = 200
        return response
    except Exception as e:
        # print(e)
        reponse = jsonify({"Message": f"{e}"})
        return reponse
    # finally:
    #     cursor.close()
    #     conn.close()

@app.route('/update', methods=['PUT'])
def atualizar_produto():
    try:
        _json = request.json
        _id = _json['id_produto']
        _produto = _json['produto']
        _tamanho = _json['tamanho']
        _sabor = _json['sabor']
        _quantidade = _json['quantidade']
        if _produto and _tamanho and _sabor and _quantidade and _id and request.method == 'PUT':
            sqlQuery = "UPDATE catalogo SET produto=%s, tamanho=%s, sabor =%s, quantidade=%s WHERE id_produto=%s"
            bindData = (_produto, _tamanho, _sabor, _quantidade, _id,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify('Atualizado com sucesso!')
            response.status_code = 200
            return response
        else:
            return showMessage()
    except Exception as e:
        print(e)
    # finally:
    #     cursor.close()
    #     conn.close()

@app.route('/produtos/<id>', methods=['DELETE'])
def deletar_produto(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM catalogo WHERE id_produto =%s", (id,))
		conn.commit()
		response = jsonify('Deletado com sucesso!')
		response.status_code = 200
		return response
	except Exception as e:
		print(e)
	# finally:
	# 	cursor.close()
	# 	conn.close()
        
       
@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    response = jsonify(message)
    response.status_code = 404
    return response
        
if (__name__ == "__main__"):
    app.run(port=5000, debug=True, host='0.0.0.0')

# port=5000 - define a porta
# debug=True - habilita o debug
# host='0.0.0.0' - abre para a internet