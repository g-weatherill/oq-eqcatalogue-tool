import unittest

from datetime import datetime

from tests.test_utils import in_data_dir
from eqcatalogue import (
    CatalogueDatabase, GroupMeasuresBySequentialClustering, C)


class DuplicateFindingTestCase(unittest.TestCase):
    """
    It loads two catalogues in different format. The first one is an
    ISF bulletin, with the measures already grouped (by the event
    source key). The second one contains the same set of measures but
    in IASPEI format. We apply the sequential grouping to see if the
    created group matches the group present in the ISF bulletin.
    """

    def setUp(self):
        self.cat = CatalogueDatabase(memory=True, filename="eqcatalogue.db")

        isf_bulletin_filename = "isf_two_events.txt"
        iaspei_filename = "iaspei_from_isf.csv"

        self.cat.load_file(in_data_dir(isf_bulletin_filename), "isf_bulletin")
        self.cat.load_file(in_data_dir(iaspei_filename), "iaspei")

    def test_match(self):
        grouper = GroupMeasuresBySequentialClustering(
            time_window=10, space_window=200)

        groups = grouper.group_measures(C())

        self.assertEqual(2, len(groups.values()))

        actual_groups = set([frozenset(measures)
                             for measures in groups.values()])

        expected_groups = set([frozenset(C(before=datetime(1952, 1, 1))),
                               frozenset(C(after=datetime(1997, 1, 1)))])

        self.assertEqual(expected_groups, actual_groups)