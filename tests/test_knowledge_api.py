import os
import tempfile
import unittest

from knowledge_api import create_knowledge_item, init_db, search_knowledge
from server import check_api_key


class KnowledgeApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp_dir = tempfile.mkdtemp(prefix="petpal-test-", dir="/tmp")
        self.db_path = os.path.join(self.tmp_dir, "petpal.db")

    def test_init_db_and_search(self) -> None:
        init_db(self.db_path)
        created = create_knowledge_item(
            title="Vaccination schedule",
            content="Pets should receive vaccines based on a veterinary plan.",
            tags="health,vaccines",
            source="test",
            db_path=self.db_path,
        )
        self.assertEqual(created["title"], "Vaccination schedule")

        results = search_knowledge("vaccines", db_path=self.db_path)
        self.assertGreaterEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Vaccination schedule")

    def test_check_api_key(self) -> None:
        self.assertTrue(check_api_key(None, None))
        self.assertTrue(check_api_key(None, "anything"))
        self.assertTrue(check_api_key("secret", "secret"))
        self.assertFalse(check_api_key("secret", "wrong"))


if __name__ == "__main__":
    unittest.main()
