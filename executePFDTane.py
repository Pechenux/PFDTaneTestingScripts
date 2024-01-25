import desbordante


def execPFDTane(parameters):
    algo = desbordante.PFDTane()

    algo.load_data(parameters["TABLE"], parameters["SEPARATOR"], parameters["HAS_HEADER"])

    algo.execute(is_null_equal_null=parameters["ISNULLEQNULL"], error=parameters["ERROR"], error_measure=parameters["ERROR_MEASURE"], max_lhs=parameters["MAXLHS"])

    return algo.get_fds()
