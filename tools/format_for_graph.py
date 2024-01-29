def format_for_graph(error, point_h):
    return f"({error}, {point_h[0]}) += ({error}, {point_h[1]}) -= ({error}, {point_h[1]})\n"