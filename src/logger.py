"""
Configure a basic application-wide logger.

Modules import `logger` from here to produce structured logs.
Adjust logging behavior centrally if needed.
"""

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
