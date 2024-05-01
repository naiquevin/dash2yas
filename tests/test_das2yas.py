from dash2yas import placeholder_mapping, render_yasnippet, Snippet


def test_placeholder_mapping():
    body = "Hello __guest__, this is just a test"
    result = placeholder_mapping(body)
    assert len(result) == 1
    assert result["__guest__"] == "${1:guest}"

    body = "x=__a__; y=__b__, x=__a__"
    result = placeholder_mapping(body)
    assert len(result) == 2
    assert result["__a__"] == "${1:a}"
    assert result["__b__"] == "${2:b}"

    body = """This is just a __test__
    With input spread across multiple __lines__.
    But this is __just__ a __test__, really.
    """
    result = placeholder_mapping(body)
    assert len(result) == 3
    assert result["__test__"] == "${1:test}"
    assert result["__lines__"] == "${2:lines}"
    assert result["__just__"] == "${3:just}"

    body = ""
    result = placeholder_mapping(body)
    assert len(result) == 0


def test_render_yasnippet():
    snippet= Snippet(mode="my-mode", key="x/pqr", body="x=__a__; y=__b__, x=__a__")
    output = render_yasnippet(snippet)
    expected_output = "\n".join([
        "# -*- mode: snippet -*-",
        "# name: x pqr",
        "# key: x/pqr",
        "# --",
        "",
        "x=${1:a}; y=${2:b}, x=${1:a}$0"
    ])
    assert output == expected_output
