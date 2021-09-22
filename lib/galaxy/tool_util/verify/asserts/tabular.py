import re


def get_first_line(output):
    """
    get the first non-comment and non-empty line
    """
    match = re.search("^([^#\n].*)$", output, flags=re.MULTILINE)
    if match is None:
        return None
    else:
        return match.group(1)


def assert_has_n_columns(output, n, sep='\t'):
    """ Asserts the tabular output contains n columns. The optional
    sep argument specifies the column seperator used to determine the
    number of columns."""
    n = int(n)
    first_line = get_first_line(output)
    assert first_line is not None, "Was expecting output with %d columns, but output was empty." % n
    assert len(first_line.split(sep)) == n, f"Expected {n} columns in output, found {first_line.split(sep)} lines"