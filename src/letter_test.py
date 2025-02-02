import pytest


from src.letter import Letter, get_html


@pytest.fixture
def letter() -> Letter:
    return Letter(to="Katie", from_="John", text="I love you sweetheart")


@pytest.fixture
def id() -> str:
    return "0"


@pytest.fixture
def correct_html_str() -> str:
    return """<div class="letter" id="0">
<p><span class="to">To Katie, </span> <span class="from">from John</span></p>
<p>I love you sweetheart</p>
</div>"""


def test_get_html(letter: Letter, id: str, correct_html_str: str):
    html = get_html(letter, id)
    assert html == correct_html_str
