from FlowField import FlowField
from Vehicle import Vehicle

debug = True
flowfield = FlowField(20)
vehicles = []


def setup():
    size(640, 360)

    # Make a whole bunch of vehicles with random maxspeed and maxforce values
    for i in range(120):
        vehicles.append(Vehicle(PVector(random(width), random(height)), random(2, 5), random(0.1, 0.5)));
    

def draw():
  background(255);
  # Display the flowfield in "debug" mode
  if (debug): flowfield.display()
  # Tell all the vehicles to follow the flow field
  for v in vehicles:
    v.follow(flowfield)
    v.run()
  

  # Instructions
  fill(0)
  text("Hit space bar to toggle debugging lines.\nClick the mouse to generate a new flow field.",10,height-20);



def keyPressed():
    global debug
    if (key == ' ') :
        debug = not debug
  



def mousePressed():
    flowfield.init()
