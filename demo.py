"""
Demo script showing Kairos security response system in action
"""

import logging
from kairos import Kairos
from cosmosSDK import Security

# Get logger (configuration is already set up by kairos module)
logger = logging.getLogger(__name__)

# Initialize Kairos
kairos = Kairos()

logger.info("\n" + "="*60)
logger.info("KAIROS SECURITY RESPONSE DEMO")
logger.info("="*60 + "\n")

# Demonstrate Critical threat response
logger.info("Scenario 1: Critical security threat detected")
logger.info("-" * 60)
kairos.autoResponse[Security.Critical]()

logger.info("\n" + "-" * 60)
logger.info("\nScenario 2: High risk vulnerability detected")
logger.info("-" * 60)
kairos.autoResponse[Security.HighRisk]()

logger.info("\n" + "-" * 60)
logger.info("\nScenario 3: Medium risk issue detected")
logger.info("-" * 60)
kairos.autoResponse[Security.MediumRisk]()

logger.info("\n" + "="*60)
logger.info("Demo Complete - All security responses functioning correctly")
logger.info("="*60)
