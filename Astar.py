from operator import attrgetter  # μεθοδος η οποια κατηγοριοποιεί ενα αντικειμενο με βαση μια παραμετρο που εχει
import tkinter, tkinter.messagebox

D1 = 1  # ειναι 1 λογω της διαστασης του κελιου

class Cell_astar:
    def __init__(self, x, y, dist, f_score, parent_x, parent_y):
        self.x = x
        self.y = y
        self.dist = dist
        self.f_score = f_score
        self.parent_x = parent_x
        self.parent_y = parent_y


class Grid_astar:
    def __init__(self, row, col, grid):
        self.row = row
        self.col = col
        self.grid = grid
        self.open_list = []
        self.close_list = []
        self.found = False
        self.cell_list = []
        self.neighbours_list = []
        self.path = []
        self.discover = []

        for i in range(0, self.row):
            for j in range(0, self.col):
                # δημιουργω μια λιστα cell_list με objects ης κλασης Cell οπου καθε cell περιεχει τις συντεταγμενες, την αποσταση, το f_score και τα parents
                if self.grid[i][j] == 0:
                    self.cell_list.append(Cell_astar(i, j, 0, 0, None, None))
                    self.open_list.append(Cell_astar(i, j, 0, 0, None, None))
                    self.start_x = i
                    self.start_y = j
                elif self.grid[i][j] == 'Goal':
                    self.cell_list.append(Cell_astar(i, j, 99, 99, None, None))
                    self.goal_x = i
                    self.goal_y = j
                    self.goal_dist = 99
                    self.goal_f = 99
                elif self.grid[i][j] == 'O':
                    self.cell_list.append(Cell_astar(i, j, -1, -1, None, None))
                else:
                    self.cell_list.append(Cell_astar(i, j, 999, 999, None, None))


    def inside_grid(self, i, j):
        return 0 <= i < self.row and 0 <= j < self.col  # ελεγχω αν οι συντεταγμενες του κελιου που εξεταζω ειναι εντος του grid


    def heuristic(self, i, j, xg, yg):  # υπολογισμος αποστασης manhattan
        self.dx = abs(i - xg)
        self.dy = abs(j - yg)
        return (self.dx + self.dy) * D1


    def neighbours(self, a, b):
        self.neighbours_list = [(0, 1), (0, -1), (-1, 0), (1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]  # οριζω στην list τις συντεταγμενες και για τους 8 γειτονες
        self.minimum_cell_f = 999
        self.minimum_cell_x = 0
        self.minimum_cell_y = 0

        for i in self.neighbours_list:
            # υπολογιζω τις συντεταγμενες x και y των γειτονων
            x_neighbour = a + i[0]
            y_neighbour = b + i[1]

            if self.found == False:  # αν το found ειναι false σημαινει πως το goal δεν βρεθηκε οποτε μπαινουμε μεσα στο if
                #  ελεγχω αν ο γειτονας ειναι εντος του grid δεν ειναι το goal δηλαδη δεν εχει αποσταση 99 και δεν ειναι στην close_list
                if self.inside_grid(x_neighbour, y_neighbour) and self.cell_list[self.col * x_neighbour + y_neighbour].dist != 99 and self.cell_list[self.col * x_neighbour + y_neighbour] not in self.close_list:
                    if i[0] == 0 or i[1] == 0:  # αν ο γειτονας ειναι οριζοντια η καθετα μπαινω μεσα στο if
                        if self.cell_list[self.col * x_neighbour + y_neighbour].dist > self.cell_list[self.col * a + b].dist + 1:  # αν το κοστος του γειτονα ειναι μεγαλυτερο απο το κοστος του τωρινου κελιου + 1
                            self.cell_list[self.col * x_neighbour + y_neighbour].dist = self.cell_list[self.col * a + b].dist + 1  # θετουμε στο κοστος του γειτονα το κοστος του τωρινου κελιου + 1
                            # υπολογιζω το f_score
                            self.cell_list[self.col * x_neighbour + y_neighbour].f_score = self.cell_list[self.col * x_neighbour + y_neighbour].dist + self.heuristic(x_neighbour, y_neighbour, self.goal_x, self.goal_y)
                            self.cell_list[self.col * x_neighbour + y_neighbour].parent_x = a  # ενημερωνω τα parents
                            self.cell_list[self.col * x_neighbour + y_neighbour].parent_y = b
                            self.open_list.append(self.cell_list[self.col * x_neighbour + y_neighbour])  # κανω append στην open_list τον γειτονα που υπολογισαμε
                            self.grid[x_neighbour][y_neighbour] = self.cell_list[self.col * x_neighbour + y_neighbour].f_score  # ενημερωνω το grid βαζωντας του το f_score
                            self.discover.append([x_neighbour, y_neighbour])

                    elif self.cell_list[self.col * x_neighbour + y_neighbour].dist > round(self.cell_list[self.col * a + b].dist + 1.4, 2):  # η ιδια διαδικασια γινεται και για τους διαγωνιους γειτονες
                        self.cell_list[self.col * x_neighbour + y_neighbour].dist = round(self.cell_list[self.col * a + b].dist + 1.4, 2)
                        self.cell_list[self.col * x_neighbour + y_neighbour].f_score = self.cell_list[self.col * x_neighbour + y_neighbour].dist + self.heuristic(x_neighbour, y_neighbour, self.goal_x, self.goal_y)
                        self.cell_list[self.col * x_neighbour + y_neighbour].parent_x = a
                        self.cell_list[self.col * x_neighbour + y_neighbour].parent_y = b
                        self.open_list.append(self.cell_list[self.col * x_neighbour + y_neighbour])
                        self.grid[x_neighbour][y_neighbour] = self.cell_list[self.col * x_neighbour + y_neighbour].f_score
                        self.discover.append([x_neighbour, y_neighbour])


                elif self.inside_grid(x_neighbour, y_neighbour) and self.cell_list[self.col * x_neighbour + y_neighbour].dist == 99:
                    # ελεγχω εαν ο γειτονας του κελιου που εξεταζω ειναι εντος grid και αν ειναι το goal τοτε το found γινεται true
                    self.found = True
                    print('Goal found')
                    self.cell_list[self.col * x_neighbour + y_neighbour].parent_x = a  # ενημερωνω τα parents
                    self.cell_list[self.col * x_neighbour + y_neighbour].parent_y = b
                    break  # κανω break ετσι ωστε να μην εκτελεσθει τιποτα παραπανω


    def shortest_path(self, temp, temp_x, temp_y):
        self.path.append([temp_x, temp_y, ':', temp])  # προσθετω στην path τα ορισματα
        par_x = self.cell_list[self.col * temp_x + temp_y].parent_x  # αναθετω στους par_x και par_y τα parents του καθε κελιου απο το goal μεχρι το start
        par_y = self.cell_list[self.col * temp_x + temp_y].parent_y
        temp = self.cell_list[self.col * par_x + par_y].f_score
        if par_x == self.start_x and par_y == self.start_y:  # αν οι parents ισουνται με τις συντεταγμενες του start τοτε κανουμε return και διακοπτεται η λειτουργια της συναρτησης
            return 0
        self.shortest_path(temp, par_x, par_y)  # ξανακαλειται η shortest_path, πραγματοποιειται αναδρομη


    def A_star(self):
        # οσο ισχυει η αρχικη συνθηκη του αλγοριθμου δηλαδη οσο η open_list δεν ειναι αδεια και το found ειναι false δηλαδη δεν εχει βρεθει το goal μπαινει στο loop
        while (self.open_list != []) and (self.found == False):
            self.cell = min(self.open_list, key=attrgetter('f_score'))  # επιλεγω το κελι με τo μικροτερο f_score απο την open_list
            self.close_list.append(self.cell)  # το προσθετω στην close_list
            self.open_list.remove(self.cell)  # το αφαιρω απο την open_list
            self.neighbours(self.cell.x, self.cell.y)  # καλω την συναρτηση neighbours για να υπολογισει τους γειτονες του

        for i in range(0, self.row):  # εκτυπωνω το grid
            print(self.grid[i])

        try:
            self.shortest_path(self.goal_f, self.goal_x, self.goal_y)  # καλω την shortest_path με ορισματα τις συντεταγμενες και το f_score του goal
        except TypeError:
            tkinter.messagebox.showinfo("Error", "There is no possible path from start to goal. \n\nThe application will now exit!")
            exit()
        self.path.append([self.start_x, self.start_y, ':', self.cell_list[self.col * self.start_x + self.start_y].f_score])  # προσθετω στην path το start
        self.path.reverse()  # αντιστρεφω τα στοιχεια της λιστας path
        self.path.pop()  # αφαιρω το τελευταιο στοιχειο της path γιατι στην αρχη εβγαζε τις συντεταγμενες και το f_score του goal ενω εμεις θελουμε να εμφανιζει το στοιχειο μεχρι και πριν το goal
        print('The shortest path from start to goal is:')
        print(self.path, '-->', 'Goal')  # εμφανιζω το συντομοτερο μονοπατι
        return self.path, self.discover
        # for i in range(1, len(self.path)):
        #     self.grid_v[self.path[i][0]][self.path[i][1]] = 5

# if __name__ == '__main__':
#     #array = [[0, 999, 999, 999, 999, 999, 999],  # ο πινακας εχει τα κοστη, στο τελος του αλγοριθμου ο πινακας θα δειχνει τα f_score και οχι τα κοστη
#              #[999, 999, 999, 999, 999, 999, 999],
#              #[999, 999, 999, 999, 999, 999, 999],
#              #[999, 999, 'O', 'O', 'O', 'O', 999],
#              #[999, 999, 'O', 'O', 'O', 'O', 'Goal'],
#              #[999, 999, 999, 999, 999, 999, 999],
#              #[999, 999, 999, 999, 999, 999, 999]]
#     #array = [[999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999],  # μπορειτε να χρησιμοποιησειτε και αυτον τον πινακα
#              #[999, 999, 999, 'O', 'Goal', 999, 999, 999, 999, 999, 999],
#              #[999, 999, 999, 'O', 'O', 'O', 'O', 'O', 999, 999, 999],
#              #[999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999],
#              #[999, 999, 999, 999, 999, 999, 999, 0, 999, 999, 999],
#              #[999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999]]
#     array = [[0, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999],
#              [999, 999, 999, 'O', 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999],
#              [999, 999, 999, 'O', 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999],
#              [999, 999, 999, 999, 'O', 'O', 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999],
#              [999, 999, 999, 'O', 'O', 'O', 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999],
#              [999, 999, 999, 'O', 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999],
#              [999, 999, 999, 'O', 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999],
#              [999, 999, 999, 'O', 'O', 'O', 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999],
#              [999, 999, 999, 'O', 'O', 'O', 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999],
#              [999, 999, 999, 999, 999, 'O', 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999],
#              [999, 999, 999, 999, 'O', 'O', 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999],
#              [999, 999, 999, 999, 'O', 'O', 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999],
#              [999, 999, 999, 999, 'O', 'O', 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 'Goal']]
#     grid = Grid(len(array), len(array[0]), array)
#     grid.A_star()