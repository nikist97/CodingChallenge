from DataModel import GridWorld
from CustomErrors import InvalidPositionError


def main():
    """
    a main method, which runs the simulation
    """

    world = GridWorld(generate=True)  # creates a grid world with randomly generated data

    while True:
        input_pos = input("Please Input Coordinates:\n\n")
        if input_pos == "q" or input_pos == "quit":
            break

        try:
            x, y = map(int, input_pos.split(","))
        except:
            print("Invalid format of the input position: positions should be in format: x, y")
            continue

        try:
            world.get_nearest_events(x, y)
        except InvalidPositionError:
            print("Out of bounds coordinates, please enter coordinates between {0} and {1} inclusive".format(-1*world.grid_size, world.grid_size))

if __name__ == "__main__":
    main()
