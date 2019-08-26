

class Boxes():
    from collections import Counter

    def __init__(self, an, bn, xl, yl, x_start, y_start, board):
        self.board = board
        self.an, self.bn = an, bn
        self.data_matrix = [[0 for b in range(bn)] for a in range(an)]
        places = []
        for i in range(an):
            for j in range(bn):
                places.append((i, j))
        while len(places) > 0:
            val = int(random(10))
            
            ind1 = int(random(len(places)))
            p1x, p1y = places[ind1]
            self.data_matrix[p1x][p1y] = val
            del places[ind1]
            
            ind2 = int(random(len(places)))
            p2x, p2y = places[ind2]
            self.data_matrix[p2x][p2y] = val
            del places[ind2]
            
            
            
            self.data_matrix[p2x][p2y] = val
            
        self.yn = len(self.data_matrix[0]) # n of grids
        self.xn = len(self.data_matrix)
        self.xl = xl # one grid's len
        self.yl = yl
        self.x_start = x_start
        self.y_start = y_start
        self.pressed = 0
        self.pressed_x , self.pressed_y = 0, 0
        self.show_line_time = 0
        self.pressed_xys = []
        self.show_polyline_time = 0
        self.polyline = []
        self.turns_limit = 1
    
    # Make new Matrix, true means blocked
        self.new_matrix = [[False]*(self.bn+2) for a in range(self.an+2)] 
        for i in range(1, self.an+1):
            for j in range(1, self.bn+1):
                self.new_matrix[i][j] = True
        #self.print_matrix(self.new_matrix)
        
        
    def n_to_pixel(self, xn, yn, xbias, ybias):
        return self.x_start+self.xl*(xn+xbias), self.y_start+self.yl*(yn + ybias)
        
    def show_polyline(self):
        for a, b in zip(self.polyline[:-1], self.polyline[1:]):
            ax, ay = self.n_to_pixel(a[0], a[1], -0.5, -0.5)
            bx, by = self.n_to_pixel(b[0], b[1], -0.5, -0.5)
            stroke(30, 30, 90)
            strokeWeight(5)
            line(ax, ay, bx, by)
            
            
        
    def draw(self):
        noStroke()
        for xi in range(self.xn):
            for yi in range(self.yn):
                if self.new_matrix[xi+1][yi+1]:
                    fill(100*self.data_matrix[xi][yi]/10, 20, 90)
                    xp, yp = self.n_to_pixel(xi, yi, 0.1, 0.1)
                    rect(xp, yp, self.xl*0.8, self.yl*0.8, self.xl*0.1)
                    fill(0)
                    textSize(self.xl*0.6)
                    xp, yp = self.n_to_pixel(xi, yi, 0.3, 0.7)
                    text(self.data_matrix[xi][yi], xp, yp)
        if self.pressed>0:
            self.pressed -= 1
            fill(0, 30)
            xp, yp = self.n_to_pixel(self.pressed_x, self.pressed_y, 0.1, 0.1)
            rect(xp, yp, self.xl*0.8, self.yl*0.8, self.xl*0.1)
        if self.show_line_time>0:
            self.show_line_time -= 1
            tline = self.show_line
            stroke(90, 30, 90)
            strokeWeight(5)
            # line(tline[0], tline[1], tline[2], tline[3])
        if self.show_polyline_time>0:
            self.show_polyline_time -=1
            self.show_polyline()

    def print_matrix(self, m):
        n = len(m[0])
        for ni in range(n):
            for l in m:
                if l[ni]==True:
                    print '0 ',
                else:
                    print '1 ',
            print(' ')

    def process_2_button(self):
        from copy import deepcopy
        (nx1, ny1), (nx2, ny2) =  self.pressed_xys
        if self.data_matrix[nx1][ny1] != self.data_matrix[nx2][ny2]:
            return
        x1, y1 = self.n_to_pixel(nx1, ny1, 0.5, 0.5)
        x2, y2 = self.n_to_pixel(nx2, ny2, 0.5, 0.5)
        self.show_line_time = 15
        self.show_line = (x1, y1, x2, y2)
        
        # GO ON, the following will appear amazing axis changes
        nx1 += 1; ny1 += 1; nx2 += 1; ny2 += 1;
        
        D = [(nx1, ny1)]  # before points
        bef_direct = None
        turns = 0
        Q = [((nx1, ny1), self.new_matrix, D, bef_direct, turns)]  # queue
        nears_plus = ((0, 1), (0, -1), (1, 0), (-1, 0))
        find_flag = False
        while Q:
            (tx, ty), M, D, bef_direct, turns = Q.pop()
            if len(Q)>100:
                break            
            for direct, (px, py) in enumerate(nears_plus):
                try:
                    new_tx = px + tx
                    new_ty = py + ty
                    if turns <= self.turns_limit:
                        new_turns = turns
                        if bef_direct:
                            if direct != bef_direct: new_turns = turns+1
                        
                        if (new_tx, new_ty) == (nx2, ny2):
                            D.append((nx2, ny2))
                            print(frameCount, "Find Path")
                            self.new_matrix[nx1][ny1] = False
                            self.new_matrix[nx2][ny2] = False
                            self.show_polyline_time = 15
                            self.polyline = D 
                            self.board.a_get_score()
                            find_flag = True
                        if M[new_tx][new_ty] == False and new_tx>=0 and new_ty>=0:
                            M2 = deepcopy(M)
                            M2[tx][ty] = True
                            D2 = deepcopy(D)
                            D2.append((new_tx, new_ty))
                            Q.append(((new_tx, new_ty), M2, D2, direct, new_turns))
                except IndexError:
                    pass
            if find_flag: break
        else:
            print(frameCount, "no")          
            
        
                                                    
    def parse_button(self, bx, by):
        if len(self.pressed_xys) >= 2:
            self.pressed_xys = []
        self.pressed_x = int(round( (bx - self.x_start)/self.xl ))
        self.pressed_y = int(round( (by - self.y_start)/self.yl ))
        if 0<= self.pressed_x < self.xn and 0<= self.pressed_y < self.yn:
            self.pressed = 15
            
        self.pressed_xys.append((self.pressed_x, self.pressed_y))
        if len(self.pressed_xys) >= 2:
            self.process_2_button()
        
