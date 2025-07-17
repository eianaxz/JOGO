import time
import random
from personagem import Personagem
from heroi import Heroi
from vilao import Vilao
from utils import limpar_tela, pausar, imprimir_titulo, imprimir_log, escolher_opcao, exibir_barra_vida, exibir_barra_mana

def menu_principal():
    imprimir_titulo("BEM-VINDO AO DESAFIO 🕹️ Improve This Game 🕹️")
    print("\nEscolha o que deseja fazer:")
    opcoes = ["Iniciar Nova Aventura", "Sair do Jogo"]
    escolha = escolher_opcao(opcoes)
    return escolha

def criar_personagens():
    imprimir_titulo("ESCOLHA SEU HERÓI!")
    heroi_nome = input("Digite o nome do seu herói: ").strip()
    print("\nEscolha a classe do seu herói:")
    opcoes_classe = ["Guerreiro (Mais vida e ataque)", "Mago (Mais mana e habilidades)", "Ladino (Mais defesa e agilidade)"]
    escolha_classe_num = escolher_opcao(opcoes_classe)
    
    if escolha_classe_num == 1:
        heroi = Heroi(heroi_nome, 120, 15, 10, 30, "Guerreiro")
        heroi.habilidades['Investida'] = {'custo': 7, 'dano': 12}
    elif escolha_classe_num == 2:
        heroi = Heroi(heroi_nome, 90, 10, 5, 60, "Mago")
        heroi.habilidades['Bola de Fogo'] = {'custo': 10, 'dano': 18}
        heroi.habilidades['Escudo Arcano'] = {'custo': 5, 'defesa_extra': 5}
    else:
        heroi = Heroi(heroi_nome, 100, 12, 12, 40, "Ladino")
        heroi.habilidades['Ataque Furtivo'] = {'custo': 6, 'dano': 15}

    print(f"\n🎉 Você criou o(a) {heroi.classe} {heroi.nome}!")
    heroi.mostrar_status()
    exibir_barra_mana(heroi)
    pausar()
    return heroi

def gerar_vilao_aleatorio(nivel_heroi):
    vilao_tipos = {
        "Goblin": {"vida": 40, "ataque": 8, "defesa": 3, "xp": 10, "fala": "Grrr... vou te pegar!"},
        "Orc": {"vida": 70, "ataque": 12, "defesa": 5, "xp": 20, "fala": "MORRA, INTRUSO!"},
        "Esqueleto Mago": {"vida": 50, "ataque": 10, "defesa": 4, "xp": 15, "fala": "Seu fim está próximo!"},
        "Dragão Juvenil": {"vida": 150, "ataque": 25, "defesa": 10, "xp": 50, "fala": "ROOOOAAAR!"}
    }
    indice = min((nivel_heroi - 1) // 2, len(vilao_tipos) - 1)
    nome = list(vilao_tipos.keys())[indice]
    dados = vilao_tipos[nome]
    return Vilao(
        nome=nome,
        vida=dados["vida"] + (nivel_heroi * 5),
        ataque=dados["ataque"] + (nivel_heroi * 2),
        defesa=dados["defesa"] + (nivel_heroi * 1),
        recompensa_xp=dados["xp"] + (nivel_heroi * 3),
        fala_ameaca=dados["fala"]
    )

def evento_mercador(heroi):
    escolha = escolher_opcao(
        ["Aceitar Oferta (Perder 5 XP)", "Recusar Oferta"],
        "O mercador te oferece uma Poção de Mana. O que você faz?"
    )
    if escolha == 1:
        heroi.adicionar_item({'nome': 'Poção de Mana Pequena', 'tipo': 'pocao_mana', 'efeito': 15})
        heroi.xp = max(0, heroi.xp - 5)
    else:
        print("Você recusa a oferta do mercador.")

def evento_descanso(heroi):
    vida_recuperada = min(heroi.vida_maxima - heroi.vida, 15)
    heroi.vida += vida_recuperada
    print(f"{heroi.nome} recuperou {vida_recuperada} de vida.")

def evento_aleatorio(heroi):
    eventos = [
        {"nome": "Poção Misteriosa", "descricao": "Você encontra uma poção brilhante no chão.",
         "acao": lambda h: h.adicionar_item({'nome': 'Poção de Vida Pequena', 'tipo': 'pocao_vida', 'efeito': 25})},
        {"nome": "Encontro com Mercador", "descricao": "Um mercador misterioso aparece e te oferece algo.",
         "acao": evento_mercador},
        {"nome": "Armadilha", "descricao": "Você pisa em uma armadilha e sofre dano.",
         "acao": lambda h: h.sofrer_dano(10)},
        {"nome": "Descanso Rápido", "descricao": "Você encontra um local seguro para descansar.",
         "acao": evento_descanso},
        {"nome": "Nada Acontece", "descricao": "O caminho segue sem intercorrências.",
         "acao": lambda h: print("Você segue seu caminho tranquilamente.")}
    ]
    evento = random.choice(eventos)
    print(f"\n--- EVENTO: {evento['nome']} ---")
    print(f"Descrição: {evento['descricao']}")
    time.sleep(2)
    evento["acao"](heroi)
    pausar()

def tela_batalha(heroi, vilao):
    imprimir_titulo(f"⚔️ BATALHA: {heroi.nome} vs. {vilao.nome} 💀")
    vilao.apresentar_ameaca()
    pausar()

    while heroi.esta_vivo() and vilao.esta_vivo():
        limpar_tela()
        print(f"--- TURNO DE {heroi.nome} ---")
        exibir_barra_vida(heroi)
        exibir_barra_mana(heroi)
        exibir_barra_vida(vilao)

        print("\nEscolha sua ação:")
        opcoes_acao = ["Atacar", "Usar Habilidade", "Usar Item", "Ver Status", "Fugir (Pode falhar!)"]
        escolha = escolher_opcao(opcoes_acao)

        if escolha == 1:
            heroi.atacar(vilao)
        elif escolha == 2:
            if not heroi.habilidades:
                print("Você não tem habilidades!")
                time.sleep(1)
                continue
            print("\nEscolha a habilidade:")
            nomes = list(heroi.habilidades.keys())
            escolha_hab = escolher_opcao(nomes)
            habilidade = nomes[escolha_hab - 1]
            if heroi.usar_habilidade(habilidade, vilao if habilidade in ['Ataque Forte'] else None):
                imprimir_log(f"{heroi.nome} usou {habilidade}.")
            else:
                continue
        elif escolha == 3:
            heroi.mostrar_inventario()
            if not heroi.inventario:
                pausar()
                continue
            item = input("Digite o nome do item: ").strip()
            if not heroi.usar_item(item):
                continue
        elif escolha == 4:
            heroi.mostrar_status()
            vilao.mostrar_status()
            pausar()
            continue
        elif escolha == 5:
            print(f"{heroi.nome} tenta fugir...")
            time.sleep(1)
            if heroi.defesa > vilao.ataque / 2:
                print("Você conseguiu fugir!")
                return "fugiu"
            else:
                print("A fuga falhou!")
                time.sleep(1)

        if not vilao.esta_vivo():
            imprimir_log(f"{vilao.nome} foi derrotado!")
            heroi.ganhar_xp(vilao.recompensa_xp)
            print("\nVocê venceu a batalha!")
            return "vitoria"

        print(f"\n--- TURNO DE {vilao.nome} ---")
        time.sleep(1)
        if vilao.vida < vilao.vida_maxima * 0.3 and 'Ameaçar' in vilao.habilidades:
            vilao.usar_habilidade_vilao('Ameaçar', heroi)
        else:
            vilao.atacar(heroi)

        if not heroi.esta_vivo():
            imprimir_log(f"{heroi.nome} foi derrotado por {vilao.nome}!")
            print("\nGAME OVER!")
            return "derrota"

        pausar()

    return "fim_inesperado"

def ciclo_jogo(heroi):
    imprimir_titulo("🌎 INÍCIO DA AVENTURA!")
    print(f"O(A) {heroi.nome} embarca em uma jornada perigosa...")
    pausar()

    for i in range(1, 4):
        if not heroi.esta_vivo():
            break
        imprimir_log(f"Caminhando... (Encontro {i})")
        if i % 2 == 0:
            evento_aleatorio(heroi)
        else:
            vilao = gerar_vilao_aleatorio(heroi.nivel)
            resultado = tela_batalha(heroi, vilao)
            if resultado in ["derrota", "fugiu"]:
                break
            elif resultado == "vitoria":
                imprimir_log("Vitória! Seguindo em frente...")
                pausar()

    if heroi.esta_vivo():
        imprimir_titulo("🌟 FIM DA PRIMEIRA JORNADA 🌟")
        print(f"Parabéns, {heroi.nome}! Você sobreviveu!")
        print(f"Nível final: {heroi.nivel} | XP: {heroi.xp}")
    else:
        imprimir_titulo("💀 FIM DE JOGO 💀")
        print("Sua aventura termina aqui. Tente novamente!")

def main():
    while True:
        escolha = menu_principal()
        if escolha == 1:
            heroi = criar_personagens()
            ciclo_jogo(heroi)
            pausar()
        elif escolha == 2:
            print("\nObrigado por jogar! Até a próxima aventura!")
            break

if __name__ == "__main__":
    main()
