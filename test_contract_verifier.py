"""
Tests for Contract Verifier module
"""

import unittest
from unittest.mock import patch, MagicMock
from contract_verifier import ContractVerifier
import json


class TestContractVerifier(unittest.TestCase):
    """Test cases for ContractVerifier class"""
    
    def setUp(self):
        """Initialize ContractVerifier instance for testing"""
        self.verifier = ContractVerifier(api_key="test_api_key")
    
    def test_initialization(self):
        """Test that ContractVerifier initializes correctly"""
        self.assertEqual(self.verifier.base_url, "https://api.etherscan.io/v2/api")
        self.assertEqual(self.verifier.api_key, "test_api_key")
    
    def test_initialization_without_api_key(self):
        """Test initialization without API key"""
        verifier = ContractVerifier()
        self.assertIsNone(verifier.api_key)
    
    def test_fetch_contract_invalid_address(self):
        """Test fetch_contract with invalid address"""
        with self.assertRaises(ValueError):
            self.verifier.fetch_contract("")
        
        with self.assertRaises(ValueError):
            self.verifier.fetch_contract(None)
    
    @patch('urllib.request.urlopen')
    def test_fetch_contract_success(self, mock_urlopen):
        """Test successful contract fetch"""
        # Mock response
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = json.dumps({
            'status': '1',
            'message': 'OK',
            'result': [{
                'SourceCode': 'contract Test {}',
                'ABI': '[{"type":"function"}]',
                'ContractName': 'TestContract',
                'CompilerVersion': 'v0.8.0'
            }]
        }).encode('utf-8')
        mock_response.__enter__ = MagicMock(return_value=mock_response)
        mock_response.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_response
        
        result = self.verifier.fetch_contract('0x123456789')
        
        self.assertEqual(result['status'], '1')
        self.assertEqual(result['message'], 'OK')
        self.assertIn('result', result)
    
    @patch('urllib.request.urlopen')
    def test_fetch_contract_connection_error(self, mock_urlopen):
        """Test fetch_contract with connection error"""
        mock_urlopen.side_effect = Exception("Connection failed")
        
        with self.assertRaises(ConnectionError):
            self.verifier.fetch_contract('0x123456789')
    
    def test_verify_contract_invalid_data(self):
        """Test verify_contract with invalid data"""
        with self.assertRaises(ValueError):
            self.verifier.verify_contract("not a dict")
    
    def test_verify_contract_with_source_code(self):
        """Test contract verification with source code"""
        contract_data = {
            'status': '1',
            'message': 'OK',
            'result': [{
                'SourceCode': 'contract SafeContract { function test() public {} }',
                'ABI': '[{"type":"function"}]',
                'ContractName': 'SafeContract',
                'CompilerVersion': 'v0.8.0'
            }]
        }
        
        result = self.verifier.verify_contract(contract_data)
        
        self.assertTrue(result['has_source_code'])
        self.assertTrue(result['has_abi'])
        self.assertEqual(result['contract_name'], 'SafeContract')
        self.assertEqual(result['compiler_version'], 'v0.8.0')
    
    def test_verify_contract_without_source_code(self):
        """Test contract verification without source code"""
        contract_data = {
            'status': '1',
            'message': 'OK',
            'result': [{
                'SourceCode': '',
                'ABI': 'Contract source code not verified',
                'ContractName': '',
                'CompilerVersion': ''
            }]
        }
        
        result = self.verifier.verify_contract(contract_data)
        
        self.assertFalse(result['has_source_code'])
        self.assertFalse(result['has_abi'])
        self.assertIn('Contract source code not verified', result['security_issues'][0])
    
    def test_verify_contract_api_error(self):
        """Test verify_contract with API error status"""
        contract_data = {
            'status': '0',
            'message': 'NOTOK',
            'result': []
        }
        
        result = self.verifier.verify_contract(contract_data)
        
        self.assertFalse(result['verified'])
        self.assertGreater(len(result['warnings']), 0)
    
    def test_check_security_patterns_safe_code(self):
        """Test security pattern checking with safe code"""
        safe_code = "contract Safe { function transfer() public {} }"
        issues = self.verifier._check_security_patterns(safe_code)
        
        self.assertEqual(len(issues), 0)
    
    def test_check_security_patterns_selfdestruct(self):
        """Test security pattern checking with selfdestruct"""
        dangerous_code = "contract Dangerous { function kill() public { selfdestruct(owner); } }"
        issues = self.verifier._check_security_patterns(dangerous_code)
        
        self.assertGreater(len(issues), 0)
        self.assertTrue(any('selfdestruct' in issue for issue in issues))
    
    def test_check_security_patterns_delegatecall(self):
        """Test security pattern checking with delegatecall"""
        dangerous_code = "contract Proxy { function execute() public { target.delegatecall(data); } }"
        issues = self.verifier._check_security_patterns(dangerous_code)
        
        self.assertGreater(len(issues), 0)
        self.assertTrue(any('delegatecall' in issue for issue in issues))
    
    def test_check_security_patterns_tx_origin(self):
        """Test security pattern checking with tx.origin"""
        dangerous_code = "contract Auth { require(tx.origin == owner); }"
        issues = self.verifier._check_security_patterns(dangerous_code)
        
        self.assertGreater(len(issues), 0)
        self.assertTrue(any('tx.origin' in issue for issue in issues))
    
    def test_check_security_patterns_multiple_issues(self):
        """Test security pattern checking with multiple issues"""
        dangerous_code = """
        contract VeryDangerous {
            function destroy() public {
                require(tx.origin == owner);
                target.delegatecall(data);
                selfdestruct(owner);
            }
        }
        """
        issues = self.verifier._check_security_patterns(dangerous_code)
        
        self.assertEqual(len(issues), 3)
    
    @patch('urllib.request.urlopen')
    def test_fetch_and_verify_success(self, mock_urlopen):
        """Test fetch_and_verify with successful result"""
        # Mock response
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = json.dumps({
            'status': '1',
            'message': 'OK',
            'result': [{
                'SourceCode': 'contract Test {}',
                'ABI': '[{"type":"function"}]',
                'ContractName': 'TestContract',
                'CompilerVersion': 'v0.8.0'
            }]
        }).encode('utf-8')
        mock_response.__enter__ = MagicMock(return_value=mock_response)
        mock_response.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_response
        
        result = self.verifier.fetch_and_verify('0x123456789')
        
        self.assertTrue(result['success'])
        self.assertEqual(result['address'], '0x123456789')
        self.assertIn('verification', result)
    
    @patch('urllib.request.urlopen')
    def test_fetch_and_verify_failure(self, mock_urlopen):
        """Test fetch_and_verify with failure"""
        mock_urlopen.side_effect = Exception("Connection failed")
        
        result = self.verifier.fetch_and_verify('0x123456789')
        
        self.assertFalse(result['success'])
        self.assertIn('error', result)


if __name__ == "__main__":
    unittest.main()
