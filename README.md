# MVP E-commerce - Gestão de Pedidos e Logística (Cenário 2)

## Descrição do Projeto
Este projeto compõe o Produto Mínimo Viável (MVP) de um sistema de e-commerce focado na arquitetura de microsserviços baseada no **Cenário 2**. A aplicação adota a componentização para dividir o sistema em módulos independentes, facilitando o desenvolvimento escalável e a manutenção. 

O sistema é estruturado da seguinte forma:
*   **API Principal (Gestão de Pedidos):** Desenvolvida em Python (Flask) com persistência em SQLite, atua como o serviço orquestrador de pedidos.
*   **API Secundária (Logística e Fretes):** Serviço autônomo que processa as regras de negócio de cálculo de distâncias e valores de frete.
*   **API Externa (ViaCEP):** Serviço público consumido internamente pela API Principal para buscar e validar endereços por meio do CEP.

## Integração com API Externa (ViaCEP)
A API Principal consulta os dados da API pública **ViaCEP** de forma transparente, não causando o redirecionamento do usuário para outra aplicação.
*   **Serviço Utilizado:** ViaCEP
*   **Licença de Uso:** Serviço público, gratuito e não pago.
*   **Cadastro:** Não requer nenhum tipo de cadastro prévio, *token* ou chave de acesso.
*   **Rota Utilizada:** `GET https://viacep.com.br/ws/{cep}/json/`

---

## Estrutura de Diretórios
Os componentes estão separados em dois repositórios distintos para garantir a autonomia de cada serviço:
*   `api_principal_pedidos/`: Contém a regra de pedidos, a integração com o ViaCEP e o arquivo `docker-compose.yml` raiz.
*   `api_secundaria_logistica/`: Contém a regra de fretes e as suas próprias tabelas de banco de dados.

---

## Rotas Implementadas
Ambos os microsserviços implementam o padrão REST com pelo menos 4 rotas, contemplando os métodos POST, GET, PUT e DELETE.

### API Principal (Pedidos - Porta 5000)
*   **POST** `/api/pedidos`: Cria um novo pedido orquestrando o ViaCEP e a API de Logística.
*   **GET** `/api/pedidos/{id}`: Retorna os detalhes de um pedido.
*   **PUT** `/api/pedidos/{id}/status`: Atualiza o status do pedido.
*   **DELETE** `/api/pedidos/{id}`: Exclui o registro de um pedido.

### API Secundária (Logística - Porta 5001)
*   **POST** `/api/frete/calcular`: Calcula o valor e prazo de frete baseado no CEP de destino.
*   **GET** `/api/frete/tabelas`: Lista as tabelas de preços de frete.
*   **PUT** `/api/frete/tabelas/{id}`: Atualiza os valores base de uma tabela.
*   **DELETE** `/api/frete/tabelas/{id}`: Remove uma tabela do banco.

---

## Pré-requisitos
Para garantir a execução utilizando containers, o seu ambiente deve conter as seguintes ferramentas instaladas:
*   **Git** (para clonar os repositórios)
*   **Docker** e **Docker Compose**

---

## Instruções de Instalação e Execução (Step-by-Step)

### Passo 1: Preparar o ambiente local
Como o sistema utiliza dois repositórios separados, crie uma pasta raiz para agrupá-los e facilitar a execução via Docker Compose:
```bash
mkdir mvp-ecommerce
cd mvp-ecommerce
```

Passo 2: Clonar os repositórios
Clone ambos os módulos para dentro da pasta raiz criada:

Bash
# Repositório da API Principal
```
git clone [https://github.com/seu-usuario/api_principal_pedidos.git](https://github.com/seu-usuario/api_principal_pedidos.git)
```
# Repositório da API Secundária
```
git clone [https://github.com/seu-usuario/api_secundaria_logistica.git](https://github.com/seu-usuario/api_secundaria_logistica.git)
```

(Importante: O diretório da API Secundária deve manter o nome exato api_secundaria_logistica para que o Docker Compose o identifique corretamente).
Passo 3: Inicialização dos Containers
O arquivo docker-compose.yml foi disponibilizado na raiz do repositório da API principal. Navegue até essa pasta e inicialize os serviços:

```Bash
cd api_principal_pedidos
sudo docker compose up --build -d
```

O Docker irá criar os containers, instalar as bibliotecas Python (Flask, requests) e configurar os bancos de dados SQLite automaticamente.
Passo 4: Verificação do Ambiente
Confirme que os dois microsserviços estão ativos e em execução:

```Bash
sudo docker compose ps
```

A API Principal estará acessível na porta 5000 e a Secundária na porta 5001.
Passo 5: Teste Funcional (Exemplo de Fluxo)
Você pode simular o funcionamento da orquestração de serviços criando um pedido:



```Bash
curl -X POST http://localhost:5000/api/pedidos \
     -H "Content-Type: application/json" \
     -d '{"produto": "Monitor 27 Polegadas", "cep_destino": "01001000"}'
```

O retorno exibirá o endereço (trazido pelo ViaCEP) e o valor do frete (trazido pela API Secundária).
Passo 6: Desligar a aplicação
Para interromper a execução, rode:

```Bash
docker-compose down
```

