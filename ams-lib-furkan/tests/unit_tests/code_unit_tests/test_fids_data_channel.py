"""Tests for Component Versions class and parsing"""

# pylint: disable=line-too-long
import unittest
import json
from ams.fid_api_calls.cache.data_channel import FidsDataChannelWebSocket


class TestFidsDataChannel(unittest.TestCase):
    """Unit Tests for the ComponentVersion class's compare functions"""

    def test_data_apply(self):
        """This test is a copy from RE, it should not be changed unless the RE test is changed."""
        ws = FidsDataChannelWebSocket(
            url="wss://none.test/data/channel",
            monitor_id="TEST",
            cli_id="TEST",
            home_airport="XXXX",
        )
        ws.register_view("viewTest", "Select Test_Data")

        update = json.loads(
            """{"data":{"viewTest":[{"N":{"0":{"flightKey":1}},"U":{"1":{"flightKey":2},"2":{"flightKey":4}}}]},"metaData":{"viewTest":{"idProperty":"flightKey"}}}"""
        )
        ws.apply_updates(update)

        view_test_result_list = ws.get_snapshot("viewTest")
        self.assertEqual(len(view_test_result_list), 3)
        self.assertEqual(view_test_result_list[0]["flightKey"], 1)
        self.assertEqual(view_test_result_list[1]["flightKey"], 2)
        self.assertEqual(view_test_result_list[2]["flightKey"], 4)

        update = json.loads(
            """{"data":{"viewTest":[{"N":{"0":{"dat":99,"flightKey":1},"1":{"dat":88,"flightKey":2},"2":{"dat":77,"flightKey":4}}}]},"metaData":{"viewTest":{"idProperty":"flightKey"}}} """
        )

        ws.apply_updates(update)
        view_test_result_list = ws.get_snapshot("viewTest")
        self.assertEqual(len(view_test_result_list), 3)
        self.assertEqual(view_test_result_list[0]["flightKey"], 1)
        self.assertEqual(view_test_result_list[0]["dat"], 99)
        self.assertEqual(view_test_result_list[1]["flightKey"], 2)
        self.assertEqual(view_test_result_list[1]["dat"], 88)
        self.assertEqual(view_test_result_list[2]["flightKey"], 4)
        self.assertEqual(view_test_result_list[2]["dat"], 77)

        update = json.loads(
            """{"data":{"viewTest":[{"D":{"2":{"flightKey":4}},"N":{"2":{"dat":22,"flightKey":44},"3":{"dat":23,"flightKey":55}},"U":{"0":{"dat":10,"flightKey":1},"1":{"dat":20,"flightKey":2}}}]},"metaData":{"viewTest":{"idProperty":"flightKey"}}}"""
        )

        ws.apply_updates(update)
        view_test_result_list = ws.get_snapshot("viewTest")
        self.assertEqual(len(view_test_result_list), 4)
        self.assertEqual(view_test_result_list[0]["flightKey"], 1)
        self.assertEqual(view_test_result_list[0]["dat"], 10)
        self.assertEqual(view_test_result_list[1]["flightKey"], 2)
        self.assertEqual(view_test_result_list[1]["dat"], 20)
        self.assertEqual(view_test_result_list[2]["flightKey"], 44)
        self.assertEqual(view_test_result_list[2]["dat"], 22)
        self.assertEqual(view_test_result_list[3]["flightKey"], 55)
        self.assertEqual(view_test_result_list[3]["dat"], 23)

        update = json.loads(
            """{"data":{"viewTest":[{"D":{"2":{"flightKey":44}},"M":{"6":3},"U":{"0":{"dat":11,"flightKey":1},"1":{"dat":12,"flightKey":2},"2":{"dat":13,"flightKey":3},"3":{"dat":14,"flightKey":4},"4":{"dat":15,"flightKey":5},"5":{"dat":16,"flightKey":6}}}]},"metaData":{"viewTest":{"idProperty":"flightKey"}}}"""
        )

        ws.apply_updates(update)
        view_test_result_list = ws.get_snapshot("viewTest")
        self.assertEqual(len(view_test_result_list), 7)
        self.assertEqual(view_test_result_list[0]["flightKey"], 1)
        self.assertEqual(view_test_result_list[0]["dat"], 11)
        self.assertEqual(view_test_result_list[1]["flightKey"], 2)
        self.assertEqual(view_test_result_list[1]["dat"], 12)
        self.assertEqual(view_test_result_list[2]["flightKey"], 3)
        self.assertEqual(view_test_result_list[2]["dat"], 13)
        self.assertEqual(view_test_result_list[3]["flightKey"], 4)
        self.assertEqual(view_test_result_list[3]["dat"], 14)
        self.assertEqual(view_test_result_list[4]["flightKey"], 5)
        self.assertEqual(view_test_result_list[4]["dat"], 15)
        self.assertEqual(view_test_result_list[5]["flightKey"], 6)
        self.assertEqual(view_test_result_list[5]["dat"], 16)
        self.assertEqual(view_test_result_list[6]["flightKey"], 55)
        self.assertEqual(view_test_result_list[6]["dat"], 23)

        update = json.loads(
            """{"data":{"viewTest":[{"D":{"0":{"flightKey":1},"1":{"flightKey":2},"2":{"flightKey":3},"3":{"flightKey":4},"4":{"flightKey":5},"5":{"flightKey":6}},"M":{"0":6}}]},"metaData":{"viewTest":{"idProperty":"flightKey"}}}"""
        )
        ws.apply_updates(update)
        view_test_result_list = ws.get_snapshot("viewTest")
        self.assertEqual(len(view_test_result_list), 1)

        update = json.loads(
            """{"data":{"viewTest":[{"D":{"0":{"flightKey":55},"1":{"flightKey":2}}}]},"metaData":{"viewTest":{"idProperty":"flightKey"}}}"""
        )
        ws.apply_updates(update)
        view_test_result_list = ws.get_snapshot("viewTest")
        self.assertEqual(len(view_test_result_list), 0)

        update = json.loads(
            """{"data":{"viewTest":[{"N":{"0":{"flightKey":66},"1":{"flightKey":77}}}]},"metaData":{"viewTest":{"idProperty":"flightKey"}}}"""
        )
        ws.apply_updates(update)
        view_test_result_list = ws.get_snapshot("viewTest")
        self.assertEqual(len(view_test_result_list), 2)
        self.assertEqual(view_test_result_list[0]["flightKey"], 66)
        self.assertEqual(view_test_result_list[1]["flightKey"], 77)

        update = json.loads(
            """{"data":{"viewTest":[{"U":{"0":{"dat":20,"flightKey":66}}}]},"metaData":{"viewTest":{"idProperty":"flightKey"}}}"""
        )
        ws.apply_updates(update)
        view_test_result_list = ws.get_snapshot("viewTest")
        self.assertEqual(len(view_test_result_list), 2)
        self.assertEqual(view_test_result_list[0]["flightKey"], 66)
        self.assertEqual(view_test_result_list[1]["flightKey"], 77)

        ws.close()


if __name__ == "__main__":
    unittest.main()
