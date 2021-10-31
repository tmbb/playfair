from matplotlib.lines import Line2D
from matplotlib import transforms, rcParams
from matplotlib import pylab


# 1pt = 1/27 inches
_pt = 1.0/72

_MIN = -1e20

def stars(n):
    return "✱" * n

class Comparison(object):

    def __init__(self, text, data1, data2, pos1=1, pos2=2):
        self.text = text
        self.data1 = data1
        self.data2 = data2
        self.pos1 = pos1
        self.pos2 = pos2

def _add_comparison_to_axes(axes, comparison, heights, nr_of_layers,
                            debug=False, **kwargs):

    font_size = rcParams['font.size']
    delta_y_bottom = (font_size * 1.4) * _pt
    delta_y_top = (font_size * 1.2) * _pt
    text_padding_bottom = (font_size * 0.6) * _pt

    fig = axes.get_figure()
    # Extract parameters from significance marker
    text = comparison.text
    data1 = comparison.data1
    data2 = comparison.data2
    pos1 = comparison.pos1
    pos2 = comparison.pos2

    dy_left = heights.get(pos1, _MIN)
    dy_right = heights.get(pos2, _MIN)
    # the dy for the horizontal bar must be higher than the y-position
    # for markers so that the new marker remains above all the ones
    # that were added before
    dy_middle = max(heights.get(pos, _MIN) for pos in range(pos1, pos2 + 1))

    # We need to account for the number of layers.
    # The number of layers reflects the number of stacked comparisons.
    # The number of layers is relevant for the placement of the left, middle and right segments.

    # The number of layers we need to account for when drawing the s1, s2, s4, and s5 segments
    # is quite obvious
    nr_of_layers_left = nr_of_layers.get(pos1, 0)
    nr_of_layers_right = nr_of_layers.get(pos2, 0)
    # The number of layers we need to account for when drawing the s3 segment is more complex.
    # We need to account for all layers between pos1 and pos2, so we simply take the maximum.
    nr_of_layers_middle = max(nr_of_layers.get(pos, 0) for pos in range(pos1, pos2 + 1))

    color = kwargs.get('color', 'black')
    linewidth = kwargs.get('linewidth', 1)

    if debug:
        cm = pylab.get_cmap('Set1')
        [color_s1, color_s2, color_s3, color_s4, color_s5] = \
            list(cm(1.*i/5) for i in range(5))
    else:
        [color_s1, color_s2, color_s3, color_s4, color_s5] = \
            [color, color, color, color, color]

    figure = axes.get_figure()
    delta_y_total = delta_y_bottom + delta_y_top + text_padding_bottom

    delta_y_bottom_left = delta_y_bottom + (delta_y_total * nr_of_layers_left)
    delta_y_bottom_right = delta_y_bottom + (delta_y_total * nr_of_layers_right)
    delta_y_bottom_middle = max([
        delta_y_bottom_left,
        delta_y_bottom_right,
        delta_y_bottom + (delta_y_total * nr_of_layers_middle)
    ])

    delta_y_text = delta_y_bottom_middle + delta_y_top + text_padding_bottom

    max_left = max(max(data1), dy_left)
    max_right = max(max(data2), dy_right)
    max_all = max(max(max_left, max_right), dy_middle)


    offset_s1 = transforms.ScaledTranslation(0, delta_y_bottom_left, fig.dpi_scale_trans)
    transform_s1 = axes.transData + offset_s1
    s1 = Line2D([pos1, pos1], [max_left, max_all],
                transform=transform_s1,
                color=color_s1,
                linewidth=linewidth,
                label="s1",
                **kwargs)

    offset_s2 = transforms.ScaledTranslation(pos1, max_all, axes.transData)
    transform_s2 = fig.dpi_scale_trans + offset_s2
    s2 = Line2D([0, 0], [delta_y_bottom_left, delta_y_bottom_middle + delta_y_top],
                transform=transform_s2,
                color=color_s2,
                linewidth=linewidth,
                label='s2',
                **kwargs)

    offset_s3 = transforms.ScaledTranslation(0, delta_y_bottom_middle + delta_y_top, fig.dpi_scale_trans)
    transform_s3 = axes.transData + offset_s3
    s3 = Line2D([pos1, pos2], [max_all, max_all],
                transform=transform_s3,
                color=color_s3,
                linewidth=linewidth,
                label='s3',
                **kwargs)

    offset_s4 = transforms.ScaledTranslation(pos2, max_all, axes.transData)
    transform_s4 = fig.dpi_scale_trans + offset_s4
    s4 = Line2D([0, 0], [delta_y_bottom_right, delta_y_bottom_middle + delta_y_top],
                transform=transform_s4,
                color=color_s4,
                linewidth=linewidth,
                label='s4',
                **kwargs)

    offset_s5 = transforms.ScaledTranslation(0, delta_y_bottom_right, fig.dpi_scale_trans)
    transform_s5 = axes.transData + offset_s5
    s5 = Line2D([pos2, pos2], [max_right, max_all],
                transform=transform_s5,
                color=color_s5,
                linewidth=linewidth,
                label='s5',
                **kwargs)

    for line_segment in [s1, s2, s3, s4, s5]:
        axes.add_line(line_segment)

    q_x = (pos1 + pos2)/2
    q_y = max_all

    offset_text = transforms.ScaledTranslation(0, delta_y_text, fig.dpi_scale_trans)
    transform_text = axes.transData + offset_text
    label = axes.text(q_x, q_y, text,
                      horizontalalignment='center',
                      transform=transform_text)

    return (max_all, label)

def add_comparisons_to_axes(axes, comparisons, **kwargs):
    """
    Add pairwise comparisons to plots in the same axis.

    Comparisons will stack automatically in order to avoid overlapping,
    but you might have to manually adjust the axis limits to guarantee
    that comparison markers are drawn inside the axes
    (otherwise they will be invisible)
    """
    heights = dict()
    nr_of_layers = dict()
    last_label = None
    for marker in comparisons:
        pos1 = marker.pos1
        pos2 = marker.pos2
        (max_height, label) = _add_comparison_to_axes(axes, marker, heights, nr_of_layers, **kwargs)
        last_label = label
        # range(a, b) is exclusive on the upper bound
        nr_of_layers_for_envelopped_positions = max(nr_of_layers.get(p, 0) for p in range(pos1, pos2 + 1)) + 1
        for pos in range(pos1, pos2 + 1):
            # Update the heights for all the positions between
            # the start and end positions of the marker
            heights[pos] = max_height
            # Update the number of layers above pos
            # the number of layers is important to correctly account
            # for the data-independent padding
            nr_of_layers[pos] = nr_of_layers_for_envelopped_positions

    # We save this data in the axes in case we want to do something with it in the future
    axes.__comparison_data = (heights, nr_of_layers)

    return (heights, nr_of_layers)