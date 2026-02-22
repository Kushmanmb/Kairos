"""
Demo script for Etherscan contract fetch and verify functionality
Shows how to use Kairos to audit smart contracts
"""

from kairos import Kairos
from contract_verifier import ContractVerifier

print("\n" + "="*70)
print("KAIROS - ETHERSCAN CONTRACT FETCH AND VERIFY DEMO")
print("="*70 + "\n")

# Initialize Kairos without API key (can also provide one for higher rate limits)
kairos = Kairos()

print("Scenario 1: Direct Contract Verification")
print("-" * 70)

# Create a standalone contract verifier
verifier = ContractVerifier()

# Example: USDT contract on Ethereum (verified contract)
usdt_address = "0xdac17f958d2ee523a2206206994597c13d831ec7"

print(f"\nFetching contract: {usdt_address}")
print("Using Etherscan API v2...\n")

# Demonstrate the fetch operation
try:
    # This shows the basic fetch operation from the problem statement
    print("Executing: fetch('https://api.etherscan.io/v2/api', options)")
    result = verifier.fetch_and_verify(usdt_address, chain="eth")
    
    if result['success']:
        verification = result['verification']
        print(f"\n✅ Contract fetched and verified successfully!")
        print(f"   Contract Name: {verification['contract_name']}")
        print(f"   Compiler: {verification['compiler_version']}")
        print(f"   Source Code Available: {verification['has_source_code']}")
        print(f"   ABI Available: {verification['has_abi']}")
        
        if verification['security_issues']:
            print(f"\n⚠️  Security Issues Detected:")
            for issue in verification['security_issues']:
                print(f"      - {issue}")
        else:
            print(f"\n✓ No security issues detected")
    else:
        print(f"\n❌ Error: {result['error']}")
        print("   (This is expected in demo mode without network access)")
        
except Exception as e:
    print(f"❌ Demo mode: {str(e)}")
    print("   In production, this would fetch real contract data from Etherscan")

print("\n" + "-" * 70)
print("\nScenario 2: Integrated Smart Contract Audit via Kairos")
print("-" * 70)

# Example contract address for audit
example_contract = "0x1234567890123456789012345678901234567890"

print(f"\nAuditing contract through Kairos: {example_contract}")
print("This demonstrates the full integration...\n")

try:
    audit_result = kairos.audit_smart_contract(example_contract)
    
    if audit_result['audit_status'] == 'complete':
        print(f"\n✅ Audit Complete")
        print(f"   Address: {audit_result['contract_address']}")
        if audit_result['threat_level']:
            print(f"   Threat Level: {audit_result['threat_level']}")
            print(f"   Auto-response triggered!")
        else:
            print(f"   Threat Level: None - Contract appears safe")
    else:
        print(f"\n⚠️  Audit Status: {audit_result['audit_status']}")
        if 'error' in audit_result:
            print(f"   Error: {audit_result['error']}")
            print("   (This is expected in demo mode without network access)")
            
except Exception as e:
    print(f"Demo mode: {str(e)}")
    print("In production, this would perform full contract audit")

print("\n" + "-" * 70)
print("\nScenario 3: Security Pattern Detection")
print("-" * 70)

# Show security pattern checking on sample code
print("\nDemonstrating security pattern detection...\n")

dangerous_code_samples = [
    ("selfdestruct", "contract Killable { function kill() { selfdestruct(owner); } }"),
    ("delegatecall", "contract Proxy { function execute() { target.delegatecall(data); } }"),
    ("tx.origin", "contract Auth { require(tx.origin == owner); }")
]

for pattern, code in dangerous_code_samples:
    issues = verifier._check_security_patterns(code)
    print(f"Code with '{pattern}':")
    print(f"  {code[:60]}...")
    if issues:
        print(f"  ⚠️  Issue detected: {issues[0]}")
    print()

print("-" * 70)
print("\n" + "="*70)
print("DEMO COMPLETE")
print("="*70)
print("\nKey Features Demonstrated:")
print("  ✓ Fetch contract data from Etherscan API v2")
print("  ✓ Verify contract source code and ABI")
print("  ✓ Detect security vulnerabilities")
print("  ✓ Automated threat response integration")
print("  ✓ Pattern-based security scanning")
print("\nFor production use:")
print("  - Provide Etherscan API key for higher rate limits")
print("  - Network access required for actual contract fetching")
print("  - Auto-response system triggers based on threat levels")
print("="*70 + "\n")
