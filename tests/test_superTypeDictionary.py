from unittest import TestCase
import tulippaths as tp

class TestSuperTypeDictionary(TestCase):

    def test_getDictionary(self):
        superTypes = tp.SuperTypeDictionary()
        self.assertTrue(len(superTypes.getDictionary()) == 11)

    def test_getSuperTypeFromType(self):
        superTypes = tp.SuperTypeDictionary()
        self.assertTrue(superTypes.getSuperTypeFromType('CBb4w') == 'CBb')
        self.assertTrue(superTypes.getSuperTypeFromType('AC') == 'YAC')
        self.assertFalse(superTypes.getSuperTypeFromType('CBb3m') == 'AC')

    def test_getTypesFromSuperType(self):
        superTypes = tp.SuperTypeDictionary()
        self.assertTrue(len(superTypes.getTypesFromSuperType('CBb')) == 23)

    def test_isTypeInSuperType(self):
        superTypes = tp.SuperTypeDictionary()
        self.assertTrue(superTypes.isTypeInSuperType('CBb4w', 'CBb'))
        self.assertFalse(superTypes.isTypeInSuperType('AC', 'CBb'))

    def test_isTypeInSuperTypes(self):
        superTypes = tp.SuperTypeDictionary()
        self.assertTrue(superTypes.isTypeInSuperTypes('CBb4w', ['CBb', 'CBa']))
        self.assertTrue(superTypes.isTypeInSuperTypes('AC', ['CBb', 'YAC']))