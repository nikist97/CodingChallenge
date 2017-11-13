import unittest
from CustomErrors import InvalidPriceError, InvalidPositionError
from DataModel import GridWorld, Event


class SimulationTests(unittest.TestCase):

    def setUp(self):
        """
        sets up objects used in the tests
        """

        self.world = GridWorld(generate=False)
        self.event = Event(1, [])

    def test_event(self):
        """
        tests the methods of the Event class
        """

        # test whether the required errors are thrown at initialisation
        with self.assertRaises(TypeError):
            Event("id", [])

        with self.assertRaises(TypeError):
            Event(1, 1)

        with self.assertRaises(InvalidPriceError):
            Event(10, [-1, 0, 2])

        # test the get_id method
        self.assertEqual(self.event.get_id(), "001", "Wrong formatting of event id with 1 digit")
        self.event.identifier = 11
        self.assertEqual(self.event.get_id(), "011", "Wrong formatting of event id with 2 digits")
        self.event.identifier = 111
        self.assertEqual(self.event.get_id(), "111", "Wrong formatting of event id with 3 digits")

        # test the get_minimum_ticket_price method
        self.assertEqual(self.event.get_minimum_ticket_price(), "N/A",
                         "Wrong result for min ticket for event with empty list of tickets")
        self.event.tickets = (3, 10.0, 4.1, 74.54, 2)
        self.assertEqual(self.event.get_minimum_ticket_price(), Event.currency + "02.00",
                         "Wrong formatting for min ticket price with 1 digit")
        self.event.tickets = [9.5]
        self.assertEqual(self.event.get_minimum_ticket_price(), Event.currency + "09.50",
                         "Wrong formatting for min ticket price with 2 digits")
        self.event.tickets = (7.54, 10)
        self.assertEqual(self.event.get_minimum_ticket_price(), Event.currency + "07.54",
                         "Wrong formatting for min ticket price with 3 digits")

    def test_world(self):
        """
        tests the methods of the GridWorld class
        """

        # test the register_event method
        with self.assertRaises(TypeError):
            self.world.register_event(None, 5, 5)
        with self.assertRaises(TypeError):
            self.world.register_event(self.event, "5", 5)
        with self.assertRaises(InvalidPositionError):
            self.world.register_event(self.event, 5, self.world.grid_size + 5)

        self.world.register_event(self.event, 0, 0)
        self.assertEqual(self.world.get_event(0, 0), self.event, "Event not registered or registered at invalid point")

        # test the get_nearest_positions method
        with self.assertRaises(TypeError):
            self.world.get_nearest_positions("5", 0, 2)
        with self.assertRaises(InvalidPositionError):
            self.world.get_nearest_positions(self.world.grid_size*2, 0, 2)

        self.world.register_event(Event(2, []), 0, 2)
        self.world.register_event(Event(3, [1]), 2, 1)
        self.world.register_event(Event(4, [4, 5]), -2, -1)
        self.assertEqual(self.world.get_nearest_positions(0, 0, 0), [],
                         "Nearest positions should be an empty list if 0 is given as argument for the number of events")

        positions = self.world.get_nearest_positions(0, 0, 1)
        self.assertEqual(len(positions), 1, "Wrong number of events returned as nearest events")
        self.assertEqual(positions[0], (0, 0), "Wrong event returned as nearest event")
        positions = self.world.get_nearest_positions(0, 0, 3)
        self.assertEqual(positions, [(0, 0), (0, 2), (2, 1)], "Wrong events returned when searching for nearest events")
        positions = self.world.get_nearest_positions(2, 2, 10)
        self.assertEqual(positions, [(2, 1), (0, 2), (0, 0), (-2, -1)],
                         "Wrong events returned when searching for more events than there are in the grid world")

    def test_static_methods(self):
        """
        tests the static methods of the GridWorld class
        """

        # test the get_manhattan_distance method
        with self.assertRaises(TypeError):
            self.world.get_manhattan_distance("2", 0, 0, 1)

        self.assertEqual(self.world.get_manhattan_distance(0, 0, 1, 1), 2,
                         "Wrong manhattan distance returned with positive inputs")
        self.assertEqual(self.world.get_manhattan_distance(-1, -2, -5, -7), 9,
                         "Wrong manhattan distance returned with negative inputs")
        self.assertEqual(self.world.get_manhattan_distance(-1, 2, 5, -7), 15,
                         "Wrong manhattan distance returned with mixed inputs")

        # test the get_available_moves method
        with self.assertRaises(InvalidPositionError):
            self.world.get_available_moves(-1, 1)
        with self.assertRaises(TypeError):
            self.world.get_available_moves(0, "0")

        positions = tuple(self.world.get_available_moves(0, 0))
        self.assertEqual(positions, ((1, 0), (0, 1)), "Wrong positions returned with boundary case (0, 0)")
        positions = tuple(self.world.get_available_moves(10, 10))
        self.assertEqual(positions, ((11, 10), (10, 11), (9, 10), (10, 9)),
                         "Wrong positions returned in middle case with all available directions")
        positions = tuple(self.world.get_available_moves(20, 20))
        self.assertEqual(positions, ((19, 20), (20, 19)), "Wrong positions returned with boundary case (20, 20)")


if __name__ == "__main__":
    unittest.main()
