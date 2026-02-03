# test_case_service.py

from unittest.mock import Mock

from backend_api.services.case_service import CaseService
from backend_api.models import Case

# Test 1 – create_case calls repo correctly
def test_create_case_calls_repo_and_returns_case():
    # Arrange
    mock_repo = Mock()
    expected_case = Case(
        id=1,
        title="Test",
        description="Desc",
        status="open"
    )
    mock_repo.create.return_value = expected_case

    service = CaseService(mock_repo)

    # Act
    result = service.create_case("Test", "Desc", "open")

    # Assert
    mock_repo.create.assert_called_once_with(
        "Test", "Desc", "open"
    )
    assert result is expected_case

    # What this test does:
    # Service:
    # - calls repo.create
    # - sends the correct arguments
    # - returns the exact repo result
    # This ensures the service layer correctly delegates case
    # creation to the repository layer.
    # Repo implementation is irrelevant

# Test 2 – get_case forwards correctly
def test_get_case_calls_repo_with_id():
    mock_repo = Mock()
    case = Case(1, "A", "B", "open")
    mock_repo.get_by_id.return_value = case

    service = CaseService(mock_repo)

    result = service.get_case(1)

    mock_repo.get_by_id.assert_called_once_with(1)
    assert result is case

    # This test ensures that the service's get_case method
    # correctly calls the repository's get_by_id method
    # with the provided case_id and returns the expected Case
    # object.

# Test 3 – get_case returns None if repo does
def test_get_case_returns_none_when_not_found():
    mock_repo = Mock()
    mock_repo.get_by_id.return_value = None

    service = CaseService(mock_repo)

    result = service.get_case(999)

    assert result is None

    # Important:
    # Service does not decide on 404 – the API layer does.
    # This test verifies that when the repository returns None
    # for a non-existent case_id, the service also returns None,
    # allowing the API layer to handle the "not found" scenario.

# Test 4 - update_case
def test_update_case_calls_repo_correctly():
    mock_repo = Mock()

    existing_case = Case(1, "Old", "old", "open")
    updated_case = Case(1, "New", "New", "closed")

    mock_repo.get_by_id.return_value = existing_case
    mock_repo.update.return_value = updated_case

    service = CaseService(mock_repo)

    result = service.update_case(1, "New", "New", "open")

    mock_repo.update.assert_called_once()

    assert result == updated_case

    # This test verifies that the service's update_case method
    # correctly calls the repository's update method with
    # the provided parameters and returns the updated Case
    # object.

# Test 5 - delete_case
def test_delete_case_calls_repo_and_returns_bool():
    mock_repo = Mock()
    mock_repo.delete.return_value = True

    service = CaseService(mock_repo)

    result = service.delete_case(1)

    mock_repo.delete.assert_called_once_with(1)
    assert result is True

    # This test ensures that the service's delete_case method
    # correctly calls the repository's delete method with
    # the provided case_id and returns the boolean result
    # indicating success or failure of the deletion.