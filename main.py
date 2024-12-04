import requests
from deep_translator import GoogleTranslator
import os

def menu():
    print("\n========= API CONSELHOS =========")
    print("1. (EN) Conselhos")
    print("2. (PT-BR) Conselhos traduzidos")
    print("3. (EN) Conselhos salvos")
    print("4. (PT-BR) Conselhos salvos")
    print("5. Sair")
    return input("Digite o número da opção: ")

def obter_conselho():
    try:
        response = requests.get("https://api.adviceslip.com/advice")
        if response.status_code == 200:
            conselho = response.json()["slip"]
            return conselho["id"], conselho["advice"]
        else:
            print("Erro ao acessar a API.")
    except Exception as e:
        print(f"Erro: {e}")

def salvar_conselho(id_conselho, texto_conselho):
    try:
        with open("conselhos.txt", "a") as arquivo:
            arquivo.write(f"{id_conselho}:{texto_conselho}\n")
        print("Conselho salvo com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar o conselho: {e}")

def en_conselhos():
    if os.path.exists("conselhos.txt"):
        with open("conselhos.txt", "r") as arquivo:
            print("\nConselhos salvos:")
            print(arquivo.read())
    else:
        print("Nenhum conselho salvo ainda.")

def ptbr_conselhos(texto):
    try:
        return GoogleTranslator(source='en', target='pt').translate(texto)
    except Exception as e:
        print(f"Erro ao traduzir: {e}")

def ptbr_conselhos_salvos():
    if os.path.exists("conselhos.txt"):
        with open("conselhos.txt", "r") as arquivo:
            linhas = arquivo.readlines()
        print("\nPTBR Conselhos:")
        for linha in linhas:
            id_conselho, texto_conselho = linha.strip().split(":", 1)
            texto_traduzido = ptbr_conselhos(texto_conselho)
            print(f"ID {id_conselho}: {texto_traduzido}")
    else:
        print("Nenhum conselho salvo para traduzir.")

def main():
    while True:
        opcao = menu()

        if opcao == "1":
            quantidade = int(input("Quantos conselhos deseja obter? "))
            for _ in range(quantidade):
                id_conselho, texto_conselho = obter_conselho()
                if id_conselho and texto_conselho:
                    print(f"Conselho (ID {id_conselho}): {texto_conselho}")
                    salvar = input("Gostaria de salvar este conselho? (s/n): ").strip().lower()
                    if salvar == 's':
                        salvar_conselho(id_conselho, texto_conselho)
        elif opcao == "2":
            quantidade = int(input("Quantos conselhos traduzidos deseja obter? "))
            for _ in range(quantidade):
                id_conselho, texto_conselho = obter_conselho()
                if id_conselho and texto_conselho:
                    texto_traduzido = ptbr_conselhos(texto_conselho)
                    print(f"\nConselho (ID {id_conselho}):")
                    print(f"Em inglês: {texto_conselho}")
                    print(f"Em português: {texto_traduzido}")
                    salvar = input("Gostaria de salvar este conselho? (s/n): ").strip().lower()
                    if salvar == 's':
                        salvar_conselho(id_conselho, texto_conselho)
        elif opcao == "3":
            en_conselhos()
        elif opcao == "4":
            ptbr_conselhos_salvos()
        elif opcao == "5":
            print("Encerrando o programa. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
