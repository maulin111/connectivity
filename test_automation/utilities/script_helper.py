import pytest
from .LoggingFormatter import logger

@pytest.mark.skip(reason="Not a test.")
def test_step(index, description):
    logger.info_step(index, description)
