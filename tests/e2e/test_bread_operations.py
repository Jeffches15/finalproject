import pytest
import requests
from app.models.calculation import Calculation
from app.models.user import User
from faker import Faker
from playwright.sync_api import Page, expect
from sqlalchemy.orm import Session


######################
# Positive E2E tests
# Successful creation, retrieval, updating, and deletion of calculations.
######################
@pytest.mark.usefixtures("fastapi_server")
def test_create_calculation_success(page, fastapi_server, db_session):
    """UI test: successfully create a calculation via dashboard."""
    base_url = fastapi_server.rstrip('/')

    # --- Create test user ---
    plain_password = "plaintextpassword"
    hashed_pw = User.hash_password(plain_password)
    user = User(
        first_name="Test",
        last_name="User",
        email="test@example.com",
        username="testuser",
        password=hashed_pw,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Login
    page.goto(f"{base_url}/login")
    page.fill('input[name="username"]', user.username)
    page.fill('input[name="password"]', plain_password)
    page.click('button[type="submit"]')

    # Wait for dashboard redirect
    page.wait_for_url(f"{base_url}/dashboard", timeout=60000)

    # Perform calculation
    page.select_option('#calcType', 'addition')
    page.fill('#calcInputs', '5,10,15')
    page.click('button[type="submit"]')

    # Verify success alert text
    success_alert = page.locator('#successAlert')
    success_alert.wait_for(timeout=10000)
    alert_text = success_alert.inner_text().lower()
    assert "calculation complete" in alert_text or "success" in alert_text

    # Verify table contains calculation
    first_row = page.locator('#calculationsTable tr').first
    row_text = first_row.inner_text().lower()
    assert "addition" in row_text
    assert "30" in row_text

fake = Faker()

@pytest.mark.usefixtures("fastapi_server")
def test_retrieve_calculation(page, fastapi_server, db_session):
    """UI test: retrieve and display a calculation in the dashboard."""
    base_url = fastapi_server.rstrip('/')

    # Create unique test user
    plain_password = "plaintextpassword"
    hashed_pw = User.hash_password(plain_password)
    user = User(
        first_name="Test",
        last_name="User",
        email=fake.unique.email(),
        username=fake.unique.user_name(),
        password=hashed_pw,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Create calculation directly in DB
    calc = Calculation.create(
        calculation_type="addition",
        user_id=user.id,
        inputs=[5, 10, 15]
    )
    calc.result = calc.get_result()
    db_session.add(calc)
    db_session.commit()
    db_session.refresh(calc)

    # Login
    page.goto(f"{base_url}/login")
    page.fill('input[name="username"]', user.username)
    page.fill('input[name="password"]', plain_password)
    page.click('button[type="submit"]')

    # Wait for dashboard
    page.wait_for_url(f"{base_url}/dashboard", timeout=60000)

    # Verify calculation is visible
    first_row = page.locator('#calculationsTable tr').first
    assert "addition" in first_row.inner_text().lower()
    assert "30" in first_row.inner_text()


@pytest.mark.usefixtures("fastapi_server")
def test_update_calculation(page, fastapi_server, db_session):
    base_url = fastapi_server.rstrip('/')

    # Create user
    hashed_pw = User.hash_password("plaintextpassword")
    user = User(
        first_name="Test",
        last_name="User",
        email="testupdate@example.com",
        username="testupdateuser",
        password=hashed_pw,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Create calculation
    calc = Calculation(
        user_id=user.id,
        type="addition",
        inputs=[10, 20, 30],
        result=60
    )
    db_session.add(calc)
    db_session.commit()
    db_session.refresh(calc)
    calc_id = calc.id

    # Login
    page.goto(f"{base_url}/login")
    page.fill('input[name="username"]', user.username)
    page.fill('input[name="password"]', "plaintextpassword")
    page.click('button[type="submit"]')
    page.wait_for_url(f"{base_url}/dashboard", timeout=60000)

    # Go to edit page
    page.goto(f"{base_url}/dashboard/edit/{calc_id}")
    page.wait_for_selector('#loadingState', state='hidden', timeout=15000)
    page.wait_for_selector('#editCalculationForm', state='visible', timeout=15000)

    # Update inputs and submit
    page.fill('#calcInputs', '20, 30, 40')
    page.click('#editCalculationForm button[type="submit"]')

    # ✅ Wait for redirect to view page
    page.wait_for_url(f"{base_url}/dashboard/view/{calc_id}", timeout=15000)

    # ✅ Wait for loading spinner to disappear
    page.wait_for_selector("#loadingState", state="hidden", timeout=15000)

    # ✅ Wait for the calculation card to be visible
    page.wait_for_selector("#calculationCard", state="visible", timeout=15000)

    # ✅ Wait until details are updated
    page.wait_for_function(
        """() => {
            const details = document.querySelector('#calcDetails');
            return details && details.innerText.includes('20, 30, 40') && details.innerText.includes('90');
        }""",
        timeout=20000
    )

    # Final assertion
    details_text = page.locator("#calcDetails").inner_text()
    assert "20, 30, 40" in details_text
    assert "90" in details_text


@pytest.mark.usefixtures("fastapi_server")
def test_delete_calculation_from_dashboard(page, fastapi_server, db_session):
    base_url = fastapi_server.rstrip('/')

    # --- Create test user in DB ---
    plain_password = "MyS3cretPwd!"
    hashed_pw = User.hash_password(plain_password)
    user = User(
        first_name="Delete",
        last_name="Tester",
        email="delete.tester@example.com",
        username="delete_tester_001",
        password=hashed_pw,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # --- Log in via UI ---
    page.goto(f"{base_url}/login")
    page.fill('input[name="username"]', user.username)
    page.fill('input[name="password"]', plain_password)
    page.click('button[type="submit"]')

    # Wait for dashboard redirect
    page.wait_for_url(f"{base_url}/dashboard", timeout=60000)

    # --- Create a calculation ---
    page.select_option('#calcType', 'addition')
    page.fill('#calcInputs', '7,8')
    page.click('button[type="submit"]')

    # Wait for success alert confirming calculation creation
    page.wait_for_selector('#successAlert', timeout=10000)
    alert_text = page.locator('#successAlert').inner_text().lower()
    assert "calculation complete" in alert_text or "success" in alert_text

    # --- Confirm calculation row exists ---
    rows_before = page.locator('tbody#calculationsTable tr').count()
    assert rows_before > 0, "No calculation rows found after creation"

    # --- Delete the first calculation ---
    # Setup to accept confirm dialog automatically
    page.once("dialog", lambda dialog: dialog.accept())
    page.locator('.delete-calc').first.click()

    # Wait for deletion success alert
    page.wait_for_selector('#successAlert', timeout=10000)
    del_alert_text = page.locator('#successAlert').inner_text().lower()
    assert "deleted" in del_alert_text or "success" in del_alert_text

    # Wait a moment for UI to update
    page.wait_for_timeout(600)


######################
# Negative E2E tests
# Handling invalid inputs, unauthorized access, and error responses.
######################
@pytest.mark.e2e
def test_unauthorized_access(page: Page):
    # Try to visit dashboard without logging in
    page.goto("http://localhost:8000/dashboard")
    
    # It should redirect to login
    assert page.url.endswith("/login")


BASE_URL = "http://localhost:8000"

@pytest.mark.e2e
def test_delete_calculation_unauthorized_ui(page: Page):
    """
    Go to dashboard without token and try to delete.
    Expected: Redirect to login.
    """
    page.goto(f"{BASE_URL}/dashboard")
    page.evaluate("() => localStorage.clear()")

    # The app should immediately redirect
    expect(page).to_have_url(f"{BASE_URL}/login")


@pytest.fixture
def unique_test_user_with_password(db_session, fake_user_data):
    """
    Create a unique test user and return the user instance along with
    the plain password used to register so we can login.
    """
    plain_password = fake_user_data["password"]
    user = User.register(db_session, fake_user_data)
    db_session.commit()
    return user, plain_password


def test_create_calculation_invalid_input(fastapi_server, unique_test_user_with_password):
    user, plain_password = unique_test_user_with_password

    # Log in to get access token
    login_payload = {
        "username": user.username,
        "password": plain_password
    }
    login_response = requests.post(f"{fastapi_server}auth/login", json=login_payload)
    assert login_response.status_code == 200, f"Login failed: {login_response.text}"
    token = login_response.json()["access_token"]

    # Prepare invalid calculation payload (only one input)
    invalid_payload = {
        "type": "addition",
        "inputs": [1]  # invalid: less than 2 numbers
    }

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{fastapi_server}calculations", json=invalid_payload, headers=headers)

    assert response.status_code == 422, f"Expected 422 validation error but got {response.status_code}"
    
    errors = response.json().get("detail", [])
    assert any(
        "inputs" in err.get("loc", []) and
        ("too_short" in err.get("type", "") or "length" in err.get("msg", "").lower())
        for err in errors
    ), f"Expected validation error about inputs length not found: {errors}"
