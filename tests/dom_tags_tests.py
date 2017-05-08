import sys
sys.path.insert(0, "../")
import unittest

from dom_tags import DomainTags

class TestDomainTags(unittest.TestCase):
 
    def test_get_domain_len(self):
        dom=DomainTags()
        self.assertEqual( len(dom.get_domain_tag("google.com")), 3)

if __name__ == '__main__':
    unittest.main(exit=False)
