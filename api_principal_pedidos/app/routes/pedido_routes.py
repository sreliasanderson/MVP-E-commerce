from flask import Blueprint, request, jsonify
from app.database.db_config import get_db_connection
from app.services.viacep_service import buscar_endereco
from app.services.logistica_service import calcular_frete

pedido_bp = Blueprint('pedido_bp', __name__)

@pedido_bp.route('/api/pedidos', methods=['POST'])
def criar_pedido():
    """
    Cria um novo pedido
    ---
    tags:
      - Pedidos
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            produto:
              type: string
              example: "Teclado Mecânico"
            cep_destino:
              type: string
              example: "01001000"
    responses:
      201:
        description: Pedido criado com sucesso
      400:
        description: CEP inválido
    """
    dados = request.get_json()
    produto = dados.get('produto')
    cep = dados.get('cep_destino')

    endereco = buscar_endereco(cep)
    if not endereco:
        return jsonify({"erro": "CEP invalido ou nao encontrado no ViaCEP"}), 400

    valor_frete = calcular_frete(cep)
    status = "Pendente"

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO pedidos (produto, cep_destino, endereco_completo, valor_frete, status) VALUES (?, ?, ?, ?, ?)',
        (produto, cep, endereco, valor_frete, status)
    )
    conn.commit()
    pedido_id = cursor.lastrowid
    conn.close()

    return jsonify({
        "mensagem": "Pedido criado com sucesso",
        "pedido_id": pedido_id,
        "frete_calculado": valor_frete,
        "endereco_entrega": endereco
    }), 201

@pedido_bp.route('/api/pedidos/<int:id>', methods=['GET'])
def obter_pedido(id):
    """
    Busca os detalhes de um pedido
    ---
    tags:
      - Pedidos
    parameters:
      - in: path
        name: id
        required: true
        type: integer
    responses:
      200:
        description: Dados do pedido
      404:
        description: Pedido não encontrado
    """
    conn = get_db_connection()
    pedido = conn.execute('SELECT * FROM pedidos WHERE id = ?', (id,)).fetchone()
    conn.close()

    if pedido is None:
        return jsonify({"erro": "Pedido nao encontrado"}), 404
    
    return jsonify(dict(pedido)), 200

@pedido_bp.route('/api/pedidos/<int:id>/status', methods=['PUT'])
def atualizar_status_pedido(id):
    """
    Atualiza o status de um pedido
    ---
    tags:
      - Pedidos
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
            status:
              type: string
              example: "Pago"
    responses:
      200:
        description: Status atualizado
      400:
        description: Erro de validação
    """
    dados = request.get_json()
    novo_status = dados.get('status')

    if not novo_status:
        return jsonify({"erro": "Campo 'status' e obrigatorio"}), 400

    conn = get_db_connection()
    conn.execute('UPDATE pedidos SET status = ? WHERE id = ?', (novo_status, id))
    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Status atualizado com sucesso"}), 200

@pedido_bp.route('/api/pedidos/<int:id>', methods=['DELETE'])
def deletar_pedido(id):
    """
    Remove um pedido do sistema
    ---
    tags:
      - Pedidos
    parameters:
      - in: path
        name: id
        required: true
        type: integer
    responses:
      200:
        description: Pedido removido
    """
    conn = get_db_connection()
    conn.execute('DELETE FROM pedidos WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Pedido removido com sucesso"}), 200