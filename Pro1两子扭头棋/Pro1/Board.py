class Board():
    
    
    def __init__(self):
        self.an = 0
        self.bn = 0
        
    def a_get_score(self):
        self.an += 1
        
    def b_get_score(self):
        self.bn += 1
        
    def draw(self):
        fill(300, 100, 200)
        k = 60
        text("a's score:", 610, k)
        text(str(self.an), 610, 2*k)
        text("b's score:", 610, 4*k)
        text(str(self.bn), 610, 5*k)
