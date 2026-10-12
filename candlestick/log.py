"""Console logging."""


def log(txt):
    """
    Prints the given text to the console with immediate flushing.

    This is particularly useful when running within a Docker container
    as it ensures logs are streamed and visible in real-time.

    Args:
        txt (str): The text to be printed.
    """
    print(txt, flush=True)
