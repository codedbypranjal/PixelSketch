import turtle

# Read drawing map profiles
with open("detailed_strokes.txt", "r") as file:
    lines = file.readlines()

# Parse the canvas parameters row to handle scaling offsets accurately
dimension_line = lines[0].strip().split(" ")
canvas_w, canvas_h = map(int, dimension_line[1].split(","))

# 1. Initialize Proportional Canvas Environment
screen = turtle.Screen()
screen.setup(canvas_w + 80, canvas_h + 80)  # Dynamic window allocation with buffer borders
screen.bgcolor("#F6F6F6")  # Textured off-white tone
screen.colormode(1.0)

pen = turtle.Turtle()
turtle.hideturtle()
pen.shape("turtle")
pen.speed(0)
pen.pensize(2)  # Thin enough to highlight small intersecting details

# Controls drawing render rates.
# complex areas, or down to 2-3 to see individual stroke movements.
turtle.tracer(12, 1)

# Sequential stroke drawing loop:   
is_drawing_stroke = False

for line in lines[1:]:
    line = line.strip()
    if not line:
        continue

    if line.startswith("STROKE"):
        _, color_str = line.split(" ")
        r, g, b = map(float, color_str.split(","))

        pen.pencolor(r, g, b)
        pen.penup()
        is_drawing_stroke = True

    elif line == "END_STROKE":
        pen.penup()
        is_drawing_stroke = False

    else:
        x_str, y_str = line.split(",")
        x = float(x_str)
        y = float(y_str)
        # Subtracting half the height/width accurately centers any custom rectangular picture.
        turtle_x = x - (canvas_w / 2)
        turtle_y = -y + (canvas_h / 2)

        if is_drawing_stroke:
            pen.goto(turtle_x, turtle_y)
            pen.pendown()
            is_drawing_stroke = False
        else:
            pen.goto(turtle_x, turtle_y)

# Finalize layout composition updates
turtle.update()
turtle.done()