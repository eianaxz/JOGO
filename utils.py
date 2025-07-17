import os
import time

def limpar_tela():
    # Limpa o console para uma melhor experiência
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    input("\nPressione Enter para continuar...")
    limpar_tela()

def imprimir_titulo(titulo):
    limpar_tela()
    print("=" * 50)
    print(f"{titulo.center(50)}")
    print("=" * 50)
    time.sleep(1)

def imprimir_log(mensagem):
    print(f"[LOG] {mensagem}")
    # Poderia salvar em um arquivo de log aqui para um histórico mais persistente
    time.sleep(0.5)

def escolher_opcao(opcoes, prompt="Escolha uma opção:"):
    while True:
        print(f"\n{prompt}")
        for i, opcao in enumerate(opcoes):
            print(f"  [{i+1}] {opcao}")
        
        escolha = input("Sua escolha: ").strip()
        if escolha.isdigit():
            escolha_num = int(escolha)
            if 1 <= escolha_num <= len(opcoes):
                return escolha_num
        print("Opção inválida. Por favor, escolha um número da lista.")
        time.sleep(1)

def exibir_barra_vida(personagem):
    vida_atual = personagem.vida
    vida_maxima = personagem.vida_maxima
    porcentagem = (vida_atual / vida_maxima) * 100
    barras_cheias = int(porcentagem // 10)
    barras_vazias = 10 - barras_cheias
    
    barra = "█" * barras_cheias + "░" * barras_vazias
    print(f"  {personagem.nome}: [{barra}] {vida_atual}/{vida_maxima} HP")
    
def exibir_barra_mana(personagem):
    if hasattr(personagem, 'mana'): # Verifica se o personagem tem mana (ex: Heroi)
        mana_atual = personagem.mana
        mana_maxima = personagem.mana_maxima
        porcentagem = (mana_atual / mana_maxima) * 100
        barras_cheias = int(porcentagem // 10)
        barras_vazias = 10 - barras_cheias
        
        barra = "🔵" * barras_cheias + "⚪" * barras_vazias
        print(f"  {personagem.nome}: [{barra}] {mana_atual}/{mana_maxima} MP") 
        