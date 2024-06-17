import unittest
from unittest.mock import patch, MagicMock

from orbis2.business_logic.orbis_service import OrbisService
from orbis2.model.corpus import Corpus
from orbis2.model.run import Run


class TestOrbisService(unittest.TestCase):

    def setUp(self):
        # Create a mock for the cache
        self.mock_cache = MagicMock()

        # Patch the cache object in the orbis_service module
        patcher = patch('orbis2.database.logging_cache.cache', self.mock_cache)
        self.addCleanup(patcher.stop)
        self.mock_cache = patcher.start()

    def test_cache_invalidation_on_add_run(self):
        orbis_service = OrbisService()

        run = Run(name="Test Run", description="Description",
                  corpus=Corpus(name="Test Corpus", supported_annotation_types=[]), document_annotations={},
                  is_gold_standard=True)

        # Check initial cache state
        orbis_service.get_runs()
        # self.assertTrue(self.mock_cache.__getitem__.called)

        # Call add_run and ensure cache is invalidated
        orbis_service.add_run(run)
        # self.assertTrue(self.mock_cache.clear.called)
        #
        # Ensure get_runs re-populates the cache
        orbis_service.get_runs()
        # self.assertTrue(self.mock_cache.__getitem__.called)


if __name__ == '__main__':
    unittest.main()
