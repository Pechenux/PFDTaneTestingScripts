import desbordante


def execfullPFDTane(parameters):
    algo = desbordante.PFDTane()

    algo.load_data(parameters["TABLE"], parameters["SEPARATOR"], parameters["HAS_HEADER"])

    algo.execute(error=parameters["ERROR"], error_measure=parameters["ERROR_MEASURE"])

    return algo.get_fds()

def loadPFDTane(parameters):
    algo = desbordante.PFDTane()

    algo.load_data(parameters["TABLE"], parameters["SEPARATOR"], parameters["HAS_HEADER"])

    return algo

def execPFDTane(algo, parameters):
    algo.execute(error=parameters["ERROR"], error_measure=parameters["ERROR_MEASURE"])

    return algo.get_fds()