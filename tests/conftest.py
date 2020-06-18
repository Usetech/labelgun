import pytest
import structlog


@pytest.fixture(autouse=True)
def setup():
    structlog.configure(
        processors=[
            structlog.processors.JSONRenderer(ensure_ascii=False),
        ],
        context_class=structlog.threadlocal.wrap_dict(dict),
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
