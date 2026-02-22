"""
Contract Verifier module for Etherscan API integration
Fetches and verifies smart contracts using Etherscan API v2
"""

import urllib.request
import urllib.error
import json


class ContractVerifier:
    """Handles contract fetching and verification via Etherscan API"""
    
    def __init__(self, api_key=None):
        """
        Initialize Contract Verifier
        
        Args:
            api_key (str, optional): Etherscan API key for authenticated requests
        """
        self.base_url = "https://api.etherscan.io/v2/api"
        self.api_key = api_key
    
    def fetch_contract(self, address, chain="eth", module="contract", action="getsourcecode"):
        """
        Fetch contract source code and details from Etherscan API
        
        Args:
            address (str): Contract address to fetch
            chain (str): Blockchain network (default: 'eth')
            module (str): API module (default: 'contract')
            action (str): API action (default: 'getsourcecode')
        
        Returns:
            dict: Contract data including source code, ABI, and metadata
        
        Raises:
            ValueError: If address is invalid
            ConnectionError: If API request fails
        """
        if not address or not isinstance(address, str):
            raise ValueError("Contract address must be a valid string")
        
        # Build query parameters
        params = {
            'chainid': chain,
            'module': module,
            'action': action,
            'address': address
        }
        
        if self.api_key:
            params['apikey'] = self.api_key
        
        # Construct URL with query parameters
        query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
        url = f"{self.base_url}?{query_string}"
        
        try:
            # Make GET request
            req = urllib.request.Request(url, method='GET')
            with urllib.request.urlopen(req, timeout=30) as response:
                if response.status != 200:
                    raise ConnectionError(f"API request failed with status {response.status}")
                
                data = json.loads(response.read().decode('utf-8'))
                return data
                
        except urllib.error.URLError as e:
            raise ConnectionError(f"Failed to fetch contract: {str(e)}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response: {str(e)}")
        except Exception as e:
            raise ConnectionError(f"Failed to fetch contract: {str(e)}")
    
    def verify_contract(self, contract_data):
        """
        Verify contract integrity and perform security checks
        
        Args:
            contract_data (dict): Contract data from fetch_contract
        
        Returns:
            dict: Verification results with security assessment
        """
        if not isinstance(contract_data, dict):
            raise ValueError("Contract data must be a dictionary")
        
        verification_result = {
            'verified': False,
            'has_source_code': False,
            'has_abi': False,
            'security_issues': [],
            'warnings': [],
            'contract_name': None,
            'compiler_version': None
        }
        
        # Check if API response is valid
        if contract_data.get('status') != '1':
            verification_result['warnings'].append(
                f"API returned non-success status: {contract_data.get('message', 'Unknown error')}"
            )
            return verification_result
        
        # Extract result data
        result = contract_data.get('result', [])
        if not result or len(result) == 0:
            verification_result['warnings'].append("No contract data found")
            return verification_result
        
        contract_info = result[0] if isinstance(result, list) else result
        
        # Check for source code
        source_code = contract_info.get('SourceCode', '')
        if source_code and source_code != '':
            verification_result['has_source_code'] = True
        else:
            verification_result['security_issues'].append("Contract source code not verified on Etherscan")
        
        # Check for ABI
        abi = contract_info.get('ABI', '')
        if abi and abi != 'Contract source code not verified':
            verification_result['has_abi'] = True
        else:
            verification_result['warnings'].append("Contract ABI not available")
        
        # Extract contract metadata
        verification_result['contract_name'] = contract_info.get('ContractName', 'Unknown')
        verification_result['compiler_version'] = contract_info.get('CompilerVersion', 'Unknown')
        
        # Perform basic security checks on source code
        if verification_result['has_source_code']:
            security_issues = self._check_security_patterns(source_code)
            verification_result['security_issues'].extend(security_issues)
        
        # Overall verification status
        verification_result['verified'] = (
            verification_result['has_source_code'] and 
            len(verification_result['security_issues']) == 0
        )
        
        return verification_result
    
    def _check_security_patterns(self, source_code):
        """
        Check for common security issues in contract source code
        
        Args:
            source_code (str): Contract source code
        
        Returns:
            list: List of security issues found
        """
        issues = []
        
        # Check for dangerous patterns (basic checks)
        dangerous_patterns = [
            ('selfdestruct', 'Contains selfdestruct - potential contract destruction risk'),
            ('delegatecall', 'Uses delegatecall - potential security risk if not properly validated'),
            ('tx.origin', 'Uses tx.origin - phishing attack vulnerability'),
        ]
        
        source_lower = source_code.lower()
        for pattern, message in dangerous_patterns:
            if pattern in source_lower:
                issues.append(message)
        
        return issues
    
    def fetch_and_verify(self, address, chain="eth"):
        """
        Convenience method to fetch and verify a contract in one call
        
        Args:
            address (str): Contract address
            chain (str): Blockchain network (default: 'eth')
        
        Returns:
            dict: Combined fetch and verification results
        """
        try:
            contract_data = self.fetch_contract(address, chain=chain)
            verification_result = self.verify_contract(contract_data)
            
            return {
                'address': address,
                'chain': chain,
                'contract_data': contract_data,
                'verification': verification_result,
                'success': True
            }
        except (ValueError, ConnectionError) as e:
            return {
                'address': address,
                'chain': chain,
                'error': str(e),
                'success': False
            }


if __name__ == "__main__":
    # Demo usage
    print("=" * 70)
    print("CONTRACT VERIFIER - Etherscan API Integration")
    print("=" * 70)
    
    verifier = ContractVerifier()
    
    # Example contract address (USDT on Ethereum)
    example_address = "0xdac17f958d2ee523a2206206994597c13d831ec7"
    
    print(f"\n📋 Fetching contract: {example_address}")
    print("-" * 70)
    
    result = verifier.fetch_and_verify(example_address)
    
    if result['success']:
        verification = result['verification']
        print(f"✅ Contract Name: {verification['contract_name']}")
        print(f"🔧 Compiler Version: {verification['compiler_version']}")
        print(f"📄 Has Source Code: {verification['has_source_code']}")
        print(f"📜 Has ABI: {verification['has_abi']}")
        print(f"✓ Verified: {verification['verified']}")
        
        if verification['security_issues']:
            print(f"\n⚠️  Security Issues Found: {len(verification['security_issues'])}")
            for issue in verification['security_issues']:
                print(f"   - {issue}")
        
        if verification['warnings']:
            print(f"\n⚡ Warnings: {len(verification['warnings'])}")
            for warning in verification['warnings']:
                print(f"   - {warning}")
    else:
        print(f"❌ Error: {result['error']}")
    
    print("\n" + "=" * 70)
