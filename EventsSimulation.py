from DataModel import GridWorld
from CustomErrors import InvalidPositionError


def main():
    """
    a main method, which runs the simulation
    """

    world = GridWorld(generate=True)  # creates a grid world with randomly generated data

    while True:
        try:
            x, y = map(int, input("Please Input Coordinates:\n\n").split(","))
        except:
            break

        try:
            world.get_nearest_events(x, y)
        except InvalidPositionError:
            print("Out of bounds coordinates, please enter coordinates between {0} and {1} inclusive".format(-1*world.grid_size, world.grid_size))

if __name__ == "__main__":
    main()
