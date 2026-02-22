# GitHub Copilot Instructions for Kairos

## Project Overview

Kairos is a blockchain security and audit system built with the CosmosSDK framework. It provides automated threat detection, vulnerability patching, and comprehensive monitoring across multiple blockchain platforms.

### Core Purpose
- Monitor all blockchain networks simultaneously
- Perform comprehensive audits on smart contracts, wallets, exchanges, and transactions
- Provide automated security responses to threats at different severity levels
- Maintain granular access control with a three-tier permission system

## Architecture

### Project Structure
```
Kairos/
├── cosmosSDK/           # Core SDK framework
│   ├── __init__.py      # Module initialization
│   ├── blockchain.py    # Blockchain configurations
│   ├── audit.py         # Audit type definitions
│   ├── alerts.py        # Alert system
│   └── security.py      # Security protocols
├── kairos.py            # Main Kairos bot implementation
├── test_kairos.py       # Test suite
└── README.md            # Documentation
```

### Key Components

#### CosmosSDK Module
- **Blockchain**: Defines blockchain network configurations
- **Audit**: Specifies audit types (SmartContracts, Wallets, Exchanges, Transactions)
- **Alerts**: Boolean alert configuration (Yes/No)
- **Security**: Access permissions, security features, and threat levels

#### Kairos Class
Main class that orchestrates the security and audit system with:
- Blockchain monitoring configuration
- Audit type selection
- Alert system
- Access level management (ReadOnly, Edit, Delete)
- Auto-response mapping for different threat levels

## Coding Standards

### Python Style Guide
- Follow PEP 8 style guidelines
- Use descriptive variable and method names
- Include docstrings for all classes and methods
- Use type hints where appropriate
- Keep methods focused and single-purpose

### Code Organization
- Maintain the modular structure with cosmosSDK as a separate package
- Each module in cosmosSDK should handle a specific domain
- Keep constants as class attributes for easy access
- Use tuples for immutable collections of audit types and security features

### Naming Conventions
- Class names: PascalCase (e.g., `Kairos`, `Blockchain`)
- Method names: snake_case (e.g., `lockdown`, `auto_patch`)
- Constants: PascalCase as class attributes (e.g., `Security.Critical`)
- Private methods: prefix with underscore (e.g., `_internal_method`)

## Security Guidelines

### Critical Security Considerations
1. **Never expose sensitive blockchain credentials** in code or logs
2. **Validate all inputs** before processing blockchain transactions
3. **Implement proper error handling** to prevent information disclosure
4. **Follow principle of least privilege** for access control
5. **Log security events** without exposing sensitive data

### Threat Response Levels
- **Critical**: Immediate lockdown - suspend all transactions, restrict access
- **High Risk**: Automatic patching - apply fixes immediately
- **Medium Risk**: Scheduled patching - queue for maintenance window

### Security Features
- **AntiTamper**: Protection against unauthorized modifications
- **CopyProtection**: Prevention of unauthorized duplication

## Testing Standards

### Test Requirements
- All new features must have corresponding unit tests
- Tests should use the `unittest` framework
- Maintain test coverage for both Kairos class and CosmosSDK modules
- Test files should be named `test_*.py`

### Running Tests
```bash
python -m unittest test_kairos.py -v
```

### Test Organization
- Use descriptive test method names starting with `test_`
- Group related tests in test classes
- Use `setUp()` for test initialization
- Assert expected behavior, not implementation details

### Current Test Coverage
- Kairos initialization and configuration
- Security response methods (lockdown, autoPatch, scheduledPatch)
- Access level configuration
- Auto-response mapping
- CosmosSDK module constants

## Development Workflow

### Adding New Features
1. **Plan**: Understand the security implications
2. **Implement**: Follow the modular architecture
3. **Test**: Write comprehensive unit tests
4. **Document**: Update README and docstrings
5. **Review**: Ensure security best practices are followed

### Modifying CosmosSDK
When adding new capabilities to CosmosSDK:
1. Create or modify the appropriate module (blockchain.py, audit.py, etc.)
2. Update `__init__.py` to export new classes/constants
3. Add corresponding tests in `test_kairos.py`
4. Update documentation

### Response Method Pattern
Security response methods should:
- Print clear, informative messages with emojis for visibility
- Return a status string indicating action taken
- Be mapped in `autoResponse` dictionary
- Have corresponding tests

Example:
```python
def new_response(self):
    """Description of the response action"""
    print("🚨 ACTION: Description")
    print("   - Step 1")
    print("   - Step 2")
    return "status_string"
```

## Common Patterns

### Adding New Audit Type
```python
# In cosmosSDK/audit.py
class Audit:
    NewAuditType = "new_audit_type"

# In kairos.py
self.audit = (
    Audit.SmartContracts,
    Audit.Wallets,
    Audit.Exchanges,
    Audit.Transactions,
    Audit.NewAuditType  # Add here
)
```

### Adding New Security Level
```python
# In cosmosSDK/security.py
class Security:
    NewThreatLevel = "new_threat_level"

# In kairos.py
self.autoResponse = {
    Security.Critical: self.lockdown,
    Security.HighRisk: self.autoPatch,
    Security.MediumRisk: self.scheduledPatch,
    Security.NewThreatLevel: self.new_response  # Add here
}
```

## Dependencies

### Current Dependencies
- Python 3.x (no external dependencies currently)
- Standard library only (`unittest` for testing)

### Adding Dependencies
When adding new dependencies:
1. Ensure they are security-vetted
2. Pin specific versions for reproducibility
3. Document in README.md
4. Update requirements.txt if created

## Documentation Standards

### README Updates
Keep README.md synchronized with code changes:
- Update feature list for new capabilities
- Maintain architecture diagram accuracy
- Include usage examples
- Document security response levels

### Code Comments
- Use docstrings for public APIs
- Add inline comments for complex logic only
- Explain "why" not "what" in comments
- Keep comments up-to-date with code changes

## Repository Conventions

### Branch Protection
- `.github/workflows/` is protected and requires @Kushmanmb approval
- All changes must go through pull requests
- Code owner reviews are required for protected paths

### Commit Messages
- Use descriptive commit messages
- Start with a verb (Add, Update, Fix, Remove)
- Reference issue numbers when applicable
- Keep subject line under 72 characters

## Best Practices

### Performance
- Keep monitoring operations efficient
- Avoid unnecessary blockchain queries
- Use appropriate data structures (tuples for immutable data)
- Cache results when appropriate

### Maintainability
- Keep classes and methods small and focused
- Avoid deep nesting
- Use meaningful variable names
- Refactor duplicate code

### Error Handling
- Handle exceptions gracefully
- Provide informative error messages
- Log errors for debugging
- Never expose stack traces to end users

## Questions and Clarifications

When in doubt:
1. Consult the README.md for project goals
2. Review existing code patterns
3. Ensure changes align with security-first philosophy
4. Maintain the modular architecture
5. Write comprehensive tests

## Contact

For questions or clarifications about the codebase, refer to:
- Repository owner: @Kushmanmb
- Documentation: README.md and inline docstrings
- Issue tracker: GitHub Issues
