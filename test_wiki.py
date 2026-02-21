"""
Tests for Kairos Blockchain Wiki
"""

import unittest
import os


class TestWiki(unittest.TestCase):
    """Test cases for Wiki HTML file"""
    
    def test_wiki_file_exists(self):
        """Test that wiki.html file exists"""
        wiki_path = os.path.join(os.path.dirname(__file__), 'wiki.html')
        self.assertTrue(os.path.exists(wiki_path), "wiki.html file should exist")
    
    def test_wiki_content_structure(self):
        """Test that wiki.html contains expected content"""
        wiki_path = os.path.join(os.path.dirname(__file__), 'wiki.html')
        with open(wiki_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for key content elements
        self.assertIn('Kairos Blockchain Wiki', content)
        self.assertIn('Birthdate:', content)
        self.assertIn('Purpose:', content)
        self.assertIn('Destiny:', content)
        self.assertIn('Challenges:', content)
        self.assertIn('Triumphs:', content)
        self.assertIn('Global blockchain innovation and security', content)
        self.assertIn('The Great Fork of 2025', content)
        self.assertIn('The Shadow Hack of 2026', content)
        self.assertIn('Universal Adoption', content)
        self.assertIn('Cosmic Alignment', content)
    
    def test_wiki_html_structure(self):
        """Test that wiki.html has valid HTML structure"""
        wiki_path = os.path.join(os.path.dirname(__file__), 'wiki.html')
        with open(wiki_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for basic HTML elements
        self.assertIn('<!DOCTYPE html>', content)
        self.assertIn('<html', content)
        self.assertIn('<head>', content)
        self.assertIn('<body>', content)
        self.assertIn('</html>', content)
        self.assertIn('<h1>', content)
        self.assertIn('<h2>', content)
        self.assertIn('<ol>', content)
        self.assertIn('<li>', content)


if __name__ == "__main__":
    unittest.main()
