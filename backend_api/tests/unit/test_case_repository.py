# test_case_repository.py
# Unit tests for CaseRepository class


from backend_api.repository import CaseRepository

# Test 1 - create() creates case and sets ID
def test_create_case_assigns_id_and_stores_case():
    repo = CaseRepository()

    case = repo.create(
        title="Test",
        description = "Desc",
        status = "open"
    )

    assert case.id == 1
    assert case.title == "Test"
    assert case.description == "Desc"
    assert case.status == "open"

    # What this test proves:
    # Repository works in isolation
    # ID logic works
    # Object is created correctly

# Test 2 - multiple create()'s give incremental ID's
def test_create_multiple_cases_increment_id():
    repo = CaseRepository()

    case1 = repo.create("A", "A-desc", "open")
    case2 = repo.create("B", "B-desc", "closed")

    assert case1.id == 1
    assert case2.id == 2

    # What this test proves:
    # ID incrementation logic works
    # Multiple objects can be created

# Test 3 - get_all() returns empty list initially
def test_get_all_returns_empty_list_initially():
    repo = CaseRepository()

    cases = repo.get_all()

    assert cases == []

    # What this test proves:
    # Initial state is empty
    # get_all() works

# Test 4 - get_by_id() finds the correct case
def test_get_by_id_returns_correct_case():
    repo = CaseRepository()
    created = repo.create("Test", "Desc", "open")

    found = repo.get_by_id(created.id)

    assert found is created

    # What this test proves:
    # Repository should return `None` if not found,
    # not throw an HTTPException
    # get_by_id() works
    # ID mapping works

# Test 5 - get_by_id() on unknown ID
def test_get_by_id_returns_none_for_unknown_id():
    repo = CaseRepository()

    result = repo.get_by_id(999)

    assert result is None

    # What this test proves:
    # HTTP logic belongs in API layer, not repository
    # get_by_id() returns `None`if not found

# Test 6 - update() modifies existing case
def test_update_case_mutates_existing_case():
    repo = CaseRepository()
    case = repo.create("Old title", "Old desc", "open")

    updated = repo.update(
        case_id=case.id,
        title="New",
        description="New desc",
        status="closed"
    )

    assert updated.title == "New"
    assert updated.description == "New desc"
    assert updated.status == "closed"

    # What this test proves:
    # Object mutation works
    # update() works

# Test 7 - update() on unknown ID
def test_update_case_returns_none_for_unknown_id():
    repo = CaseRepository()

    result = repo.update(
        case_id=123,
        title="X",
        description="Y",
        status="open"
    )

    assert result is None

    # What this test proves:
    # update() returns `None` if not found
    # API decides on 404 handling

# Test 8 - delete() removes existing case
def test_delete_removes_case():
    repo = CaseRepository()
    case = repo.create("Test", "Desc", "open")

    deleted = repo.delete(case.id)

    assert deleted is True
    assert repo.get_by_id(case.id) is None

    # What this test proves:
    # delete() works
    # Case is actually removed
    