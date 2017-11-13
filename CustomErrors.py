class InvalidPriceError(ValueError):
    """
    a custom type of error raised when there is an invalid price for a ticket, e.g. negative number for price
    """

    def __init__(self, msg):
        """
        the constructor for the error calls the parent's (ValueError) constructor
        :param msg: the msg of the error
        """

        super(InvalidPriceError, self).__init__(msg)


class InvalidPositionError(ValueError):
    """
    a custom type of error raised when there is an invalid position for an event, e.g. out of bounds coordinates
    """

    def __init__(self, msg):
        """
        the constructor for the error calls the parent's (ValueError) constructor
        :param msg: the msg of the error
        """

        super(InvalidPositionError, self).__init__(msg)


class DuplicateIdentifierError(KeyError):
    """
    a custom type of error raised when there is a duplicate identifier for en event, e.g when registering a new event
    """

    def __init__(self, msg):
        """
        the constructor for the error calls the parent's (KeyError) constructor
        :param msg: the msg of the error
        """

        super(DuplicateIdentifierError, self).__init__(msg)
