# Coding Challenge

### Compilation and execution
* Language used - Python v3.6
* Main method located in EventsSimulation.py file
* To run it, type the following command from terminal:
```
python EventsSimulation.py
```

### Assumptions
* The different tickets in an event represent different types of tickets for the given event
* From the first assumption follows that each ticket in a given event has a unique price
* Maximum number of different ticket types in an event is 15
* Minimum ticket price is $1.00
* Maximum ticket price is $100.00
* The program should output 'N/A' for the minimum ticket price of a nearest event with 0 ticket types

### Answers to questions in the specification
1) Support for multiple events at the same location - since each event has a unique identifier, I can support multiple 
events at a single location by having a map (dictionary in python) at the given location linking the unique identifier 
of the event to the event object itself. Thus, when exploring a given location, I would have to iterate through the map 
of events at the given location.

2) Working with much larger world size - to handle this scenario, I could divide the world into regions of some size,
where at each location of the grid I will have a given Region object and, thus, significantly decrease the world size. 
Each Region object will contain a number of events which as explained in question 1) could suitably be stored at a map 
linking event IDs with the event objects. This, however, will require one more change when searching through the grid 
for the closest events - currently, the search method I use is Breadth-First-Search since the path cost from one 
location to a neighbourhood location next to it is always 1. When working with regions, however, this will not be the 
case since the distance between a Region and its neighbourhood Regions is not necessarily the same and is definitely not 
a constant. Therefore, I will have to use Uninformed-Cost-Search, which expands new nodes in a sequence based on the 
path from the root node. In other words, Uninformed-Cost-Search will explore the Region closest to the input position 
first and then proceeding with the second closest Region and so on, which is exactly what we need in the search problem.
