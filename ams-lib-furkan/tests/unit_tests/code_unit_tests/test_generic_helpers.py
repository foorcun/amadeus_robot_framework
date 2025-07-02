import pytest
from unittest.mock import MagicMock, patch

from ams.data_model.common_libs.utils.generic_helpers import (
    initialize_variables,
    construct_default_params,
    construct_attributes,
    initialize_test_context,
)


class TestGenericHelpers:
    def setup_method(self):
        self.mock_self = MagicMock()
        self.mock_self.request_data = {"key1": "value1", "params": None}
        self.mock_self.context_data = {
            "test_context": {"context_key": {"params": "context_params_value"}}
        }
        self.mock_self.context_data_key = "context_key"

    def test_initialize_variables(self):
        """Test the initialize_variables function."""
        initialize_variables(self.mock_self)
        assert self.mock_self.key1 == "value1"
        assert self.mock_self.params is None

    def test_construct_default_params(self):
        default_params = "param1,param2"
        test_context_keys = ["key1", "key2"]
        test_context = {"key1": {"param1": "value1"}, "key2": {"param2": "value2"}}
        result = construct_default_params(
            default_params, test_context_keys, test_context
        )
        assert result == {"param1": "value1", "param2": "value2"}

    def test_construct_attributes(self):
        attributes = "attr1,attr2"
        result = construct_attributes(attributes)
        # Only the last attribute will be set
        assert result == {"attribute": "attr2"}

    @patch("ams.data_model.common_libs.utils.generic_helpers.os.path.exists")
    @patch("ams.data_model.common_libs.utils.generic_helpers.import_module")
    def test_initialize_test_context(self, mock_import_module, mock_path_exists):
        mock_path_exists.return_value = True
        mock_import_module.return_value = MagicMock(test_context="test_context_value")

        test_data_file_path = "/path/to/test_data.py"
        result = initialize_test_context(test_data_file_path)

        assert result.test_context == "test_context_value"
        mock_path_exists.assert_called_once_with(test_data_file_path)
        mock_import_module.assert_called_once()

    @patch("ams.data_model.common_libs.utils.generic_helpers.os.path.exists")
    def test_initialize_test_context_file_not_exist(self, mock_path_exists):
        mock_path_exists.return_value = False

        test_data_file_path = "/path/to/non_existent_test_data.py"
        with pytest.raises(
            Exception,
            match=f'Test Data context file "{test_data_file_path}" does not exist',
        ):
            initialize_test_context(test_data_file_path)
