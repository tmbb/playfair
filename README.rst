Playfair
========

Introduction
------------

Playfair is a utility package to help with common tasks for research papers.
It's named after William Playfair, credited with creating a number of important visualization tools still used today.

Features
--------

Currently, Playfair provides graphical tools for data visualization, with special focus
for the kinds of plots commonly used in scientific papers in the biomedical sciences and
utilities to display data as part of Microsoft Word files.


Graphical Tools (using matplotlib)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from playfair.compare import add_comparisons_to_axes, Comparison, stars
    from matplotlib import pyplot as plt

    d1 = np.linspace(1, 2, 55)
    d2 = np.linspace(2, 2.5, 34)
    d3 = np.linspace(1.25, 3, 40)
    d4 = np.linspace(3.4, 5.5, 50)

    comp1 = Comparison(stars(1), d1, d2, 1, 2)
    comp2 = Comparison(stars(2), d3, d4, 3, 4)
    comp3 = Comparison(stars(3), d3, d4, 2, 3)
    comp4 = Comparison(stars(4), d2, d4, 2, 4)
    comp5 = Comparison(stars(5), d1, d3, 1, 3)
    comp6 = Comparison(stars(6), d1, d4, 1, 4)
    comps = [comp1, comp2, comp3, comp4, comp5, comp6]

    fig, ax = plt.subplots(1)
    ax.boxplot([d1, d2, d3, d4], labels=["A+", "B-", "C", "d-"])
    add_comparisons_to_axes(ax, comps, debug=False)
    ax.set_ylim(0, 12)
    fig.set_size_inches(6, 6)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    fig.savefig(os.path.join(dir_path, 'fixtures/output-example-1.png'))

.. image:: docs/_static/images/output-example-1.png

Docx Tools (interact with Microsoft Word files)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**TODO**

Contributing
------------

The scope of this package isn't currently well defined.
Contributions are welcome, including documentation improvements.
While 100% code coverage isn't necessary, code contributions should come with *some* testing coverage.
