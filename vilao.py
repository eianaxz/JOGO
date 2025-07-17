import time
from personagem import Personagem

class Vilao(Personagem):
    def __init__(self, nome, vida, ataque, defesa, recompensa_xp, fala_ameaca):
        super().__init__(nome, vida, ataque, defesa)
        self.recompensa_xp = recompensa_xp
        self.fala_ameaca = fala_ameaca
        self.habilidades['Ameaçar'] = self._ameacar # Adiciona uma habilidade específica

    def apresentar_ameaca(self):
        print(f"\n💀 {self.nome}: \"{self.fala_ameaca}\"")
        time.sleep(2)

    def _ameacar(self, alvo):
        print(f"💀 {self.nome} ameaça {alvo.nome}, diminuindo sua moral!")
        # Exemplo de efeito: diminuir temporariamente a defesa do herói
        alvo.defesa = max(0, alvo.defesa - 2) # Reduz 2 de defesa
        print(f"  A defesa de {alvo.nome} foi reduzida temporariamente para {alvo.defesa}.")
        time.sleep(1.5)

    def usar_habilidade_vilao(self, habilidade_nome, alvo):
        if habilidade_nome in self.habilidades:
            self.habilidades[habilidade_nome](alvo)
        else:
            print(f"  {self.nome} não possui a habilidade '{habilidade_nome}'.")
        time.sleep(1) 
        