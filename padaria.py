import matplotlib.pyplot as plt
import numpy as np
import requests
from operator import itemgetter
from itertools import groupby

url = "http://localhost:3000/"
token = ""


#-----------------------------Programa Principal-------------------------------------

def titulo(texto, sublinhado="-"):
    print()
    print(texto)
    print(sublinhado*40)

def continuar():
    input("Tecle <Enter> para continuar...")

def login():
    titulo("Login do Usuário")

    email = input("E-mail: ")
    senha = input("Senha.: ")

    response = requests.post("http://localhost:3000/login", 
    json={"email": email, "senha": senha}
  )

    if response.status_code != 200:
        print("Erro... Login ou Senha inválidos")
        return
  
    dados = response.json()

  # para indicar que a variável aqui atribuída é a global 
  # (e não uma nova variável criada nesta função)
    global token 
    global userNome
    token = dados['token']
    usuarioNome = dados['nome']
    print(f"Bem-vindo ao sistema: {usuarioNome}")

def inclusao():
    titulo("Inclusão de Produtos")

    if token == "":
        print("Erro... Você deve logar-se primeiro")
        return
     
    nome = input("Nome do Produto: ")
    tipo = input("Tipo do Produto: ")
    validade = input("Validade do Produto: ")
    preco = float(input("Preço do Produto: "))


    response = requests.post("http://localhost:3000/produtos", 
      json={"nome": nome, "tipo": tipo, "validade": validade, "preco": preco},
      headers={"Authorization": f"Bearer {token}"})
    
    if response.status_code == 201:
        produto = response.json()
        print(f"Ok! Produto cadastrado com o código: {produto['id']}")

    else:
        print("Erro... Não foi possivel realizar a inclusão") 


def listagem():
    titulo("Listagem de Produtos")

    print("Descrição do Produto............Tipo..........Validade..........Preço R$:")
    print("===================================================================================")

    response = requests.get(url+"/produtos")

    if response.status_code != 200:
        print("Erro... Não foi possível conectar com a API")
        continuar()
        return
    
    produtos = response.json()

    for produto in produtos:
        print(f"{produto['nome']:30s} {produto['tipo']:15s} {produto['validade']:12s} {float(produto['preco']):9.2f}")

    continuar()

def alteracao():
    titulo("Alteração do Preços dos Produtos")

    id = int(input("ID do Produto: "))

    response = requests.get("http://localhost:3000/produtos")
    produtos = response.json()

    produto = [x for x in produtos if x['id'] == id]

    if len(produtos) == 0:
        print("Erro... Código do produto Inválido!!")
        return
    
    print(f"Nome do Produto: {produto[0]['nome']}")
    print(f"Tipo...........: {produto[0]['tipo']}")
    print(f"Validade........: {produto[0]['validade']}")
    print(f"Preço R$..........: {produto[0]['preco']}")
    print()

    novo_preco = float(input("Novo Preço R$......: "))

    response = requests.put("http://localhost:3000/produtos/" + str(id), json={"preco": novo_preco})
    
    if response.status_code == 200:
        print("Ok! Produto alterado com sucesso.")
    else:
        print("Erro... Não foi possivel realizar a alteração")

def exclusao():
    titulo("Exclusão de Produtos")
 #como fazer exclusão dos produtos por seu Id

    id = int(input("ID do Produto: "))

    response = requests.delete("http://localhost:3000/produtos/" + str(id))

    if response.status_code == 200:
        print("Ok! Produto excluído com sucesso.")
    else:
        print("Erro... Não foi possivel realizar a exclusão")

    continuar()


def agrupamento():
    titulo("Agrupamento de Produtos por Tipo")

    response = requests.get(url+"produtos")
    
    if response.status_code != 200:
        print("Erro... Não foi possivel obter dados da API")
        return
    
    produtos = response.json()

    # Ordenar os produtos por tipo
    produtos.sort(key=itemgetter('tipo'))

    # Agrupar os produtos por tipo
    agrupados = groupby(produtos, key=itemgetter('tipo'))

    for tipo, grupo in agrupados:
        print(f"Tipo: {tipo}")
        print("Cód. Produto................: Nome.............: Validade.........: Preço (R$)....:")
        print("-----------------------------------------------------------------------------------")
        for produto in grupo:
            print(f"{produto['id']:20} {produto['nome']:20} {produto['validade']:20} {produto['preco']}")
    print()

def grafico():
    titulo("Gráfico Comparando Venda dos Produtos por Preços")

    tipo1 = input("1º Produto: ")
    tipo2 = input("2º Produto: ")
    tipo3 = input("3º Produto: ")


# (): significa que é uma tupla (caracteristica: é imutavél)

    faixas = ("Até 10 reais", "Entre 10 e 30 reais", "Até de 50 reais")
# {}: significa que é um adicionário (chave: valor)        
    produtos= {
        tipo1: [0, 0, 0],
        tipo2: [0, 0, 0],
        tipo3: [0, 0, 0],
    }

    response = requests.get("http://localhost:3000/produtos")

    if response.status_code != 200:
        print("Erro... Não foi possível conectar com a API")
        return
    
    dados = response.json()

#    print(dados)

    for linha in dados:
        if linha['tipo'] == tipo1:
            if float(linha['preco']) <= 10:
                produtos[tipo1][0] += 1
            elif float(linha['preco']) <= 20:
                produtos[tipo1][1] += 1
            else:
                produtos[tipo1][2] += 1

        elif linha['tipo'] == tipo2:
                if float(linha['preco']) <= 15:
                    produtos[tipo2][0] += 1
                elif float(linha['preco']) <= 30:
                    produtos[tipo2][1] += 1
                else:
                    produtos[tipo2][2] += 1

        elif linha['tipo'] == tipo3:
            if float(linha['preco']) <= 50:
                produtos[tipo3][0] += 1
            elif float(linha['preco']) <= 60:
                produtos[tipo3][1] += 1
            else:
                produtos[tipo3][2] += 1                    

    x = np.arange(len(faixas))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots(layout='constrained')

    for attribute, measurement in produtos.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, padding=3)
        multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Quantidades')
    ax.set_title('Gráfico Comparativo de Faixas de Preços')
    ax.set_xticks(x + width, faixas)
    ax.legend(loc='upper left', ncols=3)
    ax.set_ylim(0, 10)

    plt.show()

    continuar()




#-----------------------------Programa Principal-------------------------------------


while True:
    titulo("Cadastro de Produtos", "=")
    print("1- Fazer Login")
    print("2- Incluir Produtos")
    print("3- Listar Produtos")
    print("4- Alterar Dados")
    print("5- Excluir Produtos")
    print("6- Agrupar Produtos")
    print("7- Gráfico Relacionando Faixas de Preços")
    print("0- Finalizar")
    
    opcao = int(input("Escolha uma Opção: "))

    if opcao == 1:
        login()
    elif opcao == 2:
        inclusao()
    elif opcao == 3:
        listagem()
    elif opcao == 4:
        alteracao()
    elif opcao == 5:
        exclusao()
    elif opcao == 6:
        agrupamento()
    if opcao == 7:
        grafico()
    elif opcao == 0:
        break