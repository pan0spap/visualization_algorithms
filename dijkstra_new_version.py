from operator import attrgetter  # μεθοδος η οποια κατηγοριοποιεί ενα αντικειμενο με βαση μια παραμετρο που εχει
import tkinter, tkinter.messagebox

class Cell_dijkstra:
    def __init__(self, x, y, dist):
        self.x = x
        self.y = y
        self.dist = dist


class Grid_dijkstra:
    def __init__(self, row, col, grid):
        self.row = row
        self.col = col
        self.grid = grid
        self.priority_list = []
        self.found = False
        self.cell_list = []
        self.neighbours_list = []
        self.path = []
        self.discover = []

        for i in range(0, self.row):
            for j in range(0, self.col):
                # δημιουργω την cell_list, μια λιστα με objects τυπου Cell οπου καθε object(cell) περιεχει τις συντεταγμενες και την αποσταση
                if self.grid[i][j] == 0:
                    self.cell_list.append(Cell_dijkstra(i, j, 0))  # εκχωρω στην cell_list τις συντεταγμενες και την αποσταση για το start
                    self.priority_list.append(Cell_dijkstra(i, j, 0))  # εκχωρω στην priority_list το start
                elif self.grid[i][j] == 'Goal':
                    self.cell_list.append(Cell_dijkstra(i, j, 99))
                    self.goal_x = i
                    self.goal_y = j
                    self.goal_dist = 99
                elif self.grid[i][j] == 'O':
                    self.cell_list.append(Cell_dijkstra(i, j, -1))
                else:
                    self.cell_list.append(Cell_dijkstra(i, j, 999))

    def inside_grid(self, i, j):
        return 0 <= i < self.row and 0 <= j < self.col  # ελεγχω αν οι συντεταγμενες του κελιου που εξεταζω ειναι εντος του grid

    def neighbours(self, a, b):
        self.neighbours_list = [(0, 1), (0, -1), (-1, 0), (1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]  # οριζω στην neighbours_list τις συντεταγμενες και για τους 8 γειτονες
        self.minimum_cell = 999
        self.minimum_cell_x = 0
        self.minimum_cell_y = 0
        for i in self.neighbours_list:
            # υπολογιζω τις συντεταγμενες x και y των γειτονων
            x_neighbour = a + i[0]
            y_neighbour = b + i[1]

            if self.found == False:
                if self.inside_grid(x_neighbour, y_neighbour) and self.cell_list[self.col * x_neighbour + y_neighbour].dist == 999:  # ελεγχω αν οι γειτονες του κελιου που εξεταζουμε ειναι εντος grid και αν εχουν τιμη 999, δηλαδη δεν ειναι visited
                    if i[0] == 0 or i[1] == 0:  # υπολογισμος γειτονων οριζοντια η καθετα
                        self.cell_list[self.col * x_neighbour + y_neighbour].dist = self.cell_list[self.col * a + b].dist + 1
                        self.grid[x_neighbour][y_neighbour] = self.cell_list[self.col * x_neighbour + y_neighbour].dist  # ενημερωνω το grid με την αποσταση του γειτονα που υπολογισαμε
                        self.discover.append([x_neighbour, y_neighbour])
                        self.priority_list.append(self.cell_list[self.col * x_neighbour + y_neighbour])  # εκχωρω στην priority_list τα κελια που λαμβανουν τιμη
                    else:
                        # υπολογισμος για τους διαγωνιους γειτονες
                        self.cell_list[self.col * x_neighbour + y_neighbour].dist = round(self.cell_list[self.col * a + b].dist + 1.4, 2)
                        self.grid[x_neighbour][y_neighbour] = self.cell_list[self.col * x_neighbour + y_neighbour].dist
                        self.discover.append([x_neighbour, y_neighbour])
                        self.priority_list.append(self.cell_list[self.col * x_neighbour + y_neighbour])

                elif self.inside_grid(x_neighbour, y_neighbour) and self.cell_list[self.col * x_neighbour + y_neighbour].dist == 99:  # εαν ειναι το goal κανουμε break
                    self.found = True
                    print('Goal found')
                    break


            if self.found == True and self.inside_grid(x_neighbour, y_neighbour):
                if self.minimum_cell > self.cell_list[self.col * x_neighbour + y_neighbour].dist >= 0:  # το >= 0 ειναι για να μην λαβει υποψην τα εμποδια επειδη εχω ορισει την αποσταση τους ως -1
                    self.minimum_cell = self.cell_list[self.col * x_neighbour + y_neighbour].dist
                    self.minimum_cell_x = x_neighbour
                    self.minimum_cell_y = y_neighbour

        return self.minimum_cell, self.minimum_cell_x, self.minimum_cell_y  # επιστερφω το κελι με την μικροτερη τιμη και τις συντεταγμενες του

    def shortest_path(self, temp_min, temp_x, temp_y):  # παιρνει στα ορισματα την αποσταση και τις συντεταγμενες του goal για να υπολογισει απο τους γειτονες του αυτον που εχει το μικροτερο κοστος
        for i in self.cell_list:
            if i.x == temp_x and i.y == temp_y:
                temp_min, temp_x, temp_y = self.neighbours(i.x, i.y)
                self.path.append([temp_x, temp_y, ':', temp_min])
                if temp_min == 0:  # αν το κελι με την μικροτερη τιμη ισουται με το start οπου ειναι το 0 τοτε
                    return 0  # κανω return για να διακοπει η ανδρομικοτητα συνεπως και η λειτουργεια της συναρτησης
        self.shortest_path(temp_min, temp_x, temp_y)  # γινεται αναδρομη για να ξανακληθει η stortset_path, ωστε να υπολογισει και για τους γειτονες του καθε κελιου που θα βρεθει με την μικροτερη αποσταση μεχρι να βρω το start

    def dijkstra(self):
        while (self.priority_list != []) and (self.found == False):  # οσο ισχυει η αρχικη συνθηκη του αλγοριθμου δηλαδη οσο η priority_list δεν ειναι αδεια και το found ειναι false μπαινει στο loop
            self.cell = min(self.priority_list, key=attrgetter('dist'))  # επιλεγω το κελι με την μικροτερη αποσταση μεσα απο την priority_list χρησιμοποιωντας την μεθοδο attrgetter
            self.priority_list.remove(self.cell)
            self.neighbours(self.cell.x, self.cell.y)

        for i in range(0, self.row):  # εκτυπωνω το grid
            print('\n')
            for j in range(0, self.col):
                print(self.grid[i][j], end='\t\t')
        print('\n')

        try:
            self.shortest_path(self.goal_dist, self.goal_x, self.goal_y)  # καλω την συναρτηση shortest_path
        except RecursionError:
            tkinter.messagebox.showinfo("Error", "There is no possible path from start to goal. \n\nThe application will now exit!")
            exit()
        self.path.reverse()  # αντιστρεφω τα στοιχεια της λιστας path
        print('The shortest path from start to goal is:')
        print(self.path, '-->', 'Goal')  # εμφανιζω το συντομοτερο μονοπατι
        return self.path, self.discover
        # for i in range(1, len(self.path)):
        #     self.grid_v[self.path[i][0]][self.path[i][1]] = 5

# if __name__ == '__main__':
#     #array = [[0, 999, 999, 999, 999, 999, 999],
#              #[999, 999, 999, 999, 999, 999, 999],
#              #[999, 999, 999, 999, 999, 999, 999],
#              #[999, 999, 999, 'O', 'O', 'O', 999],
#              #[999, 999, 999, 'O', 'O', 'O', 'Goal'],
#              #[999, 999, 999, 999, 999, 999, 999],
#              #[999, 999, 999, 999, 999, 999, 999]]
#     # array = [[0, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999],
#     #          [999, 999, 999, 'O', 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999],
#     #          [999, 999, 999, 'O', 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999],
#     #          [999, 999, 999, 999, 'O', 'O', 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999],
#     #          [999, 999, 999, 'O', 'O', 'O', 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999],
#     #          [999, 999, 999, 'O', 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999],
#     #          [999, 999, 999, 'O', 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999],
#     #          [999, 999, 999, 'O', 'O', 'O', 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999],
#     #          [999, 999, 999, 'O', 'O', 'O', 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999],
#     #          [999, 999, 999, 999, 999, 'O', 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999],
#     #          [999, 999, 999, 999, 'O', 'O', 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999],
#     #          [999, 999, 999, 999, 'O', 'O', 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999],
#     #          [999, 999, 999, 999, 'O', 'O', 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 'Goal']]
#
#     grid = Grid(len(array), len(array[0]), array)
#     grid.dijkstra()