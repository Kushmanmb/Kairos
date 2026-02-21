"""
Demo script showing Kairos security response system in action
"""

from kairos import Kairos
from cosmosSDK import Security

# Initialize Kairos
kairos = Kairos()

print("\n" + "="*60)
print("KAIROS SECURITY RESPONSE DEMO")
print("="*60 + "\n")

# Demonstrate Critical threat response
print("Scenario 1: Critical security threat detected")
print("-" * 60)
kairos.autoResponse[Security.Critical]()

print("\n" + "-" * 60)
print("\nScenario 2: High risk vulnerability detected")
print("-" * 60)
kairos.autoResponse[Security.HighRisk]()

print("\n" + "-" * 60)
print("\nScenario 3: Medium risk issue detected")
print("-" * 60)
kairos.autoResponse[Security.MediumRisk]()

print("\n" + "="*60)
print("Demo Complete - All security responses functioning correctly")
print("="*60)
