"""Library for formatting numbers using SI prefixes."""

from __future__ import annotations

import math


class _SiPrefix:
    """Class to represent SI prefixes.

    Examples
    --------
    >>> si_prefix = _SiPrefix("y", "yocto", -24)
    >>> si_prefix.short_name
    'y'

    """

    short_name: str
    long_name: str
    exponent: int

    def __init__(
        self,
        short_name: str,
        long_name: str,
        exponent: int,
    ) -> None:
        self.short_name = short_name
        self.long_name = long_name
        self.exponent = exponent

    def get_e_string(self) -> str:
        return f"e{self.exponent}"


SI_PREFIXES: list[_SiPrefix] = [
    _SiPrefix("y", "yocto", -24),
    _SiPrefix("z", "zepto", -21),
    _SiPrefix("a", "atto", -18),
    _SiPrefix("f", "femto", -15),
    _SiPrefix("p", "pico", -12),
    _SiPrefix("n", "nano", -9),
    _SiPrefix("µ", "micro", -6),
    _SiPrefix("m", "milli", -3),
    _SiPrefix("", "", 0),
    _SiPrefix("k", "kilo", 3),
    _SiPrefix("M", "mega", 6),
    _SiPrefix("G", "giga", 9),
    _SiPrefix("T", "tera", 12),
    _SiPrefix("P", "peta", 15),
    _SiPrefix("E", "exa", 18),
    _SiPrefix("Z", "zetta", 21),
    _SiPrefix("Y", "yotta", 24),
]


def _split(value: float, precision: int = 1) -> tuple[float, int]:
    """Split a SI-Prefixed value into a value and an exponent of 10.

    Split `value` into value and "exponent-of-10", where "exponent-of-10" is a
    multiple of 3.  This corresponds to SI prefixes.
    Returns tuple, where the second value is the "exponent-of-10" and the first
    value is `value` divided by the "exponent-of-10".

    Parameters
    ----------
    value : int, float
        Input value.
    precision : int
        Number of digits after decimal place to include.

    Returns
    -------
    tuple
        The second value is the "exponent-of-10" and the first value is `value`
        divided by the "exponent-of-10".

    Examples
    --------
    >>> _split(0.04784)
    (47.8, -3)

    >>> _split(4781.123)
    (4.8, 3)

    >>> _split(-0.04784, 2)
    (-47.84, -3)

    >>> _split(-0)
    (0.0, 0)

    >>> _split(0)
    (0.0, 0)

    >>> _split(1e29)
    (100.0, 27)

    >>> _split(1e-27)
    (1.0, -27)

    See Also
    --------
    with_format : for more examples.

    """
    negative = False

    if value < 0.0:
        value = -value
        negative = True
    elif value == 0.0:
        return 0.0, 0

    exp_of_10 = int(math.log10(value))
    exp_of_10 = exp_of_10 // 3 * 3 if exp_of_10 > 0 else (-exp_of_10 + 3) // 3 * -3

    value *= 10 ** (-exp_of_10)

    thousand = 1e3

    if value >= thousand:
        value /= 1000.0
        exp_of_10 += 3

    if negative:
        value *= -1

    return round(value, precision), int(exp_of_10)


def _prefix(exp_of_10: int) -> str:
    """Return the SI prefix character associated with an exponent of 10.

    Parameters
    ----------
    exp_of_10 : int
        Exponent of a power of 10 associated with a SI unit
        character.

    Returns
    -------
        str : One of the characters in the SI_PREFIXES list.

    Examples
    --------
    >>> _prefix(-24)
    'y'

    Negative test case
    >>> _prefix(30)
    Traceback (most recent call last):
        ...
    ValueError: Exponent out range of available prefixes.

    """
    # Check if the exponent is any of the SI prefixes
    for si_prefix in SI_PREFIXES:
        if exp_of_10 == si_prefix.exponent:
            return si_prefix.short_name
    msg = "Exponent out range of available prefixes."
    raise ValueError(msg)


def with_format(
    value: float,
    precision: int = 1,
    format_str: str = "{value} {prefix}",
    exp_format_str: str = "{value}e{exp_of_10}",
) -> str:
    """Return SI Formatted number string.

    Format `value` to a string with SI prefix, using the specified precision.

    Parameters
    ----------
    value : float
        Input value.
    precision : int
        Number of digits after decimal place to include.
    format_str : str or unicode
        Format string where ``{prefix}`` and ``{value}`` represent the SI
        prefix and the value (scaled according to the prefix), respectively.
        The default format matches the `SI prefix style` format.
    exp_format_str : str or unicode
        Format string where ``{exp_of_10}`` and ``{value}`` represent the
        exponent of 10 and the value (scaled according to the exponent of 10),
        respectively.  This format is used if the absolute exponent of 10 value
        is greater than 24.

    Returns
    -------
        str: `value` formatted according to the `SI prefix style`.

    Examples
    --------
    >>> with_format(0.04781, 2)
    '47.81 m'

    >>> with_format(4781.123, 2)
    '4.78 k'

    >>> with_format(0.04781, 3)
    '47.810 m'

    >>> with_format(4781.123, 3)
    '4.781 k'

    >>> with_format(1e-27)
    '1.0e-27'

    >>> with_format(1.764e-24)
    '1.8 y'

    >>> with_format(7.4088e-23, 2)
    '74.09 y'

    >>> with_format(3.1117e-21, 2)
    '3.11 z'

    >>> with_format(1.30691e-19, 2)
    '130.69 z'

    >>> with_format(5.48903e-18, 2)
    '5.49 a'

    >>> with_format(2.30539e-16, 2)
    '230.54 a'

    >>> with_format(9.68265e-15, 2)
    '9.68 f'

    >>> with_format(4.06671e-13, 2)
    '406.67 f'

    >>> with_format(1.70802e-11, 2)
    '17.08 p'

    >>> with_format(7.17368e-10, 2)
    '717.37 p'

    >>> with_format(3.01295e-08, 2)
    '30.13 n'

    >>> with_format(1.26544e-06, 2)
    '1.27 µ'

    >>> with_format(5.31484e-05, 2)
    '53.15 µ'

    >>> with_format(0.00223223, 2)
    '2.23 m'

    >>> with_format(0.0937537, 2)
    '93.75 m'

    >>> with_format(3.93766, 2)
    '3.94'

    >>> with_format(165.382, 2)
    '165.38'

    >>> with_format(6946.03, 2)
    '6.95 k'

    >>> with_format(291733, 2)
    '291.73 k'

    >>> with_format(1.22528e+07, 2)
    '12.25 M'

    >>> with_format(5.14617e+08, 2)
    '514.62 M'

    >>> with_format(2.16139e+10, 2)
    '21.61 G'

    >>> with_format(9.07785e+11, 2)
    '907.79 G'

    >>> with_format(3.8127e+13, 2)
    '38.13 T'

    >>> with_format(1.60133e+15, 2)
    '1.60 P'

    >>> with_format(6.7256e+16, 2)
    '67.26 P'

    >>> with_format(2.82475e+18, 2)
    '2.82 E'

    >>> with_format(1.1864e+20, 2)
    '118.64 E'

    >>> with_format(4.98286e+21, 2)
    '4.98 Z'

    >>> with_format(2.0928e+23, 2)
    '209.28 Z'

    >>> with_format(8.78977e+24, 2)
    '8.79 Y'

    >>> with_format(3.6917e+26, 2)
    '369.17 Y'

    >>> with_format(1.55051e+28, 2)
    '15.51e+27'

    >>> with_format(6.51216e+29, 2)
    '651.22e+27'

    """
    scale_value, exp_of_10 = _split(value, precision)
    value_str = f"{scale_value:.{precision}f}"
    try:
        return format_str.format(value=value_str, prefix=_prefix(exp_of_10).strip())
    except ValueError:
        sign = ""
        if exp_of_10 == 0:
            return value_str
        if exp_of_10 > 0:
            sign = "+"
        return exp_format_str.format(
            value=value_str,
            exp_of_10="".join([sign, str(exp_of_10)]),
        )


def parse(value: str) -> float:
    """Parse a value expressed using SI prefix units to a floating point number.

    Parameters
    ----------
    value : str or unicode
        Value expressed using SI prefix units (as returned by :func:`with_format`
        function).

    Returns
    -------
    float
        `value` parse to a floating point number.

    Examples
    --------
    >>> round(parse("47.8 m"),4)
    0.0478
    >>> parse("4.78 k")
    4780.0
    >>> parse("1.0e-27")
    1e-27

    """
    # Remove any spaces in the string.
    value = value.replace(" ", "")
    # replace the SI unit with a eX where X is the exponent of 10.
    for si_prefix in SI_PREFIXES:
        value = value.replace(si_prefix.short_name, si_prefix.get_e_string())
    return float(value)
