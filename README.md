# 🏦 Criando um Sistema Bancário com Python 🐍

## ✨ Sobre o Projeto

Este projeto é um desafio prático proposto pelo expert **Guilherme Arthur de Carvalho** [@decarvalhogui](https://www.linkedin.com/search/results/all/?heroEntityKey=urn%3Ali%3Afsd_profile%3AACoAAAckd74BsNtuzaI-QVU9BJIezynod1txAPE&keywords=Guilherme%20Arthur%20de%20Carvalho&origin=ENTITY_SEARCH_HOME_HISTORY&sid=J8Q) da plataforma **DIO (Digital Innovation One)**. Foi uma oportunidade incrível para consolidar meus conhecimentos em Python e desenvolver uma aplicação funcional do zero!

## 🎯 O Desafio

Fomos contratados por um grande banco para desenvolver um novo sistema, visando modernizar suas operações. Para esta primeira versão, o desafio consistiu em implementar as 3 operações essenciais de um sistema bancário:

* **Depósito 💰:** Permitir ao usuário depositar valores positivos na conta. Todos os depósitos devem ser armazenados e exibidos na operação de extrato.
* **Saque 💸:** Permitir até 3 saques diários, com um limite máximo de R$ 500,00 por saque. O sistema deve verificar saldo insuficiente e limites. Todos os saques também devem ser armazenados e exibidos no extrato.
* **Extrato 📜:** Listar todas as movimentações (depósitos e saques) realizadas na conta e, no final da listagem, exibir o saldo atual da conta. Os valores devem ser exibidos no formato "R$ xxx.xx".

## 🛠️ Tecnologias e Conceitos Utilizados

Para desenvolver este sistema, apliquei e reforcei diversos conceitos fundamentais da linguagem Python:

* **Variáveis e Tipos de Dados:** Utilização de `int`, `float` para valores numéricos e `str` para textos, além de `list` para armazenar históricos de transações.
* **Estruturas Condicionais (`if`, `elif`, `else`)**: Essenciais para controlar o fluxo do programa, validando entradas, verificando limites de saque e saldo, e direcionando as operações.
* **Estruturas de Repetição (`while` Loop)**: Para manter o menu do sistema em execução contínua, permitindo múltiplas operações até que o usuário decida sair.
* **Entrada e Saída de Dados (`input()`, `print()`):** Interação com o usuário para receber comandos e valores, e para exibir mensagens e resultados das operações.
* **F-Strings (Formatted String Literals):** Para formatar a saída de mensagens, especialmente valores monetários, de forma clara e legível (ex: `R${valor:.2f}`).
* **Manipulação de Listas:** Uso de métodos como `.append()` para adicionar novos itens (depósitos e saques) aos históricos.
* **Lógica Booleana:** Utilização de operadores lógicos (`and`, `or`, `not`) para construir condições complexas e eficientes.

---
