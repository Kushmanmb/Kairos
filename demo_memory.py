"""
Demo script showing Kairos memory system filtering critical errors and hacks
"""

from kairos import Kairos
from cosmosSDK import Security

# Initialize Kairos
kairos = Kairos()

print("\n" + "="*60)
print("KAIROS MEMORY SYSTEM DEMO")
print("="*60 + "\n")

# Demonstrate that only critical errors and hacks are stored
print("Testing memory filtering...")
print("-" * 60)

# Try logging different event types
print("\n1. Logging a CRITICAL ERROR (should be stored):")
stored = kairos.log_event(
    Security.CriticalError,
    "Database connection lost during transaction processing",
    "Connection timeout after 30 seconds"
)
print(f"   Stored in memory: {stored}")

print("\n2. Logging a HACK/WORKAROUND (should be stored):")
stored = kairos.log_event(
    Security.Hack,
    "Temporary workaround: Using backup API endpoint",
    "Primary endpoint down, switched to backup - needs permanent fix"
)
print(f"   Stored in memory: {stored}")

print("\n3. Logging a REGULAR EVENT (should NOT be stored):")
stored = kairos.log_event(
    Security.RegularEvent,
    "Routine system health check completed",
    "All systems operational"
)
print(f"   Stored in memory: {stored}")

print("\n4. Logging another REGULAR EVENT (should NOT be stored):")
stored = kairos.log_event(
    Security.RegularEvent,
    "User logged in successfully",
    "User ID: 12345"
)
print(f"   Stored in memory: {stored}")

# Trigger a lockdown which automatically logs a critical error
print("\n5. Triggering system lockdown (auto-logs critical error):")
print("-" * 60)
kairos.autoResponse[Security.Critical]()

# Show memory contents
print("\n" + "="*60)
print("MEMORY CONTENTS (Critical Errors and Hacks Only)")
print("="*60)
memory = kairos.get_memory()
print(f"\nTotal events stored: {len(memory)}")
print(f"Expected: 3 (2 manual + 1 from lockdown)")

print("\n" + "-" * 60)
for i, event in enumerate(memory, 1):
    print(f"\nEvent {i}:")
    print(f"  Type: {event['type']}")
    print(f"  Description: {event['description']}")
    print(f"  Details: {event['details']}")

# Filter by type
print("\n" + "="*60)
print("FILTERED MEMORY - Critical Errors Only")
print("="*60)
critical_errors = kairos.get_memory(Security.CriticalError)
print(f"\nCritical errors found: {len(critical_errors)}")
for i, event in enumerate(critical_errors, 1):
    print(f"\n{i}. {event['description']}")

print("\n" + "="*60)
print("FILTERED MEMORY - Hacks/Workarounds Only")
print("="*60)
hacks = kairos.get_memory(Security.Hack)
print(f"\nHacks/workarounds found: {len(hacks)}")
for i, event in enumerate(hacks, 1):
    print(f"\n{i}. {event['description']}")

print("\n" + "="*60)
print("Demo Complete - Memory system functioning correctly")
print("Only critical errors and hacks are stored for future reference")
print("="*60)
