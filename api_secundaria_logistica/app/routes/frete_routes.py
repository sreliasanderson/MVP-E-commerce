from flask import Blueprint, request, jsonify
from app.database.db_config import get_db_connection

frete_bp = Blueprint('frete_bp', __name__)

@frete_bp.route('/api/frete/calcular', methods=['POST'])
def calcular_frete():
    """
    Calcula o valor do frete
    ---
    tags:
      - Frete
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            cep_destino:
              type: string
              example: "01001000"
    responses:
      200:
        description: Frete calculado com sucesso
    """
    dados = request.get_json()
    cep_destino = dados.get('cep_destino')
    
    if not cep_destino:
        return jsonify({"erro": "CEP nao fornecido"}), 400
        
    valor_frete = 15.0 if cep_destino.startswith('0') else 35.50
    return jsonify({"valor_frete": valor_frete, "prazo_dias": 5}), 200

@frete_bp.route('/api/frete/tabelas', methods=['GET'])
def listar_tabelas():
    """
    Lista todas as tabelas de frete base
    ---
    tags:
      - Tabelas de Frete
    responses:
      200:
        description: Lista de tabelas
    """
    conn = get_db_connection()
    tabelas = conn.execute('SELECT * FROM tabelas_frete').fetchall()
    conn.close()
    return jsonify([dict(t) for t in tabelas]), 200

@frete_bp.route('/api/frete/tabelas/<int:id>', methods=['PUT'])
def atualizar_tabela(id):
    """
    Atualiza o valor de uma tabela de frete
    ---
    tags:
      - Tabelas de Frete
    parameters:
      - in: path
        name: id
        required: true
        type: integer
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            valor_base:
              type: number
              example: 22.50
    responses:
      200:
        description: Tabela atualizada
    """
    dados = request.get_json()
    novo_valor = dados.get('valor_base')
    conn = get_db_connection()
    conn.execute('UPDATE tabelas_frete SET valor_base = ? WHERE id = ?', (novo_valor, id))
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Tabela atualizada"}), 200

@frete_bp.route('/api/frete/tabelas/<int:id>', methods=['DELETE'])
def deletar_tabela(id):
    """
    Remove uma tabela de frete
    ---
    tags:
      - Tabelas de Frete
    parameters:
      - in: path
        name: id
        required: true
        type: integer
    responses:
      200:
        description: Tabela removida
    """
    conn = get_db_connection()
    conn.execute('DELETE FROM tabelas_frete WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Tabela removida"}), 200