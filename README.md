## Introduction

Based on [wikipedia](https://en.wikipedia.org/wiki/Elevator_algorithm), elevator algorithm is ..

> .. where the elevator continues to travel in its current direction (up or down) until empty, stopping only to let individuals off or to pick up new individuals heading in the same direction. 

Based on _contoh.py_, we have several useful information.

* Controller class: to simulate the centralized control panel of the elevator system
  * init: create instance of controller class and set default values
  * run: function to start the controller thread
  * request: function to serve reception of request from user (user push the lift button), the request list is appended
  * pickup first passenger: function invoked by the elevator to pick up first passenger (in the elevator)
  * pickup passenger: function invoked by the elevator to pick up passenger (in the elevator)
  * get closest passenger: function invoked by the elevator to find closest passenger when no passenger in elevator

* Elevator class: to simulate the instance of elevator
  * init: create an instance of elevator class and set default values
  * run: function to start the elevator thread
  * pickup passenger: function to simulate the elevator fetching passengers
  * move: function to simulate the movement of the elevator
  * set direction: function to set the direction of the elevator
  * dropoff passenger: function to simulate dropping off passenger once the targeted floor is reached
  * label: function to label the passenger details
  * delay: function to simulate delay of the elevator moving from one floor to another

The code operation is too much and was minimized. Items that were reduced are:

* Remove elevator 2 instances from code
* Change min and max delay for low traffic type to 1 and 2 respectively
* Change total request in generate requests function for low to 10

Let see the output for minimized version.

```bash
$ python3 contoh.py 
Lift-1: Starting 
Lift-1 [F:1 P:0] : moving up from Floor 1
Controller: received a request from User 1 from floor 3 down to floor 1
Controller: received a request from User 2 from floor 4 up to floor 5
Controller: received a request from User 3 from floor 4 down to floor 1
Lift-1 [F:2 P:0] : arrived at Floor 2 (distance: 1)
Lift-1 [F:2 P:0] : moving up from Floor 2
Controller: received a request from User 4 from floor 4 down to floor 1
Controller: received a request from User 5 from floor 5 down to floor 3
Controller: received a request from User 6 from floor 3 down to floor 1
Lift-1 [F:3 P:0] : arrived at Floor 3 (distance: 2)
Lift-1 [F:3 P:1] : pickup first passenger: User1 Floor3 --> Floor1 (down)
Controller: 1 requests completed. Avg waiting time: 10.0306
Lift-1 [F:3 P:2] : pickup passenger: User6 Floor3 --> Floor1 (down)
Controller: 2 requests completed. Avg waiting time: 5.9993
Lift-1 [F:3 P:2] : moving down from Floor 3
Controller: received a request from User 7 from floor 3 down to floor 2
Controller: received a request from User 8 from floor 3 down to floor 2
Controller: received a request from User 9 from floor 3 up to floor 5
Controller: received a request from User 10 from floor 5 down to floor 1
Lift-1 [F:2 P:2] : arrived at Floor 2 (distance: 3)
Lift-1 [F:2 P:2] : moving down from Floor 2
Lift-1 [F:1 P:2] : arrived at Floor 1 (distance: 4)
Lift-1 [F:1 P:2] : drop_off passenger: User1 Floor3 --> Floor1 (down)
Lift-1 [F:1 P:2] : drop_off passenger: User6 Floor3 --> Floor1 (down)
Lift-1 [F:1 P:0] : moving up from Floor 1
Lift-1 [F:2 P:0] : arrived at Floor 2 (distance: 5)
Lift-1 [F:2 P:0] : moving up from Floor 2
Lift-1 [F:3 P:0] : arrived at Floor 3 (distance: 6)
Lift-1 [F:3 P:1] : pickup first passenger: User7 Floor3 --> Floor2 (down)
Lift-1 [F:3 P:2] : pickup passenger: User8 Floor3 --> Floor2 (down)
Lift-1 [F:3 P:2] : moving down from Floor 3
Controller: 4 requests completed. Avg waiting time: 12.523
Lift-1 [F:2 P:2] : arrived at Floor 2 (distance: 7)
Lift-1 [F:2 P:2] : drop_off passenger: User7 Floor3 --> Floor2 (down)
Lift-1 [F:2 P:2] : drop_off passenger: User8 Floor3 --> Floor2 (down)
Lift-1 [F:2 P:0] : moving up from Floor 2
Lift-1 [F:3 P:0] : arrived at Floor 3 (distance: 8)
Lift-1 [F:3 P:1] : pickup first passenger: User9 Floor3 --> Floor5 (up)
Lift-1 [F:3 P:1] : moving up from Floor 3
Controller: 5 requests completed. Avg waiting time: 15.4383
Lift-1 [F:4 P:1] : arrived at Floor 4 (distance: 9)
Lift-1 [F:4 P:2] : pickup passenger: User2 Floor4 --> Floor5 (up)
Lift-1 [F:4 P:2] : moving up from Floor 4
Controller: 6 requests completed. Avg waiting time: 20.2379
Lift-1 [F:5 P:2] : arrived at Floor 5 (distance: 10)
Lift-1 [F:5 P:2] : drop_off passenger: User9 Floor3 --> Floor5 (up)
Lift-1 [F:5 P:2] : drop_off passenger: User2 Floor4 --> Floor5 (up)
Lift-1 [F:5 P:1] : pickup first passenger: User5 Floor5 --> Floor3 (down)
Lift-1 [F:5 P:2] : pickup passenger: User10 Floor5 --> Floor1 (down)
Lift-1 [F:5 P:2] : moving down from Floor 5
Controller: 8 requests completed. Avg waiting time: 25.1046
Lift-1 [F:4 P:2] : arrived at Floor 4 (distance: 11)
Lift-1 [F:4 P:3] : pickup passenger: User3 Floor4 --> Floor1 (down)
Lift-1 [F:4 P:4] : pickup passenger: User4 Floor4 --> Floor1 (down)
Lift-1 [F:4 P:4] : moving down from Floor 4
Controller: ALL requests completed...
Controller: passenger average waiting time >> 30.336
Lift-1 [F:3 P:4] : arrived at Floor 3 (distance: 12)
Lift-1 [F:3 P:4] : drop_off passenger: User5 Floor5 --> Floor3 (down)
Lift-1 [F:3 P:3] : moving down from Floor 3
Lift-1 [F:2 P:3] : arrived at Floor 2 (distance: 13)
Lift-1 [F:2 P:3] : moving down from Floor 2
Lift-1 [F:1 P:3] : arrived at Floor 1 (distance: 14)
Lift-1 [F:1 P:3] : drop_off passenger: User10 Floor5 --> Floor1 (down)
Lift-1 [F:1 P:3] : drop_off passenger: User3 Floor4 --> Floor1 (down)
Lift-1 [F:1 P:3] : drop_off passenger: User4 Floor4 --> Floor1 (down)
Main: Average Users Waiting Time: 30.336
Main: Elevator1 total distance: 14
............... ELEVATOR SIMULATION COMPLETED .................
```

The elevator works like this:

* If no passenger in elevator, check for closest passenger in request queue (check for floor above first, then the floor below)
* When elevator get to the closest passenger floor, it will check for user that have same direction and pick up if possible
* It will check the passenger destination when get to each floor and drop the passenger if possible

## Task 1: Round-robin

Based on [wikipedia](https://en.wikipedia.org/wiki/Round-robin_scheduling), it is defines as a ..

> .. scheduler generally employs time-sharing, giving each job a time slot or quantum (its allowance of CPU time), and interrupting the job if it is not completed by then.

Actually the most suitable word for this algorithm is [circular queue](https://en.wikipedia.org/wiki/Circular_buffer), not round-robin. Basically it's just, rotating to each floors in circular order: 1 -> 2 -> 3 -> 4 -> 3 -> 2 -> 1 -> 2 -> ..

You need to change the controller class's and elevator class's functions. It is very subjective and the possibilities for changes is too much.

## Task 2: First come, first serve

Based on [wikipedia](https://en.wikipedia.org/wiki/FIFO_(computing_and_electronics)), first come first serve is ..

> .. a method for organising and manipulating a data buffer, where the oldest (first) entry, or 'head' of the queue, is processed first

Basically it's just, take passenger in request order.

You need to change the controller class's and elevator class's functions. It is very subjective and the possibilities for changes is too much.

## Task 3: Shortest distance first

There is no explanation to this as shortest distance available on wikipedia or any reference are using Shortest Distance Algorithm such as Djikstra's, Floyd-Warshall etc. which is inappropriate but because elevator algorithm is a type of disk scheduling algorithm, there is one algorithm matched. It is called Shortest Seek First.

Based on [wikipedia](https://en.wikipedia.org/wiki/Shortest_seek_first), shortest seek first algorithm ..
> .. determines which request is closest to the current position of the head, and then services that request next.

Basically it's just, sort the request list by shortest distance from current floor to all user in request list.

You need to change the controller class's and elevator class's functions. It is very subjective and the possibilities for changes is too much.
