# Ex4-Pokemons

Last assignment in our OOP course

![ezgif com-gif-maker](https://user-images.githubusercontent.com/73894107/148676170-e87972bc-ed87-4bd9-8978-e71178d5d362.gif)


* [Shaked's github](https://github.com/20shaked20)
* [Yonatan's github](https://github.com/Teklar223)

## Introduction
- If you just want to know how to use this code please skip to the ``` How To Use ``` segment below.
- If you want to know how to work with the gui, we've dedictated a wiki page for it.

In this assignment we are tasked with designing a *pokemon 'game'*, in which we have a map of cities, roads between them, pokemons who sit on these roads, and agents who want to capture said pokemons. </br> </br>
This scenario is then wittled down to a non-directed weighted graph problem, the cities become nodes, roads become edges, and pokemons and agents are represented (initially) as circles. </br> </br>
Now, whenever an agent travels across the graph and happens to move through a road where a pokemo sits, he captures him and gains points, becoming quicker the more pokemon he catches, but there is a 'catch' ( haha :D ), while the graph is not directed, pokemons are! - that means that a capture only occurs if the agent travelled on the edge in the same direction as the pokemon 'sits' on it. </br> </br>
e.g. - a pokemon sits on the edge from node 9 to 10 and we know that for him the source < destination, therefore the agent will have to arrive at node 9 then travel to node 10 to capture him. 
</br> 
otherwise, if for the pokemon the source > destination then the agent would have to travel to node 10 and then to node 9 to capture him.

## Approach
Firstly, this is not our first assignment on graphs!, weve had two previous assignments ( one in java, and on in python ) both of which contain graph related algorithm's, such as Dijkstra's shortest path for example, so we imported those algorithm's into our solution immediatly. </br>
Now we have the advantage of being able to boil down our problem and solve it with applications of our previously implemented algorithm, for example if we wanted the agent to start at the 'best' position we could consider letting him start at the graph center!
</br> </br>
Secondly, we had to represent the entire game as a GUI, similar to 0 player games!, for this we looked at our previous GUI's and decided on pygame ( and tkinter for our basic 'login' ), we decided to change almost all aspects of the initial game visually, like adding different pokemon pictures, changing the background etc...
</br> </br>
Thirdly, we had to consider principles like S.O.L.I.D and MVC, and strive towards them in our project architecture!

## The Algorithms
``` Tabibito algorithm  ```: </br>
- step 0: place agents initially next to the most valuable pokemons 
- step 1: using Dijkstra's shortest path, find the closest not 'taken' pokemon
- step 2: tell the agent where he needs to go according to step 1, and broadcast the pokemon as 'taken'
- step 3: after the agent captured the pokemon, reapeat step 1.
</br>
note 1 - we are indeed in charge of where the agent starts his journey.
</br>
note 2 - this is the algorithm we strove for, the implementation may be missing fine details, but follows the same idea.


## The Classes
``` Ex4_Server_v0.0.jar ``` - This is *not* a class, but it is however an integral part of our project, as the entire game-state is managed through it.  </br>
 </br>
``` client ``` - This class is in charge of communicating with the server, receiving the game state and sending our agent's next move.  </br> 
</br>
``` Arena ``` - This class is the *"main"* class, in charge of drawing the game state, activating ``` RunServerScript ``` once, and telling the agents to move.  </br>
 </br>
``` game ``` - This class is in charge of game initialization for ``` Arena ```.  </br>
</br>
``` Logic ``` - This class is in charge of logical calculations, and as such *our algorithm is in this class*. </br>
 </br>
``` Login ``` - This class is a small 'login' GUI which allows the user to choose a case between 0 to 15.  </br>
 </br>
``` Misc ``` - This class contains code snippets which are common to atleast two other classes in our code.  </br>
 </br>
``` RunServerScript ``` - this script is in charge of activating ``` Ex4_Server_v0.0.jar ```.

## How To use

Note - you can unpack the .zip if you choose to, it works either way!

- Step 0: finding this repository! - *this is absolutely critical*.
</br></br>
- Step 1: finding our realase, have a look at this picture if you're having trouble locating it (or scroll all the way UP)
</br></br>
![image](https://user-images.githubusercontent.com/73063105/148678274-9b547ce3-3343-48ce-aec9-11a83beb8102.png)
</br></br>
- Step 2: choose a distribution that's appropriate to your OS, it's one of these:
</br></br>
![image](https://user-images.githubusercontent.com/73063105/148678398-f778697b-a535-4016-84b1-930e00257960.png)
</br></br>
- Step 3: after you open the appropriate .zip file, you should navigate to this: </br>
- For WINDOWS: 
</br></br>
![image](https://user-images.githubusercontent.com/73063105/148678476-c79f82d3-fd3d-4e39-ba6d-fafeaf09a472.png)
</br></br>
and then click on ``` Login.exe ```
</br></br>
![image](https://user-images.githubusercontent.com/73063105/148678495-035fd404-b539-4b14-a6f9-d81f00785e84.png)
<br></br>
- For MAC: 
</br></br>
![image](https://user-images.githubusercontent.com/73063105/148678542-04ae5519-9e32-4156-8eec-7fe0f6b5b36c.png)
</br></br>
and then activate ``` Login ``` as you would other .exe like files in MAC 
</br></br>
![image](https://user-images.githubusercontent.com/73063105/148678565-2188f5c9-e648-4be5-b388-e5ece81b6f8d.png)
</br></br>
- Step 4: you will come upon a screen like this, you must enter a case number between 0-15 (16 cases all in all)
</br></br>
![image](https://user-images.githubusercontent.com/73063105/148678698-2c170235-7e6c-43d0-92aa-dc3abedd626d.png)
</br></br>
- Step 5: See the game play itself!, it's somewhat of a 0-player game after all, and repeat as you'd like!
</br></br>
![image](https://user-images.githubusercontent.com/73063105/148678794-6eecf0fc-fd19-4a48-a9f6-eed268237869.png)
</br></br>
- note: a CMD (or equivalent) should appear, and you could probably view some 'calculations', if after the game it happens to not close by itself, simply close it yourself, this is *not* intended behaviour!


### If you're using PyCharm and scientific mode is on:
* it may interfere with the gui, if this happens please follow these [instructions](https://stackoverflow.com/questions/48384041/pycharm-how-to-remove-sciview)

## dependencies

``` Pygame ```  - please see [GettingStarted - pygame wiki](https://www.pygame.org/wiki/GettingStarted)

## Lessons Learned
### things to improve
- Spend more time in the early stages of development on project architechture

### things to keep
- Source control
- Naive solution first, then iterate for an elegant solution
- Proper reasearch

## Hierarchy
![game_uml](https://user-images.githubusercontent.com/73894107/148647824-7fc8557d-23dd-4af1-b48b-1b70325e5063.png)


## Reading Material
- About Directed, Weighted, and Directed + Weighted graphs: http://math.oxford.emory.edu/site/cs171/directedAndEdgeWeightedGraphs/
- Shortest Path: https://en.wikipedia.org/wiki/Shortest_path_problem#Algorithms
- Dijkstra: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
