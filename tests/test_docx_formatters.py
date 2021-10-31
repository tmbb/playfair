from playfair.docx import *

from docx import Document
from hypothesis import given
from hypothesis.strategies import floats, integers

def test_can_get_new_styled_document():
    new_styled_document()

@given(floats())
def test_integer_formatter(value):
    formatter = IntegerFormatter()
    text = formatter.as_plaintext(value)
    assert (text in ['+∞', '-∞', 'NaN'] or (text == str(int(value))))


@given(floats())
def test_default_formatter(value):
    formatter = DefaultFormatter()
    text = formatter.as_plaintext(value)
    assert text == str(value)


@given(floats(), integers(min_value=1, max_value=6))
def test_default_formatter_if_more_than_1_decimal_place_then_the_text_contains_a_dot(
        value,
        nr_of_decimal_places):

    formatter = RoundedFormatter(nr_of_decimal_places)
    text = formatter.as_plaintext(value)
    assert (text in ['+∞', '-∞', 'NaN']) or ("." in text)

@given(floats())
def test_default_formatter_if_0_decimal_places_then_the_text_doesnt_contain_a_dot(
        value):

    formatter = RoundedFormatter(0)
    text = formatter.as_plaintext(value)
    assert "." not in text

@given(floats(), floats())
def test_truncated_formatter_lower_end(value, bound):
    formatter = TruncatedFormatter(steps_less_than=[bound])
    text = formatter.as_plaintext(value)

    if value < bound:
        assert "< " in text
        number_part = text[2:]
        # the value is either rendered as a "pretty float" or as a normal float
        # If the text is not one of the "pretty floats", it must be possible
        # to parse it as a float
        if number_part not in ['+∞', '-∞', 'NaN']:
            float(number_part)
    else:
        assert "<" not in text
        # the value is either rendered as a "pretty float" or as a normal float
        # If the text is not one of the "pretty floats", it must be possible
        # to parse it as a float
        if text not in ['+∞', '-∞', 'NaN']:
            float(text)

@given(floats(), floats())
def test_truncated_formatter_upper_end(value, bound):
    formatter = TruncatedFormatter(steps_greater_than=[bound])
    text = formatter.as_plaintext(value)

    if value > bound:
        assert "> " in text
        number_part = text[2:]
        # the value is either rendered as a "pretty float" or as a normal float
        # If the text is not one of the "pretty floats", it must be possible
        # to parse it as a float
        if number_part not in ['+∞', '-∞', 'NaN']:
            float(number_part)
    else:
        assert ">" not in text
        # the value is either rendered as a "pretty float" or as a normal float
        # If the text is not one of the "pretty floats", it must be possible
        # to parse it as a float
        if text not in ['+∞', '-∞', 'NaN']:
            float(text)

@given(floats(allow_nan=False), floats(allow_nan=False), floats(allow_nan=False))
def test_truncated_formatter_both_ends_middle(a, b, c):
    [lower, value, upper] = sorted([a, b, c])

    formatter = TruncatedFormatter(steps_less_than=[lower], steps_greater_than=[upper])
    text = formatter.as_plaintext(value)

    # the value is either rendered as a "pretty float" or as a normal float
    # If the text is not one of the "pretty floats", it must be possible
    # to parse it as a float
    assert "<" not in text
    assert ">" not in text
    if text not in ['+∞', '-∞', 'NaN']:
        float(text)

@given(floats(allow_nan=False), floats(allow_nan=False), floats(allow_nan=False))
def test_truncated_formatter_both_ends_lower(a, b, c):
    [value, lower, upper] = sorted([a, b, c])

    formatter = TruncatedFormatter(steps_less_than=[lower], steps_greater_than=[upper])
    text = formatter.as_plaintext(value)

    # Remember that we can have lower == upper if a == b, b == c or c == a
    if value < lower:
        assert "< " in text
        number_part = text[2:]
        # the value is either rendered as a "pretty float" or as a normal float
        # If the text is not one of the "pretty floats", it must be possible
        # to parse it as a float
        if number_part not in ['+∞', '-∞', 'NaN']:
            float(number_part)
    else:
        assert "<" not in text
        # the value is either rendered as a "pretty float" or as a normal float
        # If the text is not one of the "pretty floats", it must be possible
        # to parse it as a float
        if text not in ['+∞', '-∞', 'NaN']:
            float(text)

@given(floats(allow_nan=False), floats(allow_nan=False), floats(allow_nan=False))
def test_truncated_formatter_both_ends_upper(a, b, c):
    [lower, upper, value] = sorted([a, b, c])

    formatter = TruncatedFormatter(steps_less_than=[lower], steps_greater_than=[upper])
    text = formatter.as_plaintext(value)

    # Remember that we can have lower == upper if a == b, b == c or c == a
    if value > upper:
        assert "> " in text
        number_part = text[2:]
        # the value is either rendered as a "pretty float" or as a normal float
        # If the text is not one of the "pretty floats", it must be possible
        # to parse it as a float
        if number_part not in ['+∞', '-∞', 'NaN']:
            float(number_part)
    else:
        assert ">" not in text
        # the value is either rendered as a "pretty float" or as a normal float
        # If the text is not one of the "pretty floats", it must be possible
        # to parse it as a float
        if text not in ['+∞', '-∞', 'NaN']:
            float(text)


@given(floats(), floats())
def test_truncated_p_value_formatter_lower_end(value, bound):
    formatter = TruncatedPValueFormatter(steps_less_than=[bound])
    text = formatter.as_plaintext(value)

    if value < bound:
        assert "p < " in text
        number_part = text[4:]
        # the value is either rendered as a "pretty float" or as a normal float
        # If the text is not one of the "pretty floats", it must be possible
        # to parse it as a float
        if number_part not in ['+∞', '-∞', 'NaN']:
            float(number_part)
    else:
        assert "p <" not in text
        assert "p = " in text
        number_part = text[4:]
        # the value is either rendered as a "pretty float" or as a normal float
        # If the text is not one of the "pretty floats", it must be possible
        # to parse it as a float
        if number_part not in ['+∞', '-∞', 'NaN']:
            float(number_part)


@given(floats(), floats())
def test_truncated_p_value_formatter_upper_end(value, bound):
    formatter = TruncatedPValueFormatter(steps_less_than=[], steps_greater_than=[bound])
    text = formatter.as_plaintext(value)

    if value > bound:
        assert "> " in text
        number_part = text[4:]
        # the value is either rendered as a "pretty float" or as a normal float
        # If the text is not one of the "pretty floats", it must be possible
        # to parse it as a float
        if number_part not in ['+∞', '-∞', 'NaN']:
            float(number_part)
    else:
        assert ">" not in text
        assert "p = " in text
        number_part = text[4:]
        # the value is either rendered as a "pretty float" or as a normal float
        # If the text is not one of the "pretty floats", it must be possible
        # to parse it as a float
        if number_part not in ['+∞', '-∞', 'NaN']:
            float(number_part)


@given(floats(allow_nan=False), floats(allow_nan=False), floats(allow_nan=False))
def test_truncated_p_value_formatter_both_ends_middle(a, b, c):
    [lower, value, upper] = sorted([a, b, c])

    formatter = TruncatedPValueFormatter(steps_less_than=[lower], steps_greater_than=[upper])
    text = formatter.as_plaintext(value)

    # the value is either rendered as a "pretty float" or as a normal float
    # If the text is not one of the "pretty floats", it must be possible
    # to parse it as a float
    assert "p <" not in text
    assert ">" not in text
    assert "p = " in text
    number_part = text[4:]
    # the value is either rendered as a "pretty float" or as a normal float
    # If the text is not one of the "pretty floats", it must be possible
    # to parse it as a float
    if number_part not in ['+∞', '-∞', 'NaN']:
        float(number_part)


@given(floats(allow_nan=False), floats(allow_nan=False), floats(allow_nan=False))
def test_truncated_p_value_formatter_both_ends_lower(a, b, c):
    [value, lower, upper] = sorted([a, b, c])

    formatter = TruncatedPValueFormatter(steps_less_than=[lower], steps_greater_than=[upper])
    text = formatter.as_plaintext(value)

    # Remember that we can have lower == upper if a == b, b == c or c == a
    if value < lower:
        assert "p < " in text
        number_part = text[4:]
        # the value is either rendered as a "pretty float" or as a normal float
        # If the text is not one of the "pretty floats", it must be possible
        # to parse it as a float
        if number_part not in ['+∞', '-∞', 'NaN']:
            float(number_part)
    else:
        assert "p <" not in text
        assert "p = " in text
        number_part = text[4:]
        # the value is either rendered as a "pretty float" or as a normal float
        # If the text is not one of the "pretty floats", it must be possible
        # to parse it as a float
        if number_part not in ['+∞', '-∞', 'NaN']:
            float(number_part)


@given(floats(allow_nan=False), floats(allow_nan=False), floats(allow_nan=False))
def test_truncated_p_value_formatter_both_ends_upper(a, b, c):
    [lower, upper, value] = sorted([a, b, c])

    formatter = TruncatedPValueFormatter(steps_less_than=[lower], steps_greater_than=[upper])
    text = formatter.as_plaintext(value)

    # Remember that we can have lower == upper if a == b, b == c or c == a
    if value > upper:
        assert "> " in text
        number_part = text[4:]
        # the value is either rendered as a "pretty float" or as a normal float
        # If the text is not one of the "pretty floats", it must be possible
        # to parse it as a float
        if number_part not in ['+∞', '-∞', 'NaN']:
            float(number_part)
    else:
        assert ">" not in text
        assert "p = " in text
        number_part = text[4:]
        # the value is either rendered as a "pretty float" or as a normal float
        # If the text is not one of the "pretty floats", it must be possible
        # to parse it as a float
        if number_part not in ['+∞', '-∞', 'NaN']:
            float(number_part)
