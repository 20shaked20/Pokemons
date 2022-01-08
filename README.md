# Ex4-Pokemons

Last assignment in OOP course

* [Shaked's github](https://github.com/20shaked20)
* [Yonatan's github](https://github.com/Teklar223)

## Introduction
- If you just want to know how to use this code please skip to the ``` How To Use ``` segment below.
- If you want to know how to work with the gui, we've dedictated a wiki page for it.

In this assignment we are tasked with designing a *pokemon 'game'*, in which we have a map of cities, roads between them, pokemons who sit on these roads, and agents who want to capture said pokemons. </br>
This scenario is then wittled down to a non-directed weighted graph problem, the cities become nodes, roads become edges, and pokemons and agents are represented (initially) as circles. </br>
Now, whenever an agent travels across the graph and happens to move through a road where a pokemo sits, he captures him and gains points, becoming quicker the more pokemon he catches, but there is a 'catch' ( haha :D ), while the graph is not directed, pokemons are! - that means that a capture only occurs if the agent travelled on the edge in the same direction as the pokemon 'sits' on it. </br>
e.g. - a pokemon sits on the edge from node 9 to 10 and we know that for him the source < destination, therefore the agent will have to arrive at node 9 then travel to node 10 to capture him, otherwise if for the pokemon the source > destination then the agent would have to travel to node 10 and then to node 9 to capture him.

## Approach
Firstly, this is not our first assignment on graphs!, weve had two previous assignments ( one in java, and on in python ) both of which contain graph related algorithm's, such as Dijkstra's shortest path for example, so we imported those algorithm's into our solution immediatly. </br>
Now we have the advantage of being able to boil down our problem and solve it with applications of our previously implemented algorithm, for example if we wanted the agent to start at the 'best' position we could consider letting him start at the graph center!
</br>
Secondly, we had to represent the entire game as a GUI, similar to 0 player games!, for this we looked at our previous GUI's and decided on pygame ( and tkinter for our basic 'login' ), we decided to change almost all aspects of the initial game visually, like adding different pokemon pictures, changing the background etc...
</br>
Thirdly, we had to consider principles like S.O.L.I.D and MVC, and strive towards them in our project architecture!

## The Algorithms
Tabibito algorithm -

## The Classes
``` Ex4_Server_v0.0.jar ``` - This is *not* a class, but it is however an integral part of our project, as the entire game-state is managed through it.
``` client ``` - This class is in charge of communicating with the server, receiving the game state and sending our agent's next move.
``` Arena ``` - This class is the *"main"* class, in charge of drawing the game state, activating ``` RunServerScript ``` once, and telling the agents to move.
``` game ``` - This class is in charge of game initialization for ``` Arena ```.
``` Logic ``` - This class is in charge of logical calculations, and as such *our algorithm is in this class*. 
``` Login ``` - This class is a small 'login' GUI which allows the user to choose a case between 0 to 15.
``` Misc ``` - This class contains code snippets which are common to atleast two other classes in our code.
``` RunServerScript ```


## How To use

### If you're using PyCharm and scientific mode is on:
* it may interfere with the gui, if this happens please follow these [instructions](https://stackoverflow.com/questions/48384041/pycharm-how-to-remove-sciview)

## dependencies

``` Pygame ```  - please see [GettingStarted - pygame wiki](https://www.pygame.org/wiki/GettingStarted)

## Lessons Learned
### things to improve
- Being even more 'on the same page'

### things to keep
- Source control
- Naive solution first, then iterate for an elegant solution
- Proper reasearch

## File Hierarchy


## Reading Material
- About Directed, Weighted, and Directed + Weighted graphs: http://math.oxford.emory.edu/site/cs171/directedAndEdgeWeightedGraphs/
- Shortest Path: https://en.wikipedia.org/wiki/Shortest_path_problem#Algorithms
- Dijkstra: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
