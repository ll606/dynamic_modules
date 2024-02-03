from unittest import TestCase 
from attribute_dictionary import AttributeDictionary



class TestAttributeDictionary(TestCase):
    
    def test_attr_dict(self):
        attr_dict = AttributeDictionary()
        attr_dict.name = 'test123'
        self.assertEqual(attr_dict.name, 'test123')
        
        del attr_dict.name
        
        self.assertFalse(
            hasattr(attr_dict, 'name'), 
            'AttributeDictionary cannot delete attributes!'
        )
    
    def test_keys_update_clear(self):
        attr_dict = AttributeDictionary()
        attr_dict.update(dict(zip(range(100), range(100))))
        
        self.assertEqual(
            list(attr_dict.keys()), list(range(100))
        )
        
        attr_dict.clear()
        self.assertEqual(
            attr_dict, AttributeDictionary()
        )
        
    def test_pop(self):
        attr_dict = AttributeDictionary()
        attr_dict.update(dict(zip(range(100), range(100))))
        
        self.assertEqual(
            attr_dict.pop(1), 1
        )
        