"""
Security module for CosmosSDK
"""

class Security:
    """Security configuration and threat levels"""
    # Access Permissions
    FullAccess = "full_access"
    ReadOnly = "read_only"
    Edit = "edit"
    Delete = "delete"
    
    # Security Features
    AntiTamper = "anti_tamper"
    CopyProtection = "copy_protection"
    
    # Threat Levels
    Critical = "critical"
    HighRisk = "high_risk"
    MediumRisk = "medium_risk"
    
    # Event Types for Memory Storage
    CriticalError = "critical_error"
    Hack = "hack"
    RegularEvent = "regular_event"
