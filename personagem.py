import time

class Personagem:
    def __init__(self, nome, vida, ataque, defesa):
        self.nome = nome
        self.vida = vida
        self.ataque = ataque
        self.defesa = defesa
        self.vida_maxima = vida # Para poções ou curas
        self.habilidades = {} # Dicionário para habilidades básicas

    def esta_vivo(self):
        return self.vida > 0

    def sofrer_dano(self, dano):
        dano_real = max(0, dano - self.defesa) # Dano nunca é negativo
        self.vida -= dano_real
        if self.vida < 0:
            self.vida = 0
        print(f"  {self.nome} sofreu {dano_real} de dano. Vida restante: {self.vida}/{self.vida_maxima}")
        time.sleep(0.5)

    def atacar(self, alvo):
        print(f"\n⚡ {self.nome} ataca {alvo.nome}!")
        time.sleep(1)
        dano_causado = self.ataque # Pode ser modificado por habilidades ou buffs
        alvo.sofrer_dano(dano_causado)

    def mostrar_status(self):
        print(f"--- Status de {self.nome} ---")
        print(f"  Vida: {self.vida}/{self.vida_maxima}")
        print(f"  Ataque: {self.ataque}")
        print(f"  Defesa: {self.defesa}")
        print("----------------------------")
        time.sleep(0.5)

    def dialogar(self, outro_personagem, mensagem):
        print(f"\n💬 {self.nome} diz para {outro_personagem.nome}: \"{mensagem}\"")
        time.sleep(1.5) 
        