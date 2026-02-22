# Copilot Instructions for Kairos Repository

## Project Overview

Kairos is a **blockchain security and audit bot** built with Python and the CosmosSDK framework. The project provides automated threat detection, vulnerability patching, and comprehensive monitoring across multiple blockchain platforms. It's a relatively small, focused Python project with a clear architecture and comprehensive test coverage.

**Repository Stats:**
- Language: Python 3.12+
- Size: Small (~10 source files)
- Type: Security/Blockchain monitoring application
- Framework: Custom CosmosSDK wrapper

## Project Structure

```
Kairos/
├── .github/
│   ├── workflows/
│   │   └── kairos-bot.yml         # CI workflow - runs tests and security audits
│   ├── branch-protection.yml       # Branch protection config
│   ├── CODEOWNERS                 # Requires @Kushmanmb approval for workflow changes
│   └── README.md
├── cosmosSDK/                      # Core SDK framework - all blockchain abstractions
│   ├── __init__.py                # Module exports: Blockchain, Audit, Alerts, Security
│   ├── blockchain.py              # Blockchain configurations (e.g., Blockchain.All)
│   ├── audit.py                   # Audit type definitions (SmartContracts, Wallets, etc.)
│   ├── alerts.py                  # Alert system (Yes/No)
│   └── security.py                # Security protocols and threat levels
├── kairos.py                       # Main Kairos bot implementation
├── test_kairos.py                  # Comprehensive test suite (14 tests)
├── demo.py                        # Demo/example script
└── README.md                      # Main documentation
```

## Build, Test, and Run Instructions

### Prerequisites
- Python 3.12+ is required (currently using Python 3.12.3)
- No external dependencies - project uses only standard library

### Testing
**ALWAYS run tests before and after making changes:**
```bash
python -m unittest test_kairos.py -v
```
- Tests run in ~1 second
- All 14 tests must pass
- Tests cover both `Kairos` class and `cosmosSDK` constants
- Tests verify initialization, security methods (lockdown, autoPatch, scheduledPatch), and all SDK constants

### Running the Application
```bash
python kairos.py
```
- Outputs initialization status and configuration
- No additional setup required
- Should display blockchain scope, audit types, alerts status, and auto-response mappings

### CI/CD Pipeline
The GitHub Actions workflow (`.github/workflows/kairos-bot.yml`) runs:
1. Python setup (3.x)
2. Unit tests via `python -m unittest test_kairos.py -v`
3. Main application via `python kairos.py`
4. Security report generation

**Important:** Workflow file changes require approval from @Kushmanmb (see CODEOWNERS)

## Code Architecture

### Core Classes

**Kairos Class** (`kairos.py`):
- Main bot implementation with security configurations
- Initialization sets up blockchain scope, audit types, alerts, permissions, memory allocation
- Three security response methods:
  - `lockdown()`: Critical threats - returns "lockdown_active"
  - `autoPatch()`: High-risk vulnerabilities - returns "auto_patch_applied"
  - `scheduledPatch()`: Medium-risk issues - returns "patch_scheduled"
- Auto-response mapping: `{threat_level: method}` dictionary

**CosmosSDK Module** (`cosmosSDK/`):
- Provides constants and enums via four sub-modules
- All classes use simple string constants (no complex logic)
- Constants:
  - `Blockchain.All` = "all_blockchains"
  - `Audit` types: "smart_contracts", "wallets", "exchanges", "transactions"
  - `Alerts`: Yes=True, No=False
  - `Security` permissions: "full_access", "read_only", "edit", "delete"
  - `Security` features: "anti_tamper", "copy_protection"
  - `Security` threat levels: "critical", "high_risk", "medium_risk"

### Testing Structure

Two test classes in `test_kairos.py`:
1. `TestKairos`: Tests main Kairos class (8 tests)
2. `TestCosmosSDK`: Tests SDK constants (6 tests)

All tests use standard `unittest` framework with `assertEqual` assertions.

## Important Guidelines

### Making Code Changes

1. **Always run tests first** to establish baseline: `python -m unittest test_kairos.py -v`
2. Make minimal, targeted changes
3. **Run tests after changes** to verify no regressions
4. If adding new security methods or threat levels:
   - Update `Kairos` class in `kairos.py`
   - Add corresponding constant in `cosmosSDK/security.py`
   - Update auto-response mapping in `__init__`
   - Add tests in `test_kairos.py`

### Security Considerations

- This is a security-focused project - maintain security features
- Three-tier access control system must remain intact
- Anti-tamper and copy protection mechanisms are critical
- All security methods should return status strings for tracking

### Common Patterns

**Adding new audit type:**
1. Add constant to `cosmosSDK/audit.py`
2. Include in `Kairos.__init__` audit tuple
3. Add test in `TestCosmosSDK.test_audit_constants`

**Adding new threat level:**
1. Add constant to `cosmosSDK/security.py`
2. Create response method in `Kairos` class
3. Add to `autoResponse` mapping in `__init__`
4. Add tests for constant and method

### What NOT to Do

- Don't add external dependencies without careful consideration
- Don't modify test return values without understanding impact
- Don't change workflow file without understanding CODEOWNERS approval requirement
- Don't alter the SDK constants without updating all references and tests

## Quick Reference

**File to change for:**
- Bot behavior: `kairos.py`
- New blockchain types: `cosmosSDK/blockchain.py`
- New audit types: `cosmosSDK/audit.py`
- New security levels/features: `cosmosSDK/security.py`
- Alert configuration: `cosmosSDK/alerts.py`
- Tests: `test_kairos.py`
- CI/CD: `.github/workflows/kairos-bot.yml` (requires CODEOWNERS approval)

**Commands that always work:**
```bash
# Test
python -m unittest test_kairos.py -v

# Run
python kairos.py

# Check Python version
python --version
```

## Trust These Instructions

These instructions are comprehensive and validated. Only search for additional information if:
- You need to understand implementation details beyond what's documented here
- These instructions are incomplete for your specific task
- You discover information here is incorrect or outdated

For most tasks, this document contains everything needed to successfully implement, test, and validate changes.
