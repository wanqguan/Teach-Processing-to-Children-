add_library('geomerative')


from itertools import chain, cycle



def setup():
    global points
    size(1600,600)
    RG.init(this)
    my_text = "CAAS"
    grp = RG.getText(my_text, "FreeSans.ttf", 400, CENTER)
    
    
    background(255)
    
    points = []
    for i in range(len(my_text)):
        points.extend(grp.children[i].getPoints())


    noFill()
    #fill(10)
    stroke(87, 214, 227, 200)

    w = 8
    h = 8
    max_dis = 30
    for i in range(width/w):
        for k in range(height/h):
            dis = max_dis
            for p in points:
                dis = min(dis, dist(w*i, h*k, p.x+width/2, p.y+height/2+100))
            #circle(w*i, h*k, dis)
            rect(w*i, h*k, dis, dis)
            
def draw():
    pass





        
            



        
        
