from random import randint, uniform


class DataGenerator(object):
    """
    a utility class providing static methods for random data generation, e.g. generate random number of events, random
    position for an event, random price for a ticket, etc.
    """

    max_num_of_tickers = 15  # this is the maximum number of tickets allowed for a single event

    max_ticket_price = 100.00  # this is the maximum price allowed for a single ticket

    min_ticket_price = 1.00  # this it the minimum price allowed for a single ticket

    @staticmethod
    def generate_number_of_events(max_number):
        """
        a static method, which generates a random number of events for the grid world
        :param max_number: the maximum number of events allowed, this should be the area of the grid world
        :return: a random integer between 1 and max_number inclusive
        """

        return randint(1, max_number)

    @staticmethod
    def generate_available_position(unavailable_positions, max_position):
        """
        a static method, which generates a random position for a new event
        :param unavailable_positions: a container object containing all unavailable positions
            (preferably a set to ensure O(1) complexity of the contains operation)
        :param max_position: an integer representing the maximum coordinate allowed
        :return: a point (x, y) represented in a tuple, which is not contained in unavailable_positions
        """

        x = randint(0, max_position)
        y = randint(0, max_position)
        position = (x, y)
        while position in unavailable_positions:
            x = randint(0, max_position)
            y = randint(0, max_position)
            position = (x, y)

        return position

    @staticmethod
    def generate_event_tickets():
        """
        a static method, which generates a collection of unique prices for tickets
        :return: a tuple of unique ticket prices (integers)
        """

        tickets = set()  # a set is used to ensure the uniqueness of the ticket prices

        num_of_tickets = randint(0, DataGenerator.max_num_of_tickers + 1)
        while len(tickets) != num_of_tickets:
            tickets.add(round(uniform(DataGenerator.min_ticket_price, DataGenerator.max_ticket_price), 2))

        return tuple(tickets)  # return a tuple instead of the set to ensure immutability of the tickets

    @staticmethod
    def init_data(world, data_type):
        """
        this is the main static method to be called in order to generate random data for the simulation, it generates
        a random number of events with random data and registers those events in the world
        :param world: the reference to the GridWorld object
        :param data_type: this is the type of data stored in the grid world, in the simulation Event should be used,
            since the world contains Event objects
        """

        # generate a number of events, the max number allowed is the whole area of the world, so if world is [-10;10]
        # then max number should be 21*21
        number_of_events = DataGenerator.generate_number_of_events((world.grid_size*2 + 1) ** 2)

        unavailable_positions = set()  # set is used to store the already in use positions to ensure fast 'contains'

        for i in range(0, number_of_events, 1):
            # generate available position for the new event
            x, y = DataGenerator.generate_available_position(unavailable_positions, world.grid_size*2)
            x -= world.grid_size
            y -= world.grid_size

            # generate new object of type 'data_type', in this case this is object of type Event
            event = data_type(i, DataGenerator.generate_event_tickets())
            # register the event
            world.register_event(event, x, y)
