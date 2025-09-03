"""Implementation of a matplotlib FuncFormatter for SI prefixes."""

from matplotlib.ticker import FuncFormatter

from . import with_format


def matplotlib_tick_formatter(
    precision: int = 0,
    format_str: str = "{value} {prefix}",
    exp_format_str: str = "{value}e{exp_of_10}",
) -> FuncFormatter:
    """Return a Matplotlib tick formatter function.

    Parameters
    ----------
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
    function
        A Matplotlib tick formatter function.

    Examples
    --------
    >>> from matplotlib.ticker import FuncFormatter
    >>> import matplotlib.pyplot as plt
    >>> fig = plt.figure()
    >>> ax = fig.add_subplot(1, 1, 1)
    >>> ax.set_yscale("log")
    >>> ax.yaxis.set_major_formatter(matplotlib_tick_formatter())
    >>> ax.plot([
    ...     1e-21, 1e-18, 1e-15, 1e-12, 1e-9, 1e-6, 1e-3,
    ...     1, 1e3, 1e6, 1e9, 1e12, 1e15, 1e18, 1e21,
    ... ])
    [<matplotlib.lines.Line2D object at ...>]
    >>> fig.savefig("test_results/test.png")

    """

    def _format_func(value: float, _: float) -> str:
        return with_format(
            value,
            precision=precision,
            format_str=format_str,
            exp_format_str=exp_format_str,
        )

    return FuncFormatter(_format_func)
