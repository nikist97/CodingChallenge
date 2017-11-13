from DataRandomizer import DataGenerator
from CustomErrors import InvalidPriceError, InvalidPositionError
from collections import deque
from math import log


class Event(object):
    """
    this class represents the model of an Event with a unique identifier and 0 or more positive ticket prices
    """

    currency = "$"  # the main currency used for the tickets is dollar

    def __init__(self, identifier, tickets):
        """
        constructor for an Event object
        :param identifier: the unique numeric identifier of the event
        :param tickets: the container with all the ticket prices
        :raises InvalidPriceError: if there is a ticker price <= 0
        :raises TypeError: if the identifier is not an integer
        """

        # ensure all tickets' prices are positive
        if not all(ticket > 0 for ticket in tickets):
            raise InvalidPriceError("All ticket prices must be greater than 0")

        # ensure the identifier is an integer
        if type(identifier) != int:
            raise TypeError("Identifier must be of type int")

        self.identifier = identifier
        self.tickets = tickets

    def get_id(self):
        """
        get a formatted string of the unique id of the event
        :return: a string of the id filled with 0s appended to its left so that the number of digits is equal to the
            number of digits of the maximum id for a ticket, for example if max ticket id might be 400, then id 4 will
            returned as '004' instead of '4'
        """

        num_of_digits = int(log((GridWorld.grid_size*2 + 1)**2, 10)) + 1

        formatted_id = str(self.identifier)
        if len(formatted_id) < num_of_digits:
            return "0"*(num_of_digits - len(formatted_id)) + formatted_id
        else:
            return formatted_id

    def get_minimum_ticket_price(self):
        """
        get the minimum ticket price from all ticket prices in this event
        :return: a formatted string of the minimum float from the collection of ticket prices, rounded to 2 digits after
            decimal point, 0s are also appended to the left to fit the format, e.g. 7.5 is returned as 07.50,
            if there are no tickets, 'N/A' is returned
        """

        if len(self.tickets) == 0:
            return "N/A"
        else:
            num_of_digits = len(str(DataGenerator.max_ticket_price))

            min_price = min(self.tickets)
            min_price = '{0:.2f}'.format(min_price)

            if len(min_price) < num_of_digits:
                return Event.currency + "0"*(num_of_digits - len(min_price)) + min_price
            else:
                return Event.currency + min_price


class GridWorld(object):
    """
    this class represents the model of a GridWorld containing a number of events
    """

    grid_size = 10  # half of the size of the grid, e.g. if this is 10, world is in range [-10, 10]

    def __init__(self, generate=True):
        """
        constructor for a GridWorld object
        :param generate: optional argument, True if data should be generated when initializing the object and False
            otherwise, default value is True
        """

        self.grid = []
        for row in range(self.grid_size*2 + 1):
            self.grid.append([None]*(self.grid_size*2 + 1))

        if generate:
            self.generate_data()

    def generate_data(self):
        """
        a method which generates random data in the world
        """

        DataGenerator.init_data(self, Event)

    def get_event(self, x, y):
        """
        a method which returns the event stored at position (x,y)
        :param x: the x coordinate
        :param y: the y coordinate
        :return: the event at position (x, y) or None if there is no event at the position
        """

        return self.grid[x + self.grid_size][y + self.grid_size]

    def register_event(self, event, i, j):
        """
        a method to register a new event in the world
        :param event: the event object to register
        :param i: the x coordinate of the event
        :param j: the y coordinate of the event
        :raises TypeError: if the event argument is not of type Event
        :raises InvalidPositionError: if the coordinates for the event are out of bounds
        """

        if type(event) != Event:
            raise TypeError("Event must be an object of type Event")

        if not ((-1*self.grid_size) <= i <= self.grid_size and (-1*self.grid_size) <= j <= self.grid_size):
            raise InvalidPositionError("Out of bounds coordinates when registering an event: {0}, {1}".format(i, j))

        self.grid[j + self.grid_size][i + self.grid_size] = event

    def get_nearest_positions(self, x, y, num_nearest_events):
        """
        a method which returns the nearest positions to an input position in which there is a registered event
        :param x: the input x coordinate
        :param y: the input y coordinate
        :param num_nearest_events: the number of nearest events to return
        :return: a list of points represented by a tuple (x,y) which are the nearest positions with an event
        :raises InvalidPositionError: when the input coordinates are out of bounds
        """

        if not ((-1*self.grid_size) <= x <= self.grid_size and (-1*self.grid_size) <= y <= self.grid_size):
            raise InvalidPositionError("Out of bounds coordinates when getting nearest events: {0}, {1}".format(x, y))

        x, y = x + self.grid_size, y + self.grid_size
        nearest_positions = []
        if num_nearest_events == 0:
            return nearest_positions

        # check if the input coordinates contain an event
        if self.grid[y][x] is not None:
            nearest_positions.append((x - self.grid_size, y - self.grid_size))

        # perform Breadth-First-Search to find the nearest events, by exploring neighbour positions
        explored = set()
        explored.add((x, y))
        fringe = deque()
        while len(nearest_positions) != num_nearest_events:
            for position in self.get_available_moves(x, y):
                if position in explored or position in fringe:
                    continue
                fringe.append(position)

            if len(fringe) == 0:
                break

            x, y = fringe.popleft()
            explored.add((x, y))
            if self.grid[y][x] is not None:
                nearest_positions.append((x - self.grid_size, y - self.grid_size))

        return nearest_positions

    def get_nearest_events(self, x, y, num_nearest_events=5):
        """
        a method to get the nearest events to an input position, prints the information about each of the nearest events
        :param x: the input x coordinate
        :param y: the input y coordinate
        :param num_nearest_events: optional argument, the number of nearest events to return, default value is 5
        """

        nearest_positions = self.get_nearest_positions(x, y, num_nearest_events)

        print("\nClosest Events to ({0},{1}):\n".format(x, y))
        for position in nearest_positions:
            event = self.grid[position[1] + self.grid_size][position[0] + self.grid_size]
            print("Event {0} - {1}, Distance {2}\n".format(event.get_id(), event.get_minimum_ticket_price(),
                                                           self.get_manhattan_distance(x, y, position[0], position[1])))

    def pretty_print_world(self):
        """
        a utility method which prints the 2D list representing the grid world
        """

        for row in self.grid:
            print(row)

    @staticmethod
    def get_available_moves(x, y):
        """
        a method, which returns the valid moves given an input position,
        expects the posituon to be positive, that is the indices of the 2D grid
        :param x: the x coordinate of the input position
        :param y: the y coordinate of the input position
        :return: all the valid moves that can be made given the input position
        :raises InvalidPositionError: if the input position is out of bounds
        """

        def valid(pos):
            """
            an inner function used to determine if a position is valid
            :param pos: the position to check, should be transformed to positive coordinates (indices of the grid)
            :return: true if the position is in bounds and false otherwise
            """

            return 0 <= pos[0] <= 2*GridWorld.grid_size and 0 <= pos[1] <= 2*GridWorld.grid_size

        # check for invalid input position
        if not valid((x, y)):
            raise InvalidPositionError("Out of bounds coordinates when getting available moves: {0}, {1}".format(x, y))

        # generate all possible moves
        positions = (x+1, y), (x, y+1), (x-1, y), (x, y-1)

        # return only those moves that are valid
        return (position for position in positions if valid(position))

    @staticmethod
    def get_manhattan_distance(x0, y0, x1, y1):
        """
        a static method, which computes the manhattan distance between 2 points
        :param x0: the x coordinate of the first point
        :param y0: the y coordinate of the first point
        :param x1: the x coordinate of the second point
        :param y1: the y coordinate of the second point
        :return: the manhattan distance between the two points
        """

        return abs(x1 - x0) + abs(y1 - y0)
