"""
Tests for Kairos Blockchain Audit Bot
"""

import unittest
from kairos import Kairos
from cosmosSDK import Blockchain, Audit, Alerts, Security


class TestKairos(unittest.TestCase):
    """Test cases for Kairos class"""
    
    def setUp(self):
        """Initialize Kairos instance for testing"""
        self.kairos = Kairos()
    
    def test_initialization(self):
        """Test that Kairos initializes with correct settings"""
        self.assertEqual(self.kairos.blockchain, Blockchain.All)
        self.assertEqual(self.kairos.alerts, Alerts.Yes)
        self.assertEqual(self.kairos.permissions, Security.FullAccess)
        self.assertEqual(self.kairos.memory, "512GB")
    
    def test_audit_configuration(self):
        """Test audit types are properly configured"""
        expected_audits = (
            Audit.SmartContracts,
            Audit.Wallets,
            Audit.Exchanges,
            Audit.Transactions
        )
        self.assertEqual(self.kairos.audit, expected_audits)
    
    def test_security_features(self):
        """Test security features are enabled"""
        expected_security_features = (Security.AntiTamper, Security.CopyProtection)
        self.assertEqual(self.kairos.security, expected_security_features)
    
    def test_access_levels(self):
        """Test access level configuration"""
        self.assertEqual(self.kairos.accessLevels[1], Security.ReadOnly)
        self.assertEqual(self.kairos.accessLevels[2], Security.Edit)
        self.assertEqual(self.kairos.accessLevels[3], Security.Delete)
    
    def test_auto_response_mapping(self):
        """Test auto-response methods are properly mapped"""
        self.assertEqual(
            self.kairos.autoResponse[Security.Critical],
            self.kairos.lockdown
        )
        self.assertEqual(
            self.kairos.autoResponse[Security.HighRisk],
            self.kairos.autoPatch
        )
        self.assertEqual(
            self.kairos.autoResponse[Security.MediumRisk],
            self.kairos.scheduledPatch
        )
    
    def test_lockdown_method(self):
        """Test lockdown method executes successfully"""
        result = self.kairos.lockdown()
        self.assertEqual(result, "lockdown_active")
    
    def test_auto_patch_method(self):
        """Test autoPatch method executes successfully"""
        result = self.kairos.autoPatch()
        self.assertEqual(result, "auto_patch_applied")
    
    def test_scheduled_patch_method(self):
        """Test scheduledPatch method executes successfully"""
        result = self.kairos.scheduledPatch()
        self.assertEqual(result, "patch_scheduled")


class TestCosmosSDK(unittest.TestCase):
    """Test cases for CosmosSDK modules"""
    
    def test_blockchain_constants(self):
        """Test Blockchain class constants"""
        self.assertEqual(Blockchain.All, "all_blockchains")
        self.assertEqual(Blockchain.Cosmos, "cosmos")
        self.assertEqual(Blockchain.Ethereum, "ethereum")
        self.assertEqual(Blockchain.Foundry, "foundry")
    
    def test_audit_constants(self):
        """Test Audit class constants"""
        self.assertEqual(Audit.SmartContracts, "smart_contracts")
        self.assertEqual(Audit.Wallets, "wallets")
        self.assertEqual(Audit.Exchanges, "exchanges")
        self.assertEqual(Audit.Transactions, "transactions")
    
    def test_alerts_constants(self):
        """Test Alerts class constants"""
        self.assertEqual(Alerts.Yes, True)
        self.assertEqual(Alerts.No, False)
    
    def test_security_permissions(self):
        """Test Security permission constants"""
        self.assertEqual(Security.FullAccess, "full_access")
        self.assertEqual(Security.ReadOnly, "read_only")
        self.assertEqual(Security.Edit, "edit")
        self.assertEqual(Security.Delete, "delete")
    
    def test_security_features(self):
        """Test Security feature constants"""
        self.assertEqual(Security.AntiTamper, "anti_tamper")
        self.assertEqual(Security.CopyProtection, "copy_protection")
    
    def test_security_threat_levels(self):
        """Test Security threat level constants"""
        self.assertEqual(Security.Critical, "critical")
        self.assertEqual(Security.HighRisk, "high_risk")
        self.assertEqual(Security.MediumRisk, "medium_risk")


if __name__ == "__main__":
    unittest.main()
