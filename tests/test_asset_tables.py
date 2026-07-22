import unittest

from eye_mystery.asset_tables import assigned_string_list, lua_tables


class AssetTableTests(unittest.TestCase):
    def test_ignores_commas_and_braces_in_literals_and_comments(self) -> None:
        source = '''
        ignored = "{,}"
        -- { fake, table }
        opts = { "A,B", "C", nested(1, 2), { 3, 4 }, "E" }
        '''
        tables = lua_tables(source)
        self.assertEqual(len(tables), 2)
        self.assertEqual(tables[0].assigned_name, "opts")
        self.assertEqual(tables[0].item_count, 5)
        self.assertEqual(tables[0].keyed_item_count, 0)
        self.assertEqual(tables[1].item_count, 2)

    def test_distinguishes_five_field_record_from_five_value_list(self) -> None:
        source = "record={a=1,b=2,c=3,d=4,e=5}; values={1,2,3,4,5}"
        tables = lua_tables(source)
        self.assertEqual(
            tuple((table.assigned_name, table.item_count, table.keyed_item_count) for table in tables),
            (("record", 5, 5), ("values", 5, 0)),
        )

    def test_extracts_simple_assigned_string_list(self) -> None:
        source = "other={'x'}; gun_names = {'Deadly', \"Type x\", 'Online',}"
        self.assertEqual(
            assigned_string_list(source, "gun_names"),
            ("Deadly", "Type x", "Online"),
        )

    def test_rejects_non_string_items(self) -> None:
        with self.assertRaisesRegex(ValueError, "items but"):
            assigned_string_list("values={'a', 2}", "values")


if __name__ == "__main__":
    unittest.main()
