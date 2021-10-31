
def round_to_nr_of_decimal_places(n, nr_of_places):
    return ("{:.%if}" % nr_of_places).format(n)