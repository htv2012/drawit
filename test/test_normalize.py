import pytest

from drawit.draw_tree_networkx import normalize_sequence


@pytest.mark.parametrize(
    "seq, expected",
    [
        pytest.param(["n", "N", "None", "null"], [None, None, None, None], id="null"),
        pytest.param(list("0123456789"), list(range(10)), id="digits"),
        pytest.param(["a", "b"], ["a", "b"], id="non digits"),
    ],
)
def test_normalize(seq, expected):
    assert normalize_sequence(seq) == expected
