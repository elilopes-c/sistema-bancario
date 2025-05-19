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

# Funções
while True:
    opcao = input(menu) 

    if opcao == "d":
        print("Depósito")
    
    elif opcao == "s":
        print("Saque")
    
    elif opcao == "e":
        print("Extrato")    
    
    elif opcao == "q":
        print("Saindo...")
        break
    
    else:
        print("Opção inválida, por favor selecione novamente a operação desejada.")