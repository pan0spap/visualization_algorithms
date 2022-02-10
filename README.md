This project is divided into two parts. In the first part, two basic optimization path algorithms were studied and implemented in a grid system, which are namely Dijkstra and A *. These algorithms are used only on maps with static obstacles. The second part of the project presents the development of a graphical environment for the visualization of the two algorithms.The pygame library is used to create the graphic environment (requirements.txt).

Menu:

Set start: Set the start in a grid cell, it can only be set once, to be set again in another position it needs to be deleted first.

Set goal: Set the goal in a cell of the grid, it is allowed to set only once, to set again in another position it needs to be deleted first.

Set block: Set the block in as many cells as the user wishes, there is no limit can be set as many times as the user wants.

Delete all: Clear the screen (grid).

Clear cell: Clear cell, first the user clicks the button and then can choose which cell he wants to delete. It has no limit, it has the ability to delete as many cells as it wants.

A*: Start the algorithm A *.

Dijkstra: Start the dijkstra algorithm.

Reset: Clear the screen (grid) except the start, goal and block if any.

Save as: Save track to PC.

Load: Loading track on the screen (grid).

Info: Information of each algorithm.
