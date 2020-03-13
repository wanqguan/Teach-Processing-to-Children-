add_library('geomerative')


from itertools import chain, cycle



def setup():
    global iter
    my_text = "YEAR"
    # Initilaize the sketch
    size(1500,800)
    RG.init(this)
    grp = RG.getText(my_text, "FreeSans.ttf", 500, CENTER)
    
    
    background(255)
    frameRate(200)
    fill(255, 102, 0)
    colorMode(HSB)
    points = [0]*len(my_text)
    for i in range(len(my_text)):
        points[i] = grp.children[i].getPoints()
    iter = iter_points(points)
    iter = cycle(iter)


def iter_points(points):
    tiao = 3
    ceng = 10
    c = 0
    for letter_i in range(len(points)):
        ps = points[letter_i][1:-1:tiao]
        for k in range(1, ceng):
            for p1, p2 in zip(ps, chain(ps[k:-1], ps[0:k])):
                x1, y1 = p1.x, p1.y
                x2, y2 = p2.x, p2.y
                
                c += 0.1
                if c >= 255: c = 0
                yield x1+width/2, y1+height/2, x2+width/2, y2+height/2, c


def draw():
    x1, y1, x2, y2, c = iter.next()
    stroke(c, 200, 200, 130)
    line(x1, y1, x2, y2)
    



        
            



        
        
