def make_example_image_1():
    from playfair.compare import add_comparisons_to_axes, Comparison, stars
    from matplotlib import pyplot as plt
    import numpy as np

    # Generate some data
    d1 = np.linspace(1, 2, 55)
    d2 = np.linspace(2, 2.5, 34)

    # Create a comparison marker between populations at the positions 1 and 2.
    comparison_marker = Comparison("$p < 0.01$", d1, d2, 1, 2)

    fig, ax = plt.subplots(1)
    # Add a normal boxplot
    ax.boxplot([d1, d2], labels=["Left", "Right"])
    add_comparisons_to_axes(ax, [comparison_marker])

    # Set the ylims manually because matplotlib isn't smart enough
    # to scale things such that the markers fit in the plot
    ax.set_ylim(0, 3.5)
    fig.savefig('docs/_static/images/example1.png')


def make_example_image_2():
    from playfair.compare import add_comparisons_to_axes, Comparison, stars
    from matplotlib import pyplot as plt
    import numpy as np

    # Generate some data
    d1 = np.linspace(1, 2, 55)
    d2 = np.linspace(2, 2.5, 34)
    d3 = np.linspace(1.35, 1.70, 55)

    # Create a comparison marker between populations at the positions 1 and 2.
    comparison_marker_1 = Comparison("$p < 0.01$", d1, d2, 1, 2)
    # Create a comparison marker between populations at the positions 1 and 3.
    comparison_marker_2 = Comparison("$p < 0.05$", d1, d2, 1, 3)

    fig, ax = plt.subplots(1)
    # Add a normal boxplot
    ax.boxplot([d1, d2, d3], labels=["A", "B", "C"])
    add_comparisons_to_axes(ax, [comparison_marker_1, comparison_marker_2])

    # Set the ylims manually because matplotlib isn't smart enough
    # to scale things such that the markers fit in the plot
    ax.set_ylim(0, 4)
    fig.savefig('docs/_static/images/example2.png')


if __name__ == '__main__':
    make_example_image_1()
    make_example_image_2()
