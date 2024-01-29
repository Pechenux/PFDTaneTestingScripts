import desbordante


def execTane(parameters):
    algo = desbordante.Tane()

    algo.load_data(parameters["TABLE"], parameters["SEPARATOR"], parameters["HAS_HEADER"])

    algo.execute(error=parameters["ERROR"], error_measure=parameters["ERROR_MEASURE"])

    return algo.get_fds()
