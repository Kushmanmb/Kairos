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
        self.assertEqual(self.kairos.memory, [])
    
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
        """Test lockdown method executes successfully and logs to memory"""
        result = self.kairos.lockdown()
        self.assertEqual(result, "lockdown_active")
        # Verify that lockdown logs a critical error to memory
        self.assertEqual(len(self.kairos.memory), 1)
        self.assertEqual(self.kairos.memory[0]["type"], Security.CriticalError)
    
    def test_auto_patch_method(self):
        """Test autoPatch method executes successfully"""
        result = self.kairos.autoPatch()
        self.assertEqual(result, "auto_patch_applied")
    
    def test_scheduled_patch_method(self):
        """Test scheduledPatch method executes successfully"""
        result = self.kairos.scheduledPatch()
        self.assertEqual(result, "patch_scheduled")
    
    def test_log_critical_error(self):
        """Test logging critical error to memory"""
        result = self.kairos.log_event(
            Security.CriticalError,
            "Test critical error",
            "Test details"
        )
        self.assertTrue(result)
        self.assertEqual(len(self.kairos.memory), 1)
        self.assertEqual(self.kairos.memory[0]["type"], Security.CriticalError)
        self.assertEqual(self.kairos.memory[0]["description"], "Test critical error")
        self.assertEqual(self.kairos.memory[0]["details"], "Test details")
    
    def test_log_hack(self):
        """Test logging hack/workaround to memory"""
        result = self.kairos.log_event(
            Security.Hack,
            "Test hack workaround",
            "Workaround details"
        )
        self.assertTrue(result)
        self.assertEqual(len(self.kairos.memory), 1)
        self.assertEqual(self.kairos.memory[0]["type"], Security.Hack)
        self.assertEqual(self.kairos.memory[0]["details"], "Workaround details")
    
    def test_log_regular_event_filtered(self):
        """Test that regular events are not stored in memory"""
        result = self.kairos.log_event(
            Security.RegularEvent,
            "Test regular event",
            "Should not be stored"
        )
        self.assertFalse(result)
        self.assertEqual(len(self.kairos.memory), 0)
    
    def test_get_memory_all(self):
        """Test retrieving all memory events"""
        self.kairos.log_event(Security.CriticalError, "Error 1", "Details 1")
        self.kairos.log_event(Security.Hack, "Hack 1", "Details 2")
        self.kairos.log_event(Security.RegularEvent, "Event 1", "Should not store")
        
        memory = self.kairos.get_memory()
        self.assertEqual(len(memory), 2)
    
    def test_get_memory_filtered(self):
        """Test retrieving filtered memory events by type"""
        self.kairos.log_event(Security.CriticalError, "Error 1", "Details 1")
        self.kairos.log_event(Security.Hack, "Hack 1", "Details 2")
        self.kairos.log_event(Security.CriticalError, "Error 2", "Details 3")
        
        critical_errors = self.kairos.get_memory(Security.CriticalError)
        self.assertEqual(len(critical_errors), 2)
        
        hacks = self.kairos.get_memory(Security.Hack)
        self.assertEqual(len(hacks), 1)
    
    def test_lockdown_logs_to_memory(self):
        """Test that lockdown method logs critical error to memory"""
        initial_length = len(self.kairos.memory)
        self.kairos.lockdown()
        self.assertEqual(len(self.kairos.memory), initial_length + 1)
        self.assertEqual(self.kairos.memory[-1]["type"], Security.CriticalError)
    
    def test_clear_memory(self):
        """Test clearing all memory events"""
        self.kairos.log_event(Security.CriticalError, "Error 1", "Details 1")
        self.kairos.log_event(Security.Hack, "Hack 1", "Details 2")
        self.assertEqual(len(self.kairos.memory), 2)
        
        self.kairos.clear_memory()
        self.assertEqual(len(self.kairos.memory), 0)
    
    def test_limit_memory(self):
        """Test limiting memory to maximum number of events"""
        total_events = 15
        max_events = 10
        
        # Add 15 events
        for i in range(total_events):
            self.kairos.log_event(Security.CriticalError, f"Error {i}", f"Details {i}")
        
        self.assertEqual(len(self.kairos.memory), total_events)
        
        # Limit to 10 most recent events
        self.kairos.limit_memory(max_events)
        self.assertEqual(len(self.kairos.memory), max_events)
        
        # Verify we kept the most recent ones (discarded first 5, kept 5-14)
        discarded_count = total_events - max_events
        self.assertEqual(self.kairos.memory[0]["description"], f"Error {discarded_count}")
        self.assertEqual(self.kairos.memory[-1]["description"], f"Error {total_events - 1}")
    
    def test_event_has_timestamp(self):
        """Test that logged events include timestamp"""
        self.kairos.log_event(Security.CriticalError, "Test error", "Details")
        self.assertEqual(len(self.kairos.memory), 1)
        self.assertIn("timestamp", self.kairos.memory[0])
        self.assertIsNotNone(self.kairos.memory[0]["timestamp"])


class TestCosmosSDK(unittest.TestCase):
    """Test cases for CosmosSDK modules"""
    
    def test_blockchain_constants(self):
        """Test Blockchain class constants"""
        self.assertEqual(Blockchain.All, "all_blockchains")
    
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
    
    def test_security_event_types(self):
        """Test Security event type constants"""
        self.assertEqual(Security.CriticalError, "critical_error")
        self.assertEqual(Security.Hack, "hack")
        self.assertEqual(Security.RegularEvent, "regular_event")


if __name__ == "__main__":
    unittest.main()
