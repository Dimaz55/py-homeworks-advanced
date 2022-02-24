from unittest import TestCase
from app import *
from unittest.mock import patch


class TestSecretary(TestCase):
    def test_check_document_existance_doc_exist(self):
        self.assertTrue(check_document_existance('10006'))

    def test_check_document_existance_doc_not_exist(self):
        self.assertFalse(check_document_existance('10005'))
    
    def test_get_doc_owner_name_owner_exist(self):
        with patch('builtins.input', return_value='11-2'):
            owner = get_doc_owner_name()
        self.assertEqual(owner, 'Геннадий Покемонов')

    def test_get_doc_owner_name_owner_not_exist(self):
        with patch('builtins.input', return_value='11-3'):
            owner = get_doc_owner_name()
        self.assertIsNone(owner)
    
    def test_get_all_doc_owners_names(self):
        unique_users = get_all_doc_owners_names()
        users = set([el['name'] for el in documents])
        self.assertEqual(unique_users, users)
    
    def test_remove_doc_from_shelf_doc_exist(self):
        result = remove_doc_from_shelf('10006')
        self.assertNotIn('10006', directories['2'])

    def test_remove_doc_from_shelf_doc_not_exist(self):
        result = remove_doc_from_shelf('10001')
        self.assertFalse(result)
    
    def test_add_new_shelf_shelf_not_exist(self):
        self.assertEqual(add_new_shelf('4'), ('4', True))

    def test_add_new_shelf_shelf_exist(self):
        self.assertEqual(add_new_shelf('3'), ('3', False))

    def test_add_new_shelf_shelf_arg_not_specified(self):
        with patch('builtins.input', return_value=''):
            self.assertEqual(add_new_shelf(), ('', True))
    
    def test_append_doc_to_shelf(self):
        append_doc_to_shelf('123', '3')
        self.assertIn('123', directories['3'])
    
    def test_delete_doc(self):
        with patch('builtins.input', return_value='10006'):
            result = delete_doc()
        self.assertEqual(result, ('10006', True))

    def test_delete_non_exist_doc(self):
        with patch('builtins.input', return_value='10007'):
            result = delete_doc()
        self.assertIsNone(result)
    
    def test_get_doc_shelf(self):
        result = get_doc_shelf('123')
        self.assertEqual(result, '3')

    def test_get_non_exist_doc_shelf(self):
        result = get_doc_shelf('10007')
        self.assertIsNone(result)
    
    def test_show_document_info(self):
        result = show_document_info(documents[2])
        self.assertEqual(result, (documents[2]['type'],
                                  documents[2]['number'],
                                  documents[2]['name']))
    
    def test_add_new_doc(self):
        new_doc = ['123', 'new_type', 'John Doe']
        to_shelf = '3'
        add_new_doc(*new_doc, to_shelf)
        doc_values = [_ for _ in documents[3].values()]
        self.assertEqual(set(new_doc),  set(doc_values))
        self.assertIn('123', directories['3'])
