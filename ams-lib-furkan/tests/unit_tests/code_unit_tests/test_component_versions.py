"""Tests for Component Versions class and parsing"""

# pylint: disable=line-too-long
# pylint: disable = protected-access

import unittest
import json
from ams.initalize_ams_test.component_versions import (
    ComponentVersion,
    parse_version,
    get_component_versions_from_json,
    get_esb_repo_versions_from_json,
)


class TestComponentVersions(unittest.TestCase):
    """Unit Tests for the ComponentVersion class's compare functions"""

    def test_get_component_versions_from_json(self):
        """Test parsing the payload from the /versions call"""
        versions = get_component_versions_from_json(json.loads(self.versions_payload))
        self.assertEqual(versions["aaa"], "5.2.78")
        self.assertEqual(versions["afv"], "3.12.11")
        self.assertEqual(versions["cfg"], "5.6.32")
        self.assertEqual(versions["msc"], "2.29.40")
        self.assertEqual(versions["tam"], "10.8.7")

    def test_get_esb_repo_versions_from_json(self):
        """Test parsing the payload from the /versions call for esb repos"""
        repo_versions = get_esb_repo_versions_from_json(json.loads(self.esb_payload))
        self.assertEqual(repo_versions["altea-core-repo"], "1.1.16")
        self.assertEqual(repo_versions["den-repo"], "1.1.5")
        self.assertEqual(repo_versions["finavia-repo"], "1.1.12.5")

    def test_equals_numbers(self):
        """Tests the equals and not equals of the ComponentVersions class"""
        self.assertEqual(
            ComponentVersion(None),
            ComponentVersion(None),
        )
        self.assertNotEqual(ComponentVersion(9), ComponentVersion(7))
        self.assertEqual(ComponentVersion(9), ComponentVersion(9))
        self.assertNotEqual(ComponentVersion(9, 1), ComponentVersion(9, 2))
        self.assertEqual(ComponentVersion(9, 2), ComponentVersion(9, 2))
        self.assertNotEqual(ComponentVersion(9, 1), ComponentVersion(9, 2))
        self.assertEqual(ComponentVersion(9, 2, 100), ComponentVersion(9, 2, 100))
        self.assertNotEqual(ComponentVersion(9, 1, 200), ComponentVersion(9, 2, 100))
        self.assertEqual(
            ComponentVersion(9, 2, 100, 10), ComponentVersion(9, 2, 100, 10)
        )
        self.assertNotEqual(
            ComponentVersion(9, 1, 200, 10), ComponentVersion(9, 2, 100, 12)
        )

    def test_equals_alphanumeric(self):
        """Test versions with letters and numbers"""
        self.assertEqual(ComponentVersion(9, 2, "25a"), ComponentVersion(9, 2, "25a"))
        self.assertNotEqual(
            ComponentVersion(9, 1, "100a"), ComponentVersion(9, 2, "500a")
        )
        self.assertEqual(
            ComponentVersion(9, 2, 100, "a"), ComponentVersion(9, 2, 100, "a")
        )
        self.assertNotEqual(
            ComponentVersion(9, 1, 200, "a"), ComponentVersion(9, 2, 100, "z")
        )

    def test_compare_numbers(self):
        """Test version comparison"""
        self.assertTrue(ComponentVersion(9) < ComponentVersion(10))
        self.assertFalse(ComponentVersion(9) > ComponentVersion(10))
        self.assertTrue(ComponentVersion(9, 10) < ComponentVersion(10, 11))
        self.assertTrue(ComponentVersion(9, 10) < ComponentVersion(10, 10, 12))
        self.assertTrue(ComponentVersion(9, 10) < ComponentVersion(10, 10, 12, 100))
        self.assertTrue(ComponentVersion(9, 10, 100) < ComponentVersion(10, 10, 200))
        self.assertTrue(
            ComponentVersion(9, 10, 100, 25) < ComponentVersion(10, 10, 200, 50)
        )
        self.assertFalse(
            ComponentVersion(9, 10, 100, 25) > ComponentVersion(10, 10, 200, 50)
        )
        self.assertTrue(
            ComponentVersion(9, 10, 100, 25) <= ComponentVersion(10, 10, 200, 50)
        )
        self.assertTrue(
            ComponentVersion(10, 10, 200, 50) <= ComponentVersion(10, 10, 200, 50)
        )
        self.assertFalse(
            ComponentVersion(9, 10, 100, 25) >= ComponentVersion(10, 10, 200, 50)
        )

    def test_compare_alphanumeric(self):
        """Test version compaison with versions with letters"""
        self.assertTrue(
            ComponentVersion(9, 10, "25d") < ComponentVersion(10, 10, "25g")
        )
        self.assertFalse(
            ComponentVersion(9, 10, "25d") > ComponentVersion(10, 10, "25g")
        )
        self.assertTrue(
            ComponentVersion(9, 10, "25d", "a") < ComponentVersion(10, 10, "25d", "z")
        )
        self.assertFalse(
            ComponentVersion(9, 10, "25d", "a") > ComponentVersion(10, 10, "25d", "z")
        )

    def test_parsing(self):
        """Test parse_vesion function with varies version strings"""
        self.assertEqual(ComponentVersion(9, 10, 1), parse_version("9.10.1"))
        self.assertEqual(ComponentVersion(9, 10), parse_version("9.10"))
        self.assertEqual(
            ComponentVersion(
                9,
            ),
            parse_version("9."),
        )
        self.assertEqual(
            ComponentVersion(
                10,
            ),
            parse_version("10"),
        )
        self.assertEqual(ComponentVersion(9, 10, 1, 5), parse_version("9.10.1.5"))
        self.assertEqual(ComponentVersion(9, 10, 1, 5), parse_version("9.10.1-5"))
        self.assertEqual(ComponentVersion(9, 10, 1, "a"), parse_version("9.10.1-a"))
        self.assertEqual(ComponentVersion(9, 10, "1a"), parse_version("9.10.1a"))
        self.assertEqual(
            ComponentVersion(2025, 4, 4, 1825), parse_version("202504041825")
        )
        self.assertEqual(
            ComponentVersion(2024, 12, 12, 21), parse_version("202412120021")
        )
        self.assertEqual(
            ComponentVersion(
                "v5",
            ),
            parse_version("v5"),
        )
        self.assertRaises(ValueError, parse_version, None)

    # example payloads
    versions_payload = '{"deployments":{"aptams-aaa-qcp2":{"containers":{"aptams-aaa-qcp2":{"image":"docker-production-aptams/aptams/aaa:5.2.78","resources":{"limits":{"ephemeral-storage":"45Gi","memory":"6Gi"},"requests":{"cpu":"1","ephemeral-storage":"45Gi","memory":"6Gi"}}}},"init_containers":{"certificate-management":{"image":"docker-registry-redhat-io-remote/redhat-sso-7/sso71-openshift:1.1-16","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"200m","ephemeral-storage":"1Gi","memory":"1Gi"}}},"ldbtools-copy-sql-from-product-image":{"image":"docker-production-aptams/aptams/aaa:5.2.78","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"100m","ephemeral-storage":"1Gi","memory":"1Gi"}}},"ldbtools-update-db":{"image":"docker-production-aptams/aptams/ldbtools:1.0.34","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"200m","ephemeral-storage":"1Gi","memory":"1Gi"}}}},"pods":{}},"aptams-afv-qcp2":{"containers":{"aptams-afv-qcp2":{"image":"docker-production-aptams/aptams/afv:3.12.11","resources":{"limits":{"ephemeral-storage":"45Gi","memory":"3Gi"},"requests":{"cpu":"800m","ephemeral-storage":"45Gi","memory":"3Gi"}}}},"init_containers":{"afv-maptiles-update":{"image":"docker-registry-redhat-io-remote/redhat-sso-7/sso71-openshift:1.1-16","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"2","ephemeral-storage":"1Gi","memory":"1Gi"}}},"certificate-management":{"image":"docker-registry-redhat-io-remote/redhat-sso-7/sso71-openshift:1.1-16","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"200m","ephemeral-storage":"1Gi","memory":"1Gi"}}},"ldbtools-copy-sql-from-product-image":{"image":"docker-production-aptams/aptams/afv:3.12.11","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"100m","ephemeral-storage":"1Gi","memory":"1Gi"}}},"ldbtools-update-db":{"image":"docker-production-aptams/aptams/ldbtools:1.0.34","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"200m","ephemeral-storage":"1Gi","memory":"1Gi"}}}},"pods":{}},"aptams-amg-qcp2":{"containers":{"aptams-amg-qcp2":{"image":"docker-production-aptams/aptams/amg:10.6.143","resources":{"limits":{"ephemeral-storage":"45Gi","memory":"5Gi"},"requests":{"cpu":"1","ephemeral-storage":"45Gi","memory":"5Gi"}}}},"init_containers":{"certificate-management":{"image":"docker-registry-redhat-io-remote/redhat-sso-7/sso71-openshift:1.1-16","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"200m","ephemeral-storage":"1Gi","memory":"1Gi"}}},"ldbtools-copy-sql-from-product-image":{"image":"docker-production-aptams/aptams/amg:10.6.143","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"100m","ephemeral-storage":"1Gi","memory":"1Gi"}}},"ldbtools-update-db":{"image":"docker-production-aptams/aptams/ldbtools:1.0.34","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"200m","ephemeral-storage":"1Gi","memory":"1Gi"}}}},"pods":{}},"aptams-amo-qcp2":{"containers":{"aptams-amo-qcp2":{"image":"docker-production-aptams/aptams/apt-monitoring:5.2.27","resources":{"limits":{"ephemeral-storage":"45Gi","memory":"5Gi"},"requests":{"cpu":"500m","ephemeral-storage":"45Gi","memory":"5Gi"}}}},"init_containers":{"certificate-management":{"image":"docker-registry-redhat-io-remote/redhat-sso-7/sso71-openshift:1.1-16","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"200m","ephemeral-storage":"1Gi","memory":"1Gi"}}},"ldbtools-copy-sql-from-product-image":{"image":"docker-production-aptams/aptams/apt-monitoring:5.2.27","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"100m","ephemeral-storage":"1Gi","memory":"1Gi"}}},"ldbtools-update-db":{"image":"docker-production-aptams/aptams/ldbtools:1.0.34","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"200m","ephemeral-storage":"1Gi","memory":"1Gi"}}}},"pods":{}},"aptams-cds-qcp2":{"containers":{"aptams-cds-qcp2":{"image":"docker-production-aptams/aptams/cds:2.1.25","resources":{"limits":{"ephemeral-storage":"45Gi","memory":"5Gi"},"requests":{"cpu":"500m","ephemeral-storage":"45Gi","memory":"5Gi"}}}},"init_containers":{"certificate-management":{"image":"docker-registry-redhat-io-remote/redhat-sso-7/sso71-openshift:1.1-16","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"200m","ephemeral-storage":"1Gi","memory":"1Gi"}}},"ldbtools-copy-sql-from-product-image":{"image":"docker-production-aptams/aptams/cds:2.1.25","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"100m","ephemeral-storage":"1Gi","memory":"1Gi"}}},"ldbtools-update-db":{"image":"docker-production-aptams/aptams/ldbtools:1.0.34","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"200m","ephemeral-storage":"1Gi","memory":"1Gi"}}}},"pods":{}},"aptams-cfg-qcp2":{"containers":{"aptams-cfg-qcp2":{"image":"docker-production-aptams/aptams/shared-configuration:5.6.32","resources":{"limits":{"ephemeral-storage":"45Gi","memory":"5Gi"},"requests":{"cpu":"2","ephemeral-storage":"45Gi","memory":"5Gi"}}}},"init_containers":{"certificate-management":{"image":"docker-registry-redhat-io-remote/redhat-sso-7/sso71-openshift:1.1-16","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"200m","ephemeral-storage":"1Gi","memory":"1Gi"}}},"ldbtools-copy-sql-from-product-image":{"image":"docker-production-aptams/aptams/shared-configuration:5.6.32","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"100m","ephemeral-storage":"1Gi","memory":"1Gi"}}},"ldbtools-update-db":{"image":"docker-production-aptams/aptams/ldbtools:1.0.34","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"200m","ephemeral-storage":"1Gi","memory":"1Gi"}}}},"pods":{}},"aptams-csv-qcp2":{"containers":{"aptams-csv-qcp2":{"image":"docker-production-aptams/aptams/core-services:1.20.5","resources":{"limits":{"ephemeral-storage":"45Gi","memory":"8Gi"},"requests":{"cpu":"2","ephemeral-storage":"45Gi","memory":"8Gi"}}}},"init_containers":{"certificate-management":{"image":"docker-registry-redhat-io-remote/redhat-sso-7/sso71-openshift:1.1-16","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"200m","ephemeral-storage":"1Gi","memory":"1Gi"}}}},"pods":{}},"aptams-dfib-qcp2":{"containers":{"aptams-dfib-qcp2":{"image":"docker-production-aptams/aptams/df-ib:2.0.16","resources":{"limits":{"ephemeral-storage":"45Gi","memory":"6Gi"},"requests":{"cpu":"1","ephemeral-storage":"45Gi","memory":"6Gi"}}}},"init_containers":{"certificate-management":{"image":"docker-registry-redhat-io-remote/redhat-sso-7/sso71-openshift:1.1-16","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"200m","ephemeral-storage":"1Gi","memory":"1Gi"}}},"ldbtools-copy-sql-from-product-image":{"image":"docker-production-aptams/aptams/df-ib:2.0.16","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"100m","ephemeral-storage":"1Gi","memory":"1Gi"}}},"ldbtools-update-db":{"image":"docker-production-aptams/aptams/ldbtools:1.0.34","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"200m","ephemeral-storage":"1Gi","memory":"1Gi"}}}},"pods":{}},"aptams-esb-qcp2":{"containers":{"aptams-esb-qcp2":{"image":"docker-production-aptams/aptams/esb:202504041825","resources":{"limits":{"ephemeral-storage":"45Gi","memory":"12Gi"},"requests":{"cpu":"2","ephemeral-storage":"45Gi","memory":"12Gi"}}}},"init_containers":{"certificate-management":{"image":"docker-registry-redhat-io-remote/redhat-sso-7/sso71-openshift:1.1-16","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"200m","ephemeral-storage":"1Gi","memory":"1Gi"}}}},"pods":{}},"aptams-fds-qcp2":{"containers":{"aptams-fds-qcp2":{"image":"docker-production-aptams/aptams/fds:3.11.1-103","resources":{"limits":{"ephemeral-storage":"45Gi","memory":"14Gi"},"requests":{"cpu":"2","ephemeral-storage":"45Gi","memory":"14Gi"}}}},"init_containers":{"certificate-management":{"image":"docker-registry-redhat-io-remote/redhat-sso-7/sso71-openshift:1.1-16","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"200m","ephemeral-storage":"1Gi","memory":"1Gi"}}},"ldbtools-copy-sql-from-product-image":{"image":"docker-production-aptams/aptams/fds:3.11.1-103","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"100m","ephemeral-storage":"1Gi","memory":"1Gi"}}},"ldbtools-update-db":{"image":"docker-production-aptams/aptams/ldbtools:1.0.34","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"200m","ephemeral-storage":"1Gi","memory":"1Gi"}}}},"pods":{}},"aptams-fid-qcp2":{"containers":{"aptams-fid-qcp2":{"image":"docker-production-aptams/aptams/fids:3.1.0-47","resources":{"limits":{"ephemeral-storage":"45Gi","memory":"12Gi"},"requests":{"cpu":"1","ephemeral-storage":"45Gi","memory":"12Gi"}}}},"init_containers":{"certificate-management":{"image":"docker-registry-redhat-io-remote/redhat-sso-7/sso71-openshift:1.1-16","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"200m","ephemeral-storage":"1Gi","memory":"1Gi"}}},"ldbtools-copy-sql-from-product-image":{"image":"docker-production-aptams/aptams/fids:3.1.0-47","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"100m","ephemeral-storage":"1Gi","memory":"1Gi"}}},"ldbtools-update-db":{"image":"docker-production-aptams/aptams/ldbtools:1.0.34","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"200m","ephemeral-storage":"1Gi","memory":"1Gi"}}}},"pods":{}},"aptams-fom-qcp2":{"containers":{"aptams-fom-qcp2":{"image":"docker-production-aptams/aptams/fom:9.27.22","resources":{"limits":{"ephemeral-storage":"75Gi","memory":"22Gi"},"requests":{"cpu":"5","ephemeral-storage":"75Gi","memory":"22Gi"}}}},"init_containers":{"certificate-management":{"image":"docker-registry-redhat-io-remote/redhat-sso-7/sso71-openshift:1.1-16","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"200m","ephemeral-storage":"1Gi","memory":"1Gi"}}},"ldbtools-copy-sql-from-product-image":{"image":"docker-production-aptams/aptams/fom:9.27.22","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"100m","ephemeral-storage":"1Gi","memory":"1Gi"}}},"ldbtools-update-db":{"image":"docker-production-aptams/aptams/ldbtools:1.0.34","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"200m","ephemeral-storage":"1Gi","memory":"1Gi"}}}},"pods":{}},"aptams-lcx-qcp2":{"containers":{"aptams-lcx-qcp2":{"image":"docker-production-aptams/aptams/lcx:2.14.0","resources":{"limits":{"ephemeral-storage":"45Gi","memory":"3Gi"},"requests":{"cpu":"500m","ephemeral-storage":"45Gi","memory":"3Gi"}}}},"init_containers":{"certificate-management":{"image":"docker-registry-redhat-io-remote/redhat-sso-7/sso71-openshift:1.1-16","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"200m","ephemeral-storage":"1Gi","memory":"1Gi"}}},"ldbtools-copy-sql-from-product-image":{"image":"docker-production-aptams/aptams/lcx:2.14.0","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"100m","ephemeral-storage":"1Gi","memory":"1Gi"}}},"ldbtools-update-db":{"image":"docker-production-aptams/aptams/ldbtools:1.0.34","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"200m","ephemeral-storage":"1Gi","memory":"1Gi"}}}},"pods":{}},"aptams-mb-qcp2":{"containers":{"aptams-mb-qcp2":{"image":"docker-production-aptams/aptams/mb:7.0.11","resources":{"limits":{"ephemeral-storage":"45Gi","memory":"10Gi"},"requests":{"cpu":"3","ephemeral-storage":"45Gi","memory":"10Gi"}}}},"init_containers":{"certificate-management":{"image":"docker-registry-redhat-io-remote/redhat-sso-7/sso71-openshift:1.1-16","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"200m","ephemeral-storage":"1Gi","memory":"1Gi"}}}},"pods":{}},"aptams-mbl-qcp2":{"containers":{"aptams-mbl-qcp2":{"image":"docker-production-aptams/aptams/mbl:3.10.7","resources":{"limits":{"ephemeral-storage":"45Gi","memory":"3Gi"},"requests":{"cpu":"2","ephemeral-storage":"45Gi","memory":"3Gi"}}}},"init_containers":{"certificate-management":{"image":"docker-registry-redhat-io-remote/redhat-sso-7/sso71-openshift:1.1-16","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"200m","ephemeral-storage":"1Gi","memory":"1Gi"}}}},"pods":{}},"aptams-msc-qcp2":{"containers":{"aptams-msc-qcp2":{"image":"docker-production-aptams/aptams/messagestore:2.29.40","resources":{"limits":{"ephemeral-storage":"45Gi","memory":"5Gi"},"requests":{"cpu":"1","ephemeral-storage":"45Gi","memory":"5Gi"}}}},"init_containers":{"certificate-management":{"image":"docker-registry-redhat-io-remote/redhat-sso-7/sso71-openshift:1.1-16","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"200m","ephemeral-storage":"1Gi","memory":"1Gi"}}},"ldbtools-copy-sql-from-product-image":{"image":"docker-production-aptams/aptams/messagestore:2.29.40","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"100m","ephemeral-storage":"1Gi","memory":"1Gi"}}},"ldbtools-update-db":{"image":"docker-production-aptams/aptams/ldbtools:1.0.34","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"200m","ephemeral-storage":"1Gi","memory":"1Gi"}}}},"pods":{}},"aptams-prw-qcp2":{"containers":{"aptams-prw-qcp2":{"image":"docker-production-aptams/aptams/prw:10.2.0-14","resources":{"limits":{"ephemeral-storage":"45Gi","memory":"3Gi"},"requests":{"cpu":"1","ephemeral-storage":"45Gi","memory":"3Gi"}}}},"init_containers":{"certificate-management":{"image":"docker-registry-redhat-io-remote/redhat-sso-7/sso71-openshift:1.1-16","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"200m","ephemeral-storage":"1Gi","memory":"1Gi"}}},"ldbtools-copy-sql-from-product-image":{"image":"docker-production-aptams/aptams/prw:10.2.0-14","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"100m","ephemeral-storage":"1Gi","memory":"1Gi"}}},"ldbtools-update-db":{"image":"docker-production-aptams/aptams/ldbtools:1.0.34","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"200m","ephemeral-storage":"1Gi","memory":"1Gi"}}}},"pods":{}},"aptams-psa-qcp2":{"containers":{"aptams-psa-qcp2":{"image":"docker-production-aptams/aptams/apt-psa:2.13.3","resources":{"limits":{"ephemeral-storage":"45Gi","memory":"5Gi"},"requests":{"cpu":"3","ephemeral-storage":"45Gi","memory":"5Gi"}}}},"init_containers":{"certificate-management":{"image":"docker-registry-redhat-io-remote/redhat-sso-7/sso71-openshift:1.1-16","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"200m","ephemeral-storage":"1Gi","memory":"1Gi"}}},"ldbtools-copy-sql-from-product-image":{"image":"docker-production-aptams/aptams/apt-psa:2.13.3","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"100m","ephemeral-storage":"1Gi","memory":"1Gi"}}},"ldbtools-update-db":{"image":"docker-production-aptams/aptams/ldbtools:1.0.34","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"200m","ephemeral-storage":"1Gi","memory":"1Gi"}}}},"pods":{}},"aptams-sds-qcp2":{"containers":{"aptams-sds-qcp2":{"image":"docker-production-aptams/aptams/sds:10.11.18","resources":{"limits":{"ephemeral-storage":"45Gi","memory":"14Gi"},"requests":{"cpu":"3","ephemeral-storage":"45Gi","memory":"14Gi"}}}},"init_containers":{"certificate-management":{"image":"docker-registry-redhat-io-remote/redhat-sso-7/sso71-openshift:1.1-16","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"200m","ephemeral-storage":"1Gi","memory":"1Gi"}}},"ldbtools-copy-sql-from-product-image":{"image":"docker-production-aptams/aptams/sds:10.11.18","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"100m","ephemeral-storage":"1Gi","memory":"1Gi"}}},"ldbtools-update-db":{"image":"docker-production-aptams/aptams/ldbtools:1.0.34","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"200m","ephemeral-storage":"1Gi","memory":"1Gi"}}}},"pods":{}},"aptams-sga-qcp2":{"containers":{"aptams-sga-qcp2":{"image":"docker-production-aptams/aptams/frms:24.1.135","resources":{"limits":{"ephemeral-storage":"45Gi","memory":"14Gi"},"requests":{"cpu":"3","ephemeral-storage":"45Gi","memory":"14Gi"}}}},"init_containers":{"certificate-management":{"image":"docker-registry-redhat-io-remote/redhat-sso-7/sso71-openshift:1.1-16","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"200m","ephemeral-storage":"1Gi","memory":"1Gi"}}},"ldbtools-copy-sql-from-product-image":{"image":"docker-production-aptams/aptams/frms:24.1.135","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"100m","ephemeral-storage":"1Gi","memory":"1Gi"}}},"ldbtools-update-db":{"image":"docker-production-aptams/aptams/ldbtools:1.0.34","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"200m","ephemeral-storage":"1Gi","memory":"1Gi"}}}},"pods":{}},"aptams-slb-dmz":{"containers":{"aptams-slb-dmz":{"image":"docker-production-aptams/aptams/haproxy:3.0.4","resources":{"limits":{"ephemeral-storage":"10Gi","memory":"2Gi"},"requests":{"cpu":"3","ephemeral-storage":"10Gi","memory":"2Gi"}}}},"init_containers":{"certificate-management":{"image":"docker-registry-redhat-io-remote/redhat-sso-7/sso71-openshift:1.1-16","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"3","ephemeral-storage":"1Gi","memory":"1Gi"}}}},"pods":{}},"aptams-slb-qcp2":{"containers":{"aptams-slb-qcp2":{"image":"docker-production-aptams/aptams/haproxy:3.0.4","resources":{"limits":{"ephemeral-storage":"10Gi","memory":"2Gi"},"requests":{"cpu":"3","ephemeral-storage":"10Gi","memory":"2Gi"}}}},"init_containers":{"certificate-management":{"image":"docker-registry-redhat-io-remote/redhat-sso-7/sso71-openshift:1.1-16","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"3","ephemeral-storage":"1Gi","memory":"1Gi"}}}},"pods":{}},"aptams-splunk-qcp2":{"containers":{"aptams-splunk-qcp2":{"image":"docker-production-aptams/aptams/splunk-operator:1.0.2","resources":{"limits":{"ephemeral-storage":"5Gi","memory":"1Gi"},"requests":{"cpu":"50m","ephemeral-storage":"5Gi","memory":"1Gi"}}}},"init_containers":{},"pods":{}},"aptams-tam-qcp2":{"containers":{"aptams-tam-qcp2":{"image":"docker-production-aptams/aptams/tam:10.8.7","resources":{"limits":{"ephemeral-storage":"45Gi","memory":"5Gi"},"requests":{"cpu":"500m","ephemeral-storage":"45Gi","memory":"5Gi"}}}},"init_containers":{"certificate-management":{"image":"docker-registry-redhat-io-remote/redhat-sso-7/sso71-openshift:1.1-16","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"200m","ephemeral-storage":"1Gi","memory":"1Gi"}}},"ldbtools-copy-sql-from-product-image":{"image":"docker-production-aptams/aptams/tam:10.8.7","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"100m","ephemeral-storage":"1Gi","memory":"1Gi"}}},"ldbtools-update-db":{"image":"docker-production-aptams/aptams/ldbtools:1.0.34","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"200m","ephemeral-storage":"1Gi","memory":"1Gi"}}}},"pods":{}},"aptams-tools-qcp2":{"containers":{"aptams-tools-qcp2":{"image":"docker-production-aptams/aptams/versions-api:1.0.14","resources":{"limits":{"ephemeral-storage":"45Gi","memory":"3Gi"},"requests":{"cpu":"800m","ephemeral-storage":"45Gi","memory":"3Gi"}}}},"init_containers":{},"pods":{}},"aptams-vip-qcp2":{"containers":{"aptams-vip-qcp2":{"image":"docker-production-aptams/aptams/vip:6.4.72","resources":{"limits":{"ephemeral-storage":"45Gi","memory":"8Gi"},"requests":{"cpu":"1","ephemeral-storage":"45Gi","memory":"8Gi"}}}},"init_containers":{"certificate-management":{"image":"docker-registry-redhat-io-remote/redhat-sso-7/sso71-openshift:1.1-16","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"200m","ephemeral-storage":"1Gi","memory":"1Gi"}}},"ldbtools-copy-sql-from-product-image":{"image":"docker-production-aptams/aptams/vip:6.4.72","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"100m","ephemeral-storage":"1Gi","memory":"1Gi"}}},"ldbtools-update-db":{"image":"docker-production-aptams/aptams/ldbtools:1.0.34","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"200m","ephemeral-storage":"1Gi","memory":"1Gi"}}}},"pods":{}}},"statefulsets":{"aptams-esb-qcp2-zookeeper-ss":{"containers":{"kubernetes-zookeeper":{"image":"docker-production-aptams/aptams/kubernetes-zookeeper:20250207.0416","resources":{"limits":{"ephemeral-storage":"10Gi","memory":"10Gi"},"requests":{"cpu":"1","ephemeral-storage":"10Gi","memory":"10Gi"}}}},"init_containers":{},"pods":{}},"splunk-aptams-splunk-qcp2-standalone":{"containers":{"splunk":{"image":"docker-production-aptams/aptams/splunk:splunk-8.1.14-sdk-1.6.3-app-250110.1210","resources":{"limits":{"cpu":"6","ephemeral-storage":"10Gi","memory":"15Gi"},"requests":{"cpu":"2","ephemeral-storage":"10Gi","memory":"15Gi"}}}},"init_containers":{},"pods":{}}}}'

    esb_payload = '{"deployments":{"aptams-esb-qcp2":{"containers":{"aptams-esb-qcp2":{"image":"docker-production-aptams/aptams/esb:202504041825","resources":{"limits":{"ephemeral-storage":"45Gi","memory":"12Gi"},"requests":{"cpu":"2","ephemeral-storage":"45Gi","memory":"12Gi"}}}},"init_containers":{"certificate-management":{"image":"docker-registry-redhat-io-remote/redhat-sso-7/sso71-openshift:1.1-16","resources":{"limits":{"ephemeral-storage":"1Gi","memory":"1Gi"},"requests":{"cpu":"200m","ephemeral-storage":"1Gi","memory":"1Gi"}}}},"pods":{"aptams-esb-qcp2-5f86fcdd8c-nq9m6":{"databases":[],"deployments":["esb4-agent-1.1.23.war"],"interfaces":["altea-core-repo-1.1.16.zip","ams-common-repo-1.1.70.zip","ams-core-repo-1.1.55.zip","den-repo-1.1.5.zip","esb-bre-repo-1.1.19.zip","esb4-repository-1.1.23.zip","finavia-repo-1.1.12.5.zip","gyd-repo-1.1.5.zip"],"jboss":"jboss-eap-7:7.4.20-rev-5.0.15","jdk":"1.8.0_432"}}}}}'


if __name__ == "__main__":
    unittest.main()
