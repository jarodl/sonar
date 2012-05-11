import unittest
from sonar.models.base import BaseItem

class BaseItemTests(unittest.TestCase):

    def tearDown(self):
        BaseItem.clear()

    def test_all(self):
        for i in range(10):
            item = BaseItem('ident-%d' % i)
            item.save()
        self.assertEquals(len(BaseItem.all()), 10)

    def test_get(self):
        item = BaseItem('ident')
        self.assertEquals(BaseItem.get('ident'), None)
        item.save()
        self.assertEquals(BaseItem.get('ident').ident, 'ident')

    def test_exists(self):
        item = BaseItem('ident')
        self.assertFalse(BaseItem.exists(item))
        item.save()
        self.assertTrue(BaseItem.exists(item))

    def test_make_key(self):
        item = BaseItem('ident')
        self.assertEquals(item.redis_key, 'BaseItem:ident')

    def test_update(self):
        item = BaseItem('ident', object_id='object_id')
        item.save()
        item.object_id = 'different_object_id'
        item.update()
        self.assertEquals(item.object_id, 'object_id')

    def test_delete(self):
        item = BaseItem('ident')
        item.save()
        item.delete()
        self.assertFalse(BaseItem.get('ident'))

if __name__ == '__main__':
    unittest.main()
