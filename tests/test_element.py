from exercise.element import Element


def test_element():
    element = Element({"aaaa": {"bbbb": [{"cccc": 1}, {"cccc": 2}]}})

    assert element.aaaa.bbbb[0] == Element({"cccc": 1})

    assert element.aaaa.bbbb[0].value == {"cccc": Element(1)}
    assert element.aaaa.bbbb[0].cccc.value == 1

    assert str(element.aaaa.bbbb[0]) == "Element(cccc=1)"


def test_env_interpolation(monkeypatch):
    monkeypatch.setenv("TEST_ENV_VAR", "my value")

    element = Element({"aaaa": "$TEST_ENV_VAR"})
    assert element.aaaa.value == "my value"
