#!/usr/bin/python
#ball collisions using class
#try to optimise the collision detecting algorithm

import turtle, time, math, random

N = int(input('Number of balls: '))
CoefficientOfRestitution = 1

window = turtle.Screen()
window.tracer(0,0)

width = window.window_width()
height = window.window_height()

colors = ['red', 'blue', 'green', 'yellow', 'orange', 'black', 'purple', 'lightblue', 'pink']
balls = [] #store ball objects as dictionary
starting_posns = []

class Ball(turtle.Turtle):
    def __init__(self, color, v_x, v_y):
        #global balls
        turtle.Turtle.__init__(self)
        self.penup()
        self.color(color)
        self.shape("circle")

        self.velocity = [v_x, v_y]
        self.new_coordinates = [0,0]
        self.SPEED = 5 #choose values later
        #perhaps will use later, keep default for now
        self.mass = 1
        self.radius = 10
        self.hit_boundary = False
        self.collided = False
    
    '''
    Methods for momentum are added because I think it might me useful to adjust the directions after the balls have collided.
    '''
    def total_momentum(self):
        return self.mass * (math.sqrt(self.v_x ** 2 + self.v_y ** 2))

    def x_momentum(self):
        return self.mass * self.v_x

    def y_momentum(self):
        return self.mass * self.v_y

    def distance(self):
        global width, height
        return math.sqrt((self.xcor() + width / 2) ** 2 + (self.ycor() + height / 2) ** 2)

    def calculate_new_coordinates(self):
        # normalise velocity component then mult by SPEED
        magnitude = math.sqrt(self.velocity[0]**2 + self.velocity[1]**2)
        if magnitude != 0:
            a = self.SPEED/magnitude
            self.new_coordinates[0] = self.xcor() + a*self.velocity[0]
            self.new_coordinates[1] = self.ycor() + a*self.velocity[1]
        else:
            self.new_coordinates[0] = self.xcor() + self.velocity[0]
            self.new_coordinates[1] = self.ycor() + self.velocity[1]

    def move_ball(self):
        self.goto(self.new_coordinates[0], self.new_coordinates[1])

    def change_size(self):
        self.shapesize(self.radius/10)

'''
#make border
border = turtle.Turtle()
border.hideturtle()
border.speed(0)
border.pensize(3)
border.penup()
border.goto(-width/2,-height/2)
border.pendown()
for i in range(2):
    border.forward(width)
    border.left(90)
    border.forward(height)
    border.left(90)
'''

#check boundary
def checkboundary(screen, ball, e=1/2):
    '''
    Check the collision between a ball and boundaries.
    If there is a collision, move the ball to corresponding direction according to physical laws.
    '''
    width, height = screen.window_width(), screen.window_height()
    ball.hit_boundary = False
    ball.calculate_new_coordinates()
    x = ball.new_coordinates[0]  #save writing this again
    y = ball.new_coordinates[1]
    r = ball.radius + 1 #(+ padding)
    if x+r > width/2 or x-r < -width/2:
        ball.velocity[0] = -e*ball.velocity[0]
        ball.calculate_new_coordinates()
        ball.hit_boundary = True
        return True

    if y+r > height/2 or y-r < -height/2:
        ball.velocity[1] = -e*ball.velocity[1]
        ball.calculate_new_coordinates()
        ball.hit_boundary = True
        return True
    else:
        return False

def check_ball_collision(ball1, ball2, e=1/2):
    '''
    Check the collision between two balls.
    If there is a collision, move the two balls to corresponding directions.
    The motion is not realistic. Still working on it.
    '''
    #global balls
    dx = (ball2.new_coordinates[0] - ball1.new_coordinates[0])
    dy = (ball2.new_coordinates[1] - ball1.new_coordinates[1])
    distance = math.sqrt(dx**2 + dy**2)
    R = ball1.radius + ball2.radius ###
    u1x = ball1.velocity[0]
    u1y = ball1.velocity[1]
    u2x = ball2.velocity[0]
    u2y = ball2.velocity[1]

    if distance <= R:
        ball1.SPEED, ball2.SPEED = e * ball2.SPEED, e * ball1.SPEED
        ball1.velocity = [(2 * ball2.mass * u2x + u1x * (ball1.mass - ball2.mass)) / (ball1.mass + ball2.mass), (2 * ball2.mass * u2y + u1y * (ball1.mass - ball2.mass)) / (ball1.mass + ball2.mass)]
        ball2.velocity = [(2 * ball1.mass * u1x + u2x * (ball2.mass - ball1.mass)) / (ball1.mass + ball2.mass), (2 * ball1.mass * u1y + u2y * (ball2.mass - ball1.mass)) / (ball1.mass + ball2.mass)]
        ball1.calculate_new_coordinates()
        ball2.calculate_new_coordinates()
        return True
    else:
        return False

def check_distance(a,b):
    '''Distances between two coordinates a and b'''
    dx = a[0]-b[0]
    dy = a[1]-b[1]
    return math.sqrt(dx**2 + dy**2)

       
def gen_random_start():
    x = random.randint(-(width/2)+15, (width/2)-15)
    y = random.randint(-(height/2)+15, (height/2)-15)
    return [x, y]

def generating_balls(n):
    while len(balls) < n:
        vx, vy = 0, 0
        while vx * vy == 0:
            vx = random.randint(-5, 5)
            vy = random.randint(-5, 5)
        color = colors[random.randint(0, len(colors) - 1)]
        balls.append(Ball(color, vx, vy))
        
    while len(starting_posns) < n:
        unique = True
        coordinates = gen_random_start()
        for i in starting_posns:
            if check_distance(i, coordinates) < 25:
                unique = False
                continue
        if unique:
            starting_posns.append(coordinates)

    for i in range(len(balls)):
        balls[i].setposition(starting_posns[i])
        coordinates = starting_posns[i]
        if coordinates[0] > 0 and coordinates[1] > 0:
            balls[i].color('red')
        elif coordinates[0] > 0 and coordinates[1] < 0:
            balls[i].color('blue')
        elif coordinates[0] < 0 and coordinates[1] > 0:
            balls[i].color('green')
        else:
            balls[i].color('yellow')

def quicksort(array):
    '''
    Sort the balls in the order of their distance to the imagined origin.
    '''
    if len(array) < 2:
        return array

    pivot = array[-1]
    i = 0
    j = len(array) - 1

    while i < j:
        if array[i].distance() <= pivot.distance():
            i += 1
        elif array[i].distance() > pivot.distance():
            array.insert(-1, array.pop(i))
            j -= 1
    return quicksort(array[:j]) + [pivot] + quicksort(array[j:len(array) - 1])

def insertsort(array):
    '''
    Another way to sort.
    It may have better performance than quicksort().
    '''
    for i in range(1, len(array)):
        key = array.pop(i)
        j = i
        while j > 0 and array[j - 1].distance() > key.distance():
            j -= 1
        array.insert(j, key)
    return array

###check initial posns
min_d = 100
def check_initial_positions():
    global starting_posns
    min_d = 100
    for c in balls:#combinations:
        r = check_distance(starting_posns[c - 1],starting_posns[c[1]-1])
        if r < min_d:
            min_d = r
    return min_d

# generate N balls
generating_balls(N)

def iterative_checking(ball):
    index = balls.index(ball)
    i = index + 1
    count = 0
    while balls[i].distance() - ball.distance() <= ball.radius + balls[i].radius:
        if check_ball_collision(ball, balls[i], CoefficientOfRestitution):
            count += 1
        if i + 1 < len(balls):
            i += 1
        else:
            break
    return count

while True:
    insertsort(balls)
    
    CollisionCount = 0
    for ball in balls:
        ball.calculate_new_coordinates()
        if checkboundary(window, ball, CoefficientOfRestitution):
            CollisionCount += 1

    
    for i in range(0, len(balls) - 1):
        if balls[i + 1].distance() - balls[i].distance() < 50:#balls[i + 1].radius + balls[i].radius:
            CollisionCount += iterative_checking(balls[i])

        else:
            pass

    for i in balls:
        i.move_ball()
    print(sum((i.SPEED for i in balls)) / N, CollisionCount)
    window.update()
    time.sleep(1 / 60)
