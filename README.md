This project is divided into two parts. In the first part, two basic optimization path algorithms were studied and implemented in a grid system, which are namely Dijkstra and A *. These algorithms are used only on maps with static obstacles. The second part of the project presents the development of a graphical environment for the visualization of the two algorithms.The pygame library is used to create the graphic environment. The installation is done on the command line with the following command: pip install pygame (requirements.txt). Then if any is used ide you will have to install it there as well.

Menu:

1.Set start: Set the start in a grid cell, it can only be set once, to be set again in another position it needs to be deleted first.

2.Set goal: Set the goal in a cell of the grid, it is allowed to set only once, to set again in another position it needs to be deleted first.

3.Set block: Set the block in as many cells as the user wishes, there is no limit can be set as many times as the user wants.

4.Delete all: Clear the screen (grid).

5.Clear cell: Clear cell, first the user clicks the button and then can choose which cell he wants to delete. It has no limit, it has the ability to delete as many cells as it wants.

6.A *: Start the algorithm A *.

7.Dijkstra: Start the dijkstra algorithm.

8.Reset: Clear the screen (grid) except the start, goal and block if any.

9.Save as: Save track to PC.

10.Load: Loading track on the screen (grid).

11.Info: Information of each algorithm.
