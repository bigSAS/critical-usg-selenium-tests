import pytest

'''
HOW to docstring pod raport HTML :)

def test_unit_test():
    """ <- zawsze docstring w portojnych quoteach
    First unit test :) <- tytul testu zawsze pierwsza linika 
                       <- zawsze empty line po tytule testu
    Some cool test description :)  <- description 
    foobar <- zwykly tekst wrapowany jest w paragraf <p>foobar</p>
            <- pusta linia traktowana jest jako <br> w html
    new new line ;)
    STEPS:
    1. foo
    2. bar
    3. baz
    """
    pass
'''

@pytest.mark.unit
def test_unit_test():
    """
    First unit test :)

    Some cool test description :)
    new line

    new new line ;)
    STEPS:
    1. foo
    2. bar
    3. baz
    """
    pass


@pytest.mark.unit
def test_unit_test_s(actions):
    """
    Second unit test :)

    heloo :)
    """
    actions.element_provider.driver.get('https://google.pl')
    assert False


@pytest.mark.unit
def test_unit_test_3():
    pass