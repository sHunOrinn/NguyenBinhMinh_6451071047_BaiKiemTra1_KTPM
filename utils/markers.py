import pytest

import config

requires_credentials = pytest.mark.skipif(
    not config.HAS_CREDENTIALS,
    reason="Chua dat UTC_USER / UTC_PASS trong file .env",
)
