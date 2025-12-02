import math as m

class Node:
    def __init__(self, si, arbre, voisin_up=None, voisin_down=None,
                 p_up=None, p_down=None, p_mid=None):
        
        self.si = si
        self.arbre = arbre
        self.voisin_up = voisin_up
        self.voisin_down = voisin_down
        self.p_up = p_up
        self.p_down = p_down
        self.p_mid = p_mid
        self.next_up = None
        self.next_down = None
        self.next_mid = None
        self.voisin_behind = None
        self.si2 = None

    def move_up(self, alpha):
        if not self.voisin_up:
            self.voisin_up = Node(self.si * alpha, arbre=self.arbre)
            self.voisin_up.voisin_down = self
        return self.voisin_up

    def move_down(self, alpha):
        if not self.voisin_down:
            self.voisin_down = Node(self.si / alpha, arbre=self.arbre)
            self.voisin_down.voisin_up = self
        return self.voisin_down

    def compute_probabilities(self, D=0):
        r = self.arbre.market.int_rate
        dt = self.arbre.dt
        alpha = self.arbre.alpha
        sigma = self.arbre.market.sigma
        esp = self.si * m.exp(r * dt) - D
        var = (self.si ** 2) * m.exp(2 * r * dt) * (m.exp((sigma ** 2) * dt) - 1)
        nmv = self.next_mid.si

        numer = (1 / nmv ** 2) * (var + esp ** 2) - 1 - (alpha + 1) * ((1 / nmv) * esp - 1)
        denom = (1 - alpha) * ((1 / alpha ** 2) - 1)
        self.p_down = numer / denom

        numer_up = (1 / nmv) * esp - 1 - ((1 / alpha) - 1) * self.p_down
        denom_up = alpha - 1
        self.p_up = numer_up / denom_up
        self.p_mid = 1 - self.p_up - self.p_down





    def set_next_mid(self,forward,noeud_next_up_memory, D=0):
        alpha = self.arbre.alpha

        # IL FAUT CHANGER ICI LA CONSTRUCTION
        #self.next_mid = Node.find_next_mid(forward, alpha, last_next_mid)

        self.next_mid = self.find_next_mid(forward, alpha, noeud_next_up_memory)


        self.next_mid.voisin_behind = self
        self.next_up = self.next_mid.move_up(alpha)
        self.next_down = self.next_mid.move_down(alpha)
        self.compute_probabilities(D)
        return self.next_mid

    @staticmethod
    def find_next_mid(forward, alpha, start_node):
        node = start_node
        while forward > node.si * (1 + alpha) / 2:
            node = node.move_up(alpha)
        while forward <= node.si * (1 + 1 / alpha) / 2:
            if forward < 0:
                break
            node = node.move_down(alpha)
        return node