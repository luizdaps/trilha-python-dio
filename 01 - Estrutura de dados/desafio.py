import textwrap
from datetime import datetime

# Variáveis globais
usuarios = []
contas = []
AGENCIA = "0001"

def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nu]\tNovo usuário
    [nc]\tNova conta
    [lc]\tListar contas
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

def login():
    cpf = input("Digite seu CPF (apenas números): ")
    for usuario in usuarios:
        if usuario['cpf'] == cpf:
            return usuario
    print("Usuário não encontrado!")
    return None

def validar_valor(valor):
    try:
        valor = float(valor)
        if valor <= 0:
            print("Valor deve ser positivo!")
            return None
        return valor
    except ValueError:
        print("Valor inválido! Use números.")
        return None

def depositar(saldo, extrato):
    valor = input("Valor do depósito: R$ ")
    valor = validar_valor(valor)
    
    if valor:
        saldo += valor
        extrato.append(f"{datetime.now().strftime('%d/%m/%Y %H:%M')} - Depósito: R$ {valor:.2f}")
        print(f"Depósito de R$ {valor:.2f} realizado!")
    return saldo, extrato

def sacar(saldo, extrato, numero_saques):
    LIMITE_SAQUES = 3
    LIMITE_VALOR = 500
    
    if numero_saques >= LIMITE_SAQUES:
        print("Limite diário de saques atingido!")
        return saldo, extrato, numero_saques
    
    valor = input("Valor do saque: R$ ")
    valor = validar_valor(valor)
    
    if not valor:
        return saldo, extrato, numero_saques
    
    if valor > LIMITE_VALOR:
        print(f"Limite por saque: R$ {LIMITE_VALOR:.2f}")
    elif valor > saldo:
        print("Saldo insuficiente!")
    else:
        saldo -= valor
        numero_saques += 1
        extrato.append(f"{datetime.now().strftime('%d/%m/%Y %H:%M')} - Saque: R$ {valor:.2f}")
        print(f"Saque de R$ {valor:.2f} realizado!")
    
    return saldo, extrato, numero_saques

def mostrar_extrato(saldo, extrato):
    print("\n=============== EXTRATO ===============")
    if not extrato:
        print("Não houve movimentações.")
    else:
        print("\n".join(extrato))
    print(f"\nSaldo atual: R$ {saldo:.2f}")
    print("======================================")

def criar_usuario():
    cpf = input("CPF (apenas números): ")
    
    # Verifica se usuário já existe
    for usuario in usuarios:
        if usuario['cpf'] == cpf:
            print("CPF já cadastrado!")
            return
    
    nome = input("Nome completo: ")
    data_nasc = input("Data nasc. (dd/mm/aaaa): ")
    endereco = input("Endereço (rua, nro - bairro - cidade/UF): ")
    
    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nasc,
        "cpf": cpf,
        "endereco": endereco
    })
    
    print("Usuário cadastrado com sucesso!")

def criar_conta(usuario):
    global contas
    
    numero_conta = len(contas) + 1
    contas.append({
        "agencia": AGENCIA,
        "numero_conta": numero_conta,
        "usuario": usuario
    })
    
    print(f"Conta criada! Agência: {AGENCIA} - Conta: {numero_conta}")

def listar_contas():
    if not contas:
        print("Nenhuma conta cadastrada.")
        return
    
    print("\n============= CONTAS =============")
    for conta in contas:
        print(f"""
        Agência:\t{conta['agencia']}
        C/C:\t\t{conta['numero_conta']}
        Titular:\t{conta['usuario']['nome']}
        """)
    print("=================================")

def main():
    saldo = 0
    extrato = []
    numero_saques = 0
    usuario_logado = None
    
    while True:
        if not usuario_logado:
            print("\n=== BANCO DIO ===")
            opcao = input("[1] Login\n[2] Criar usuário\n[3] Sair\n=> ")
            
            if opcao == "1":
                usuario_logado = login()
            elif opcao == "2":
                criar_usuario()
            elif opcao == "3":
                break
            else:
                print("Opção inválida!")
            continue
        
        # Menu principal para usuários logados
        opcao = menu()
        
        if opcao == "d":
            saldo, extrato = depositar(saldo, extrato)
        elif opcao == "s":
            saldo, extrato, numero_saques = sacar(saldo, extrato, numero_saques)
        elif opcao == "e":
            mostrar_extrato(saldo, extrato)
        elif opcao == "nu":
            criar_usuario()
        elif opcao == "nc":
            criar_conta(usuario_logado)
        elif opcao == "lc":
            listar_contas()
        elif opcao == "q":
            usuario_logado = None
            print("Logout realizado!")
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()
