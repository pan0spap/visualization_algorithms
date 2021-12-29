import pygame
from dijkstra_new_version import *
from Astar import * 
import json
import tkinter, tkinter.messagebox
from tkinter import filedialog   # για να γινει το save as και το load


pygame.init()

display_width = 1350
display_height = 720
grid_width = 50
grid_height = 50

margin = 5
grid_v = []
array = []

root = tkinter.Tk()
root.withdraw()

set_start = False
set_goal = False
set_block = False
already_set_start = False
already_set_goal = False
path_set = False
clear_cell = False
alg = False

filename = ''


for row in range(13):
    grid_v.append([])
    array.append([])
    for column in range(18):
        grid_v[row].append(0)
        array[row].append(0)


black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
purple = (128, 0, 128)
grey = (128, 128, 128)
orange = (255, 165, 0)

gameDisplay = pygame.display.set_mode((display_width, display_height))  # δημιουργια οθονης
pygame.display.set_caption('Visualization algorithms')  # ορισμος τιτλου οθονης
clock = pygame.time.Clock()


def texts():
    # δημιουργια κειμενου και τοποθετηση στην οθονη
    font = pygame.font.Font('freesansbold.ttf', 30)
    menu_text = font.render('MENU', True, white)
    textRect = menu_text.get_rect()
    textRect.center = ((1170), (display_height / 10))
    gameDisplay.blit(menu_text, textRect)

    # δημιουργια κουμπιων (σχημα και χρωμα)
    pygame.draw.rect(gameDisplay, blue, (1000, 200, 80, 50))
    pygame.draw.rect(gameDisplay, orange, (1260, 200, 80, 50))
    pygame.draw.rect(gameDisplay, green, (1000, 300, 80, 50))
    pygame.draw.rect(gameDisplay, red, (1000, 400, 80, 50))
    pygame.draw.rect(gameDisplay, white, (1000, 500, 80, 50))
    pygame.draw.rect(gameDisplay, purple, (1260, 300, 80, 50))
    pygame.draw.rect(gameDisplay, grey, (1260, 400, 80, 50))
    pygame.draw.rect(gameDisplay, grey, (1260, 500, 80, 50))
    pygame.draw.rect(gameDisplay, grey, (1260, 600, 80, 50))
    pygame.draw.rect(gameDisplay, grey, (1000, 600, 80, 50))
    pygame.draw.rect(gameDisplay, grey, (1130, 600, 80, 50))

    font = pygame.font.Font('freesansbold.ttf', 18)
    Astar_text = font.render('A*', True, black)
    textRect = Astar_text.get_rect()
    textRect.center = ((1000 + (80/2)), (200 + (50 / 2)))
    gameDisplay.blit(Astar_text, textRect)

    font = pygame.font.Font('freesansbold.ttf', 18)
    dijkstra_text = font.render('Dijkstra', True, black)
    textRect = dijkstra_text.get_rect()
    textRect.center = ((1260 + (80 / 2)), (200 + (50 / 2)))
    gameDisplay.blit(dijkstra_text, textRect)

    font = pygame.font.Font('freesansbold.ttf', 20)
    big_text = font.render('Choose your algorithm', True, white)
    textRect = big_text.get_rect()
    textRect.center = ((1170), (display_height / 5))
    gameDisplay.blit(big_text, textRect)

    font = pygame.font.Font('freesansbold.ttf', 16)
    set_start_text = font.render('Set start', True, black)
    textRect = set_start_text.get_rect()
    textRect.center = ((1000 + (80 / 2)), (300 + (50 / 2)))
    gameDisplay.blit(set_start_text, textRect)

    font = pygame.font.Font('freesansbold.ttf', 16)
    set_goal_text = font.render('Set goal', True, black)
    textRect = set_goal_text.get_rect()
    textRect.center = ((1000 + (80 / 2)), (400 + (50 / 2)))
    gameDisplay.blit(set_goal_text, textRect)

    font = pygame.font.Font('freesansbold.ttf', 16)
    set_block_text = font.render('Set block', True, black)
    textRect = set_block_text.get_rect()
    textRect.center = ((1000 + (80 / 2)), (500 + (50 / 2)))
    gameDisplay.blit(set_block_text, textRect)

    font = pygame.font.Font('freesansbold.ttf', 16)
    delete_all_text = font.render('Delete all', True, black)
    textRect = delete_all_text.get_rect()
    textRect.center = ((1260 + (80 / 2)), (300 + (50 / 2)))
    gameDisplay.blit(delete_all_text, textRect)

    font = pygame.font.Font('freesansbold.ttf', 16)
    clear_cell_text = font.render('Clear cell', True, black)
    textRect = clear_cell_text.get_rect()
    textRect.center = ((1260 + (80 / 2)), (400 + (50 / 2)))
    gameDisplay.blit(clear_cell_text, textRect)

    font = pygame.font.Font('freesansbold.ttf', 16)
    inf_text = font.render('Info', True, black)
    textRect = inf_text.get_rect()
    textRect.center = ((1260 + (80 / 2)), (500 + (50 / 2)))
    gameDisplay.blit(inf_text, textRect)

    font = pygame.font.Font('freesansbold.ttf', 16)
    reset_text = font.render('Reset', True, black)
    textRect = reset_text.get_rect()
    textRect.center = ((1260 + (80 / 2)), (600 + (50 / 2)))
    gameDisplay.blit(reset_text, textRect)

    font = pygame.font.Font('freesansbold.ttf', 16)
    save_as_text = font.render('Save as', True, black)
    textRect = save_as_text.get_rect()
    textRect.center = ((1000 + (80 / 2)), (600 + (50 / 2)))
    gameDisplay.blit(save_as_text, textRect)

    font = pygame.font.Font('freesansbold.ttf', 16)
    load_text = font.render('Load', True, black)
    textRect = load_text.get_rect()
    textRect.center = ((1130 + (80 / 2)), (600 + (50 / 2)))
    gameDisplay.blit(load_text, textRect)

def buttons(x, y, w, h, action = None):
    global already_set_start, already_set_goal, set_start, set_goal, set_block, path_set, path, discover, clear_cell, grid_v, filename, alg
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    # αν το χ + το πλατος (W) του κουμπιου ειναι μεγαλυτερο απο το πλατος του ποντικιου μεγαλυτερο απο το χ του κουμπιου και αν το y + το υψος (h) του κουμπιου μεγαλυτερο απο το υψος του ποντικιου μεγαλυτερο απο το y του κουμπιου
    if (x + w) > mouse[0] > x and (y + h) > mouse[1] > y:
        if click[0] == 1 and action != None:  # αν πατηθει το ποντικι (αριστερο κλικ) και action διαφορο oy none
            # ελεγχει αν το κουμπι που πατηθηκε ειναι το set start, set goal, A*, Dijkstra, set block, delete all, clear cell, info, reset, save as, load
            if action == 'A*' and already_set_start and already_set_goal and not alg:
                for i in range(len(grid_v)):
                    for j in range(len(grid_v[0])):
                        if grid_v[i][j] == 1:
                            array[i][j] = 0
                        elif grid_v[i][j] == 2:
                            array[i][j] = 'Goal'
                        elif grid_v[i][j] == 3:
                            array[i][j] = 'O'
                        else:
                            array[i][j] = 999
                grid = Grid_astar(len(array), len(array[0]), array)
                path, discover = grid.A_star()
                path_set = True
                path.pop(0)  # κανουμε pop για να μην χρωματισει το start δηλαδη το πρωτο στοιχειο του path
                alg = True

            elif action == 'Dijkstra' and already_set_start and already_set_goal and not alg:
                for i in range(len(grid_v)):
                    for j in range(len(grid_v[0])):
                        if grid_v[i][j] == 1:
                            array[i][j] = 0
                        elif grid_v[i][j] == 2:
                            array[i][j] = 'Goal'
                        elif grid_v[i][j] == 3:
                            array[i][j] = 'O'
                        else:
                            array[i][j] = 999
                grid = Grid_dijkstra(len(array), len(array[0]), array)
                path, discover = grid.dijkstra()
                path_set = True
                path.pop(0)
                alg = True

            elif action == 'Set start' and already_set_start == False:
                set_start = True
                set_goal = False  # για να αποφυγουμε την περιπτωση να ενεργοποιηθουν ταυτοχρονα
                set_block = False
                clear_cell = False

            elif action == 'Set goal' and already_set_goal == False:
                set_goal = True
                set_start = False
                set_block = False
                clear_cell = False

            elif action == 'Set block':
                set_block = True
                set_start = False
                set_goal = False
                clear_cell = False

            elif action == 'Delete all':
                for i in range(len(grid_v)):
                    for j in range(len(grid_v[0])):
                        grid_v[i][j] = 4
                already_set_start = False  # για να μπορεσει να ξαναπατηθει το start μετα το delete all
                already_set_goal = False
                path_set = False
                alg = False

            elif action == 'Clear cell':
                clear_cell = True
                set_block = False
                set_start = False
                set_goal = False

            elif action == 'Info':
                tkinter.messagebox.showinfo("Algorithm information", "The purple boxes show the sortest path and the grey boxes show the mapping!")

            elif action == 'Reset':
                for i in range(len(grid_v)):
                    for j in range(len(grid_v[0])):
                        if grid_v[i][j] == 5 or grid_v[i][j] == 6:
                            grid_v[i][j] = 4
                path_set = False
                alg = False

            elif action == 'Save as':
                if already_set_start and already_set_goal:  # ελεγχουμε οτι εχει οριστει start και goal πριν την αποθηκευση
                    filename = filedialog.asksaveasfile(mode='w')
                    if filename == '':
                        filename = filedialog.asksaveasfile(mode='w')  # γινεται η αποθηκευση
                    if filename is not None:
                        j = json.dumps(grid_v)  # κωδικοποιουμε τον πινακα grid_v σε μορφη json
                        filename.write(j)  # γραφουμε τον κωδικοποιημενο πινακα στο αρχειο που αποθηκευσε ο χρηστης
                else:
                    tkinter.messagebox.showinfo("Error", "Please set start and goal before saving!")

            elif action == 'Load':
                filename = filedialog.askopenfile(mode='r+')
                if filename is not None:
                    t = filename.read()  # διαβαζουμε τα δεδομενα που εχει το αρχειο
                    grid_v = json.loads(t)  # τα γραφουμε στο grid
                    already_set_start = True  # για να μπορεσουν να τρεξουν οι αλγοριθμοι μετα την φορτωση της πιστας
                    already_set_goal = True
                    alg = False


def main():
    run = True
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False

            buttons(1000, 200, 80, 50, 'A*')
            buttons(1260, 200, 80, 50, 'Dijkstra')
            buttons(1000, 300, 80, 50, 'Set start')
            buttons(1000, 400, 80, 50, 'Set goal')
            buttons(1000, 500, 80, 50, 'Set block')
            buttons(1260, 300, 80, 50, 'Delete all')
            buttons(1260, 400, 80, 50, 'Clear cell')
            buttons(1260, 500, 80, 50, 'Info')
            buttons(1260, 600, 80, 50, 'Reset')
            buttons(1000, 600, 80, 50, 'Save as')
            buttons(1160, 600, 80, 50, 'Load')

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    global set_start, set_goal, set_block, clear_cell, already_set_start, already_set_goal
                    if set_start == True:
                        pos = pygame.mouse.get_pos()
                        if pos[0] <= 995:  # αν η θεση του ποντικιου ειναι μεχρι το τελος του grid στην ακρη δεξια
                            column = pos[0] // (grid_width + margin)
                            row = pos[1] // (grid_height + margin)
                            grid_v[row][column] = 1
                            set_start = False  # για να μην μπορεσει να ξαναπατηθει το start αφου το ορισουμε μια φορα
                            already_set_start = True  # για να αποφυγουμε να την περιπτωση να οριστει δυο φορες το set start

                    if set_goal == True:
                        pos = pygame.mouse.get_pos()
                        if pos[0] <= 995:
                            column = pos[0] // (grid_width + margin)
                            row = pos[1] // (grid_height + margin)
                            grid_v[row][column] = 2
                            set_goal = False
                            already_set_goal = True

                    if set_block == True:
                        pos = pygame.mouse.get_pos()
                        if pos[0] <= 995:
                            column = pos[0] // (grid_width + margin)
                            row = pos[1] // (grid_height + margin)
                            grid_v[row][column] = 3

                    if clear_cell == True:
                        pos = pygame.mouse.get_pos()
                        if pos[0] <= 995:
                            column = pos[0] // (grid_width + margin)
                            row = pos[1] // (grid_height + margin)
                            if grid_v[row][column] == 1:
                                already_set_start = False  # αν αυτο που μολις σβηνεται να επιτραπει να ξαναοριστει
                            elif grid_v[row][column] == 2:
                                already_set_goal = False
                            grid_v[row][column] = 4

        gameDisplay.fill(black)

        if path_set and discover:  # ελεγχουμε αν εχει τρεξει ο αλγοριθμος και η discover δεν ειναι αδεια
            pygame.time.delay(50)
            x = discover.pop(0)  # σε καθε επαναληψη του βρογχου των γραφικων κανω pop το πρωτο στοιχειο της discover
            grid_v[x[0]][x[1]] = 6  # χρωματιζω με γκρι τα στοιχεια που εξερευνησε
        if path_set and path and not discover:  # ελεγχουμε αν εχει τρεξει ο αλγοριθμος και η path δεν ειναι αδεια και η discover να εχει αδειασει
            pygame.time.delay(50)
            x = path.pop(0)
            grid_v[x[0]][x[1]] = 5  # χρωματιζω με μωβ το path πανω απο το γκρι


        for row in range(13):
            for column in range(18):
                color = white

                if grid_v[row][column] == 1:
                    color = green
                pygame.draw.rect(gameDisplay,
                                 color,
                                 [(margin + grid_width) * column + margin,
                                  (margin + grid_height) * row + margin,
                                  grid_width,
                                  grid_height])

                if grid_v[row][column] == 2:
                    color = red
                pygame.draw.rect(gameDisplay, color,
                                 [(margin + grid_width) * column + margin, (margin + grid_height) * row + margin,
                                  grid_width, grid_height])

                if grid_v[row][column] == 3:
                    color = black
                pygame.draw.rect(gameDisplay,
                                 color,
                                 [(margin + grid_width) * column + margin,
                                  (margin + grid_height) * row + margin,
                                  grid_width,
                                  grid_height])

                if grid_v[row][column] == 4:
                    color = white
                pygame.draw.rect(gameDisplay,
                                 color,
                                 [(margin + grid_width) * column + margin,
                                  (margin + grid_height) * row + margin,
                                  grid_width,
                                  grid_height])

                if grid_v[row][column] == 5:
                    color = purple
                pygame.draw.rect(gameDisplay,
                                 color,
                                 [(margin + grid_width) * column + margin,
                                  (margin + grid_height) * row + margin,
                                  grid_width,
                                  grid_height])

                if grid_v[row][column] == 6:
                    color = grey
                pygame.draw.rect(gameDisplay,
                                 color,
                                 [(margin + grid_width) * column + margin,
                                  (margin + grid_height) * row + margin,
                                  grid_width,
                                  grid_height])
        texts()
        pygame.display.update()
        clock.tick(60)

    pygame.quit()

main()
pygame.quit()
