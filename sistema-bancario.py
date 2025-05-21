# As aspas triplas permitem que você defina strings que se estendem por várias linhas diretamente no seu código. 
# As quebras de linha presentes no código serão preservadas na string final.

menu = """

[d] Depositar
[s] Sacar   
[e] Extrato
[q] Sair
=> """

# Variáveis
saldo = 0
limite = 500
extrato = ""
numero_de_saques = 0    
limite_de_saques = 3
historico_depositos = []
historico_saques = []

# Funções
while True:
    opcao = input(menu) 

    if opcao == "d":
        
        deposito = float(input("Informe o valor do depósito: "))
        if deposito > 0:
            saldo += deposito
            historico_depositos.append(deposito)
            print(f"Depósito de R${deposito:.2f} realizado com sucesso")
            print(f"Seu saldo é R${saldo:.2f}")
            
        else:
            print("Valor inválido para depósito.")
    
    elif opcao == "s":
        if numero_de_saques >= limite_de_saques:
            print(f"Limite de saques: {limite_de_saques} atingido!")
        else:
            saque = float(input("Informe o valor do saque: "))
            if saque > saldo:
                print("Saque indisponível por saldo insuficiente.")
            elif saque > limite:
                print(f"O valor do saque excede o limite de R${limite:.2f}.")
            elif saque <= 0:
                print("Valor de saque inválido.")
            else:
                saldo -= saque
                historico_saques.append(saque)    
                print(f"Saque de R${saque:.2f} realizado com sucesso!")
                print(f"Seu saldo é R${saldo:.2f}")
                numero_de_saques += 1

    
    elif opcao == "e":
        print("Extrato")    
    
    elif opcao == "q":
        print("Saindo...")
        break

    else:
        print("Opção inválida, por favor selecione novamente a operação desejada.")
