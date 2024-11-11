"""Library for formatting numbers using SI prefixes."""

from __future__ import annotations

import math
import re

SI_PREFIX_UNITS = "yzafpnµm kMGTPEZY"
CRE_SI_NUMBER = re.compile(
    r"\s*(?P<sign>[\+\-])?"
    r"(?P<integer>\d+)"
    r"(?P<fraction>.\d+)?\s*"
    rf"(?P<si_unit>[{SI_PREFIX_UNITS}])?\s*",
)


def split(value: float, precision: int = 1) -> tuple[float, int]:
    """Split a SI-Prefixed value into a value and an exponent of 10.

    Split `value` into value and "exponent-of-10", where "exponent-of-10" is a
    multiple of 3.  This corresponds to SI prefixes.
    Returns tuple, where the second value is the "exponent-of-10" and the first
    value is `value` divided by the "exponent-of-10".

    Args:
    ----
    value : int, float
        Input value.
    precision : int
        Number of digits after decimal place to include.

    Returns:
    -------
    tuple
        The second value is the "exponent-of-10" and the first value is `value`
        divided by the "exponent-of-10".

    Examples:
    --------
    >>> si_prefix.split(0.04781)
    (47.8, -3)

    >>> si_prefix.split(4781.123)
    (4.8, 3)
    See :func:`si_format` for more examples.

    """
    negative = False
    digits = precision + 1

    if value < 0.0:
        value = -value
        negative = True
    elif value == 0.0:
        return 0.0, 0

    expof10 = int(math.log10(value))
    expof10 = expof10 // 3 * 3 if expof10 > 0 else (-expof10 + 3) // 3 * -3

    value *= 10 ** (-expof10)

    thousand = 1e3
    hundred = 100.0
    ten = 10

    if value >= thousand:
        value /= 1000.0
        expof10 += 3
    elif value >= hundred:
        digits -= 2
    elif value >= ten:
        digits -= 1

    if negative:
        value *= -1

    return value, int(expof10)


def prefix(expof10: int) -> str:
    """Return the SI prefix character associated with an exponent of 10.

    Args:
        expof10 (int): Exponent of a power of 10 associated with a SI unit
            character.

    Returns:
        str : One of the characters in "yzafpnµm kMGTPEZY".

    """
    prefix_levels = (len(SI_PREFIX_UNITS) - 1) // 2
    si_level = expof10 // 3

    if abs(si_level) > prefix_levels:
        msg = "Exponent out range of available prefixes."
        raise ValueError(msg)
    return SI_PREFIX_UNITS[si_level + prefix_levels]


def si_format(
    value: float,
    precision: int = 1,
    format_str: str = "{value} {prefix}",
    exp_format_str: str = "{value}e{expof10}",
) -> str:
    """Return SI Formatted number string.

    Format `value` to a string with SI prefix, using the specified precision.

    Args:
        value (float): Input value.
        precision (int): Number of digits after decimal place to include.
        format_str (str or unicode):
            Format string where ``{prefix}`` and ``{value}`` represent the SI
            prefix and the value (scaled according to the prefix), respectively.
            The default format matches the `SI prefix style` format.
        exp_format_str (str or unicode):
            Format string where ``{expof10}`` and ``{value}`` represent the
            exponent of 10 and the value (scaled according to the exponent of 10),
            respectively.  This format is used if the absolute exponent of 10 value
            is greater than 24.

    Returns:
        str: `value` formatted according to the `SI prefix style`.

    Examples:
    For example, with `precision=2`:

    >>> si_format(0.04781, 2)
    '47.81 m'

    >>> si_format(4781.123, 2)
    '4.78 k'

    >>> si_format(0.04781, 3)
    '47.810 m'

    >>> si_format(4781.123, 3)
    '4.781 k'

    >>> si_format(1e-27)
    '1.0e-27'

    >>> si_format(1.764e-24)
    '1.8 y'

    >>> si_format(7.4088e-23, 2)
    '74.09 y'

    >>> si_format(3.1117e-21, 2)
    '3.11 z'

    >>> si_format(1.30691e-19, 2)
    '130.69 z'

    >>> si_format(5.48903e-18, 2)
    '5.49 a'

    >>> si_format(2.30539e-16, 2)
    '230.54 a'

    >>> si_format(9.68265e-15, 2)
    '9.68 f'

    >>> si_format(4.06671e-13, 2)
    '406.67 f'

    >>> si_format(1.70802e-11, 2)
    '17.08 p'

    >>> si_format(7.17368e-10, 2)
    '717.37 p'

    >>> si_format(3.01295e-08, 2)
    '30.13 n'

    >>> si_format(1.26544e-06, 2)
    '1.27 u'

    >>> si_format(5.31484e-05, 2)
    '53.15 u'

    >>> si_format(0.00223223, 2)
    '2.23 m'

    >>> si_format(0.0937537, 2)
    '93.75 m'

    >>> si_format(3.93766, 2)
    '3.94'

    >>> si_format(165.382, 2)
    '165.38'

    >>> si_format(6946.03, 2)
    '6.95 k'

    >>> si_format(291733, 2)
    '291.73 k'

    >>> si_format(1.22528e+07, 2)
    '12.25 M'

    >>> si_format(5.14617e+08, 2)
    '514.62 M'

    >>> si_format(2.16139e+10, 2)
    '21.61 G'

    >>> si_format(9.07785e+11, 2)
    '907.78 G'

    >>> si_format(3.8127e+13, 2)
    '38.13 T'

    >>> si_format(1.60133e+15, 2)
    '1.60 P'

    >>> si_format(6.7256e+16, 2)
    '67.26 P'

    >>> si_format(2.82475e+18, 2)
    '2.82 E'

    >>> si_format(1.1864e+20, 2)
    '118.64 E'

    >>> si_format(4.98286e+21, 2)
    '4.98 Z'

    >>> si_format(2.0928e+23, 2)
    '209.28 Z'

    >>> si_format(8.78977e+24, 2)
    '8.79 Y'

    >>> si_format(3.6917e+26, 2)
    '369.17 Y'

    >>> si_format(1.55051e+28, 2)
    '15.51e+27'

    >>> si_format(6.51216e+29, 2)
    '651.22e+27'

    """
    svalue, expof10 = split(value, precision)
    value_format = "%%.%df" % precision
    value_str = value_format % svalue
    try:
        return format_str.format(value=value_str, prefix=prefix(expof10).strip())
    except ValueError:
        sign = ""
        if expof10 > 0:
            sign = "+"
        return exp_format_str.format(
            value=value_str,
            expof10="".join([sign, str(expof10)]),
        )


def si_parse(value: str) -> float:
    """Parse a value expressed using SI prefix units to a floating point number.

    Parameters
    ----------
    value : str or unicode
        Value expressed using SI prefix units (as returned by :func:`si_format`
        function).

    """
    cre_10e_number = re.compile(
        r"^\s*(?P<integer>[\+\-]?\d+)?"
        r"(?P<fraction>.\d+)?\s*([eE]\s*"
        r"(?P<expof10>[\+\-]?\d+))?$",
    )
    match = cre_10e_number.match(value)
    if match:
        # Can be parsed using `float`.
        if match.group("integer") is None and match.group("fraction") is None:
            msg = "No number found."
            raise ValueError(msg)
        return float(value)
    match = CRE_SI_NUMBER.match(value)
    if match is None:
        msg = f"Invalid number: {value}"
        raise ValueError(msg)
    if match.group("integer") is None and match.group("fraction") is None:
        msg = "No number found."
        raise ValueError(msg)
    d = match.groupdict()
    si_unit = d["si_unit"] if d["si_unit"] else " "
    prefix_levels = (len(SI_PREFIX_UNITS) - 1) // 2
    scale = 10 ** (3 * (SI_PREFIX_UNITS.index(si_unit) - prefix_levels))
    ret_val = float(d["number"]) * scale
    if not isinstance(ret_val, float):
        msg = "Invalid number."
        raise TypeError(msg)
    return ret_val


def si_prefix_scale(si_unit: str) -> int:
    """Return the multiple associated with an SI unit character.

    Args:
    si_unit : str
        SI unit character, i.e., one of "yzafpnµm kMGTPEZY".

    Returns:
    int
        Multiple associated with `si_unit`, e.g., 1000 for `si_unit=K`.

    """
    ret_val = 10 ** si_prefix_expof10(si_unit)
    if not isinstance(ret_val, int):
        msg = "Invalid number."
        raise TypeError(msg)
    return ret_val


def si_prefix_expof10(si_unit: str) -> int:
    """Return the exponent of the power of ten associated with an SI unit character.

    Args:
        si_unit (str):
            SI unit character, i.e., one of "yzafpnµm kMGTPEZY".

    Returns:
        int:
        Exponent of the power of ten associated with `si_unit`, e.g., 3 for
        `si_unit=K` and -6 for `si_unit=µ`.

    """
    prefix_levels = (len(SI_PREFIX_UNITS) - 1) // 2
    return 3 * (SI_PREFIX_UNITS.index(si_unit) - prefix_levels)
