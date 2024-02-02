import desbordante


def execfullTane(parameters):
    algo = desbordante.Tane()

    algo.load_data(parameters["TABLE"], parameters["SEPARATOR"], parameters["HAS_HEADER"])

    algo.execute(error=parameters["ERROR"])

    return algo.get_fds()

def loadTane(parameters):
    algo = desbordante.Tane()

    algo.load_data(parameters["TABLE"], parameters["SEPARATOR"], parameters["HAS_HEADER"])

    return algo

def execTane(algo, parameters):
    algo.execute(error=parameters["ERROR"])

    return algo.get_fds()