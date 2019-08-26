class Board():
    
    
    def __init__(self):
        self.an = 0
        self.bn = 0
        
    def a_get_score(self):
        self.an += 1
        

        
    def draw(self):
        fill(50, 100, 200)
        k = 60
        text("a's score:", 410, k)
        text(str(self.an), 410, 2*k)
