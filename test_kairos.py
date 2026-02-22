"""
Tests for Kairos Blockchain Audit Bot
"""

import unittest
from unittest.mock import patch, MagicMock
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
    
    def test_contract_verifier_initialization(self):
        """Test that contract verifier is initialized"""
        self.assertIsNotNone(self.kairos.contract_verifier)
    
    @patch('contract_verifier.ContractVerifier.fetch_and_verify')
    def test_audit_smart_contract_success(self, mock_fetch_verify):
        """Test successful smart contract audit"""
        mock_fetch_verify.return_value = {
            'success': True,
            'verification': {
                'verified': True,
                'has_source_code': True,
                'has_abi': True,
                'security_issues': [],
                'warnings': [],
                'contract_name': 'TestContract',
                'compiler_version': 'v0.8.0'
            }
        }
        
        result = self.kairos.audit_smart_contract('0x123456789')
        
        self.assertEqual(result['audit_status'], 'complete')
        self.assertEqual(result['contract_address'], '0x123456789')
        self.assertIsNone(result['threat_level'])
    
    @patch('contract_verifier.ContractVerifier.fetch_and_verify')
    def test_audit_smart_contract_with_issues(self, mock_fetch_verify):
        """Test smart contract audit with security issues"""
        mock_fetch_verify.return_value = {
            'success': True,
            'verification': {
                'verified': False,
                'has_source_code': True,
                'has_abi': True,
                'security_issues': ['Uses tx.origin'],
                'warnings': [],
                'contract_name': 'RiskyContract',
                'compiler_version': 'v0.8.0'
            }
        }
        
        result = self.kairos.audit_smart_contract('0x123456789')
        
        self.assertEqual(result['audit_status'], 'complete')
        self.assertEqual(result['threat_level'], Security.HighRisk)
    
    @patch('contract_verifier.ContractVerifier.fetch_and_verify')
    def test_audit_smart_contract_unverified(self, mock_fetch_verify):
        """Test smart contract audit for unverified contract"""
        mock_fetch_verify.return_value = {
            'success': True,
            'verification': {
                'verified': False,
                'has_source_code': False,
                'has_abi': False,
                'security_issues': ['Contract source code not verified'],
                'warnings': [],
                'contract_name': 'Unknown',
                'compiler_version': 'Unknown'
            }
        }
        
        result = self.kairos.audit_smart_contract('0x123456789')
        
        self.assertEqual(result['audit_status'], 'complete')
        self.assertEqual(result['threat_level'], Security.HighRisk)
    
    @patch('contract_verifier.ContractVerifier.fetch_and_verify')
    def test_audit_smart_contract_critical_issues(self, mock_fetch_verify):
        """Test smart contract audit with critical issues"""
        mock_fetch_verify.return_value = {
            'success': True,
            'verification': {
                'verified': False,
                'has_source_code': True,
                'has_abi': True,
                'security_issues': ['Issue 1', 'Issue 2', 'Issue 3'],
                'warnings': [],
                'contract_name': 'DangerousContract',
                'compiler_version': 'v0.8.0'
            }
        }
        
        result = self.kairos.audit_smart_contract('0x123456789')
        
        self.assertEqual(result['audit_status'], 'complete')
        self.assertEqual(result['threat_level'], Security.Critical)
    
    @patch('contract_verifier.ContractVerifier.fetch_and_verify')
    def test_audit_smart_contract_failure(self, mock_fetch_verify):
        """Test smart contract audit failure"""
        mock_fetch_verify.return_value = {
            'success': False,
            'error': 'Connection failed'
        }
        
        result = self.kairos.audit_smart_contract('0x123456789')
        
        self.assertEqual(result['audit_status'], 'failed')
        self.assertIn('error', result)


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


if __name__ == "__main__":
    unittest.main()
