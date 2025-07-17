import time
from personagem import Personagem

class Heroi(Personagem):
    def __init__(self, nome, vida, ataque, defesa, mana, classe):
        super().__init__(nome, vida, ataque, defesa)
        self.mana = mana
        self.mana_maxima = mana
        self.classe = classe
        self.xp = 0
        self.nivel = 1
        self.inventario = [] # Lista de itens
        # Habilidades específicas do herói (ex: ataque_forte, cura)
        self.habilidades['Ataque Forte'] = {'custo': 5, 'dano': 10}
        self.habilidades['Curar'] = {'custo': 8, 'cura': 15}

    def ganhar_xp(self, quantidade_xp):
        self.xp += quantidade_xp
        print(f"✨ {self.nome} ganhou {quantidade_xp} de XP! Total: {self.xp}")
        time.sleep(1)
        self._verificar_nivel()

    def _verificar_nivel(self):
        xp_para_proximo_nivel = self.nivel * 20 # Exemplo de progressão
        if self.xp >= xp_para_proximo_nivel:
            self.nivel += 1
            self.vida_maxima += 10 # Aumenta vida ao subir de nível
            self.vida = self.vida_maxima # Cura completa ao subir de nível
            self.ataque += 2
            self.defesa += 1
            self.mana_maxima += 5
            self.mana = self.mana_maxima
            print(f"\n🎉 PARABÉNS! {self.nome} subiu para o NÍVEL {self.nivel}!")
            self.mostrar_status()
            time.sleep(2)
            print("  Seus atributos melhoraram!")

    def usar_habilidade(self, nome_habilidade, alvo=None):
        if nome_habilidade not in self.habilidades:
            print(f"  {self.nome} não possui a habilidade '{nome_habilidade}'.")
            time.sleep(1)
            return False

        habilidade_info = self.habilidades[nome_habilidade]
        custo = habilidade_info.get('custo', 0)

        if self.mana < custo:
            print(f"  ❌ {self.nome} não tem mana suficiente para usar '{nome_habilidade}'. Mana atual: {self.mana}/{self.mana_maxima}")
            time.sleep(1)
            return False

        self.mana -= custo
        print(f"✨ {self.nome} usa '{nome_habilidade}'! Mana restante: {self.mana}/{self.mana_maxima}")
        time.sleep(1)

        if nome_habilidade == 'Ataque Forte':
            dano_extra = habilidade_info.get('dano', 0)
            dano_total = self.ataque + dano_extra
            if alvo:
                print(f"  Causando {dano_total} de dano extra!")
                alvo.sofrer_dano(dano_total)
            else:
                print("  Erro: Habilidade 'Ataque Forte' requer um alvo.")
            return True
        elif nome_habilidade == 'Curar':
            cura = habilidade_info.get('cura', 0)
            self.vida = min(self.vida_maxima, self.vida + cura)
            print(f"  {self.nome} se curou em {cura} pontos. Vida atual: {self.vida}/{self.vida_maxima}")
            return True
        # Adicione mais habilidades aqui!
        return False

    def adicionar_item(self, item):
        self.inventario.append(item)
        print(f"🎒 {self.nome} pegou um(a) {item['nome']}!")
        time.sleep(1)

    def usar_item(self, nome_item):
        for item in self.inventario:
            if item['nome'].lower() == nome_item.lower():
                self.inventario.remove(item)
                print(f"🎒 {self.nome} usou {item['nome']}.")
                time.sleep(1)
                # Aplica o efeito do item
                if item['tipo'] == 'pocao_vida':
                    self.vida = min(self.vida_maxima, self.vida + item['efeito'])
                    print(f"  {self.nome} recuperou {item['efeito']} de vida. Vida atual: {self.vida}/{self.vida_maxima}")
                elif item['tipo'] == 'pocao_mana':
                    self.mana = min(self.mana_maxima, self.mana + item['efeito'])
                    print(f"  {self.nome} recuperou {item['efeito']} de mana. Mana atual: {self.mana}/{self.mana_maxima}")
                return True
        print(f"  ❌ {self.nome} não tem '{nome_item}' no inventário.")
        time.sleep(1)
        return False

    def mostrar_inventario(self):
        if not self.inventario:
            print(f"  {self.nome} não tem itens no inventário.")
            return
        print(f"\n--- Inventário de {self.nome} ---")
        for item in self.inventario:
            print(f"  - {item['nome']} ({item['tipo'].replace('_', ' ').title()})")
        print("----------------------------")
        time.sleep(1) 
        