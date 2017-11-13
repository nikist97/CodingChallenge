from DataModel import GridWorld


def main():
    """
    a main method, which runs the simulation
    """

    world = GridWorld(generate=True)  # creates a grid world with randomly generated data

    x, y = map(int, input("Please Input Coordinates:\n\n").split(","))
    world.get_nearest_events(x, y)

if __name__ == "__main__":
    main()
