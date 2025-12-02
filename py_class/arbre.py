import math
from py_class.node import Node

class Arbre:
    def __init__(self, market, contract, n_steps: int):
        self.market = market
        self.contract = contract
        self.n_steps = n_steps
        self.dt = self.contract.maturity / n_steps
        self.alpha = math.exp(self.market.sigma * math.sqrt(3 * self.dt))
        self.racine = None
        self._generer_arbre(n_steps)

    def is_dividend(self, step: int) -> bool:
        if self.market.div_date is None:
            return False
        t_start = step * self.dt
        t_end = (step + 1) * self.dt
        div_date = (self.market.div_date - self.contract.pricing_date).days / 365.0
        return t_start < div_date <= t_end

    def _generer_arbre(self, N: int):
        S0 = self.market.stock_price
        r = self.market.int_rate
        dt = self.dt
        self.racine = Node(si=S0, arbre=self)
        noeud_tronc = self.racine

        for k in range(N):
            if k == 18:
                print('tesrt')


            if self.is_dividend(k):
                D = self.market.div 
                print (f'div {D}, {k}')
            else:
                D = 0
            noeud_a_traiter = noeud_tronc
            forward_val = noeud_tronc.si * math.exp(r * dt) - D
            last_next_mid = Node(si=forward_val, arbre=self)
            noeud_next_up_memory=last_next_mid


            while noeud_a_traiter is not None:
                forward = noeud_a_traiter.si * math.exp(r * dt) - D
                last_next_mid = noeud_a_traiter.set_next_mid(forward,noeud_next_up_memory, D)
                noeud_a_traiter = noeud_a_traiter.voisin_up
                noeud_next_up_memory=last_next_mid.voisin_up

            noeud_a_traiter = noeud_tronc.voisin_down
            last_next_mid = noeud_tronc.next_mid


            noeud_next_down_memory=last_next_mid.voisin_down

            while noeud_a_traiter is not None:
                forward = noeud_a_traiter.si * math.exp(r * dt) - D
                last_next_mid = noeud_a_traiter.set_next_mid(forward,noeud_next_down_memory, D)
                noeud_a_traiter = noeud_a_traiter.voisin_down
                noeud_next_down_memory = last_next_mid.voisin_down

            noeud_tronc = noeud_tronc.next_mid
