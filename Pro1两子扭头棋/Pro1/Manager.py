class Manager():
    
    
    def __init__(self, a, b, board):
        self.a = a
        self.b = b
        self.board = board
        self.turn = True
        self.dd = {'s':(0, 1), 'w':(0, -1), 'a':(-1, 0), 'd':(1, 0), 'k':(0, 1), 'i':(0, -1), 'j':(-1, 0), 'l':(1, 0)}
        self.restart = False
        
        
    def draw(self):
        self.a.draw()
        self.b.draw()
        self.board.draw()
        
    def get(self, k):
        try:
            tmp = PVector(*self.dd[k])
        except KeyError:
            return
                
        if self.turn:
            if k in 'asdw':
                self.a.move(tmp)
                if self.a.p == self.b.p:
                    print("A is the winner!")
                    self.board.a_get_score()
                    self.restart = True
                self.turn = not self.turn
            
        else: # b's turn
            if k in 'jkli':
                self.b.move(tmp)
                if self.a.p == self.b.p:
                    print("B is the winner!")
                    self.board.b_get_score()
                    self.restart = True
                self.turn = not self.turn
