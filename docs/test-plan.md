# Campus Connect QA Test Plan

## 1. Objective
The objective of this QA Automation test plan is to establish a rigorous, repeatable, and scalable quality assurance framework for the **Campus Connect** full-stack web application. The suite automates functional verification of the Express REST API and end-to-end user workflows in the React frontend using **PyTest** and **Selenium WebDriver**, integrated with **GitHub Actions CI**.

---

## 2. Scope

The testing scope encompasses:
- **REST API Endpoints**: Authentication (`/api/auth`), Profile Management (`/api/user`), and Posts & Social interactions (`/api/posts`).
- **Frontend UI & E2E Workflows**: Registration, Login authentication, Session handling & Logout, Post Creation, Post Feed rendering, Profile editing, and Route authentication guards.
- **Continuous Integration**: GitHub Actions workflow executing automated tests on every push and pull request.
- **Cross-Platform Compatibility**: Linux (CI) and Windows local execution environments.
- **Regression Testing**: Automated suite verification to prevent defect recurrence.

---

## 3. Testing Tools & Technologies

| Tool / Technology | Purpose |
|---|---|
| **Python 3.11+** | Test automation scripting language |
| **PyTest** | Test framework, fixture lifecycle management, assertions |
| **Requests** | HTTP client for REST API validation |
| **Selenium WebDriver** | Browser automation for End-to-End UI testing |
| **Google Chrome (Headless & Visual)** | Target browser for UI execution |
| **Node.js & Express** | Application backend runtime |
| **React 19 & Vite** | Application frontend client |
| **MongoDB / MongoMemoryServer** | Database tier for data persistence and isolated test execution |
| **GitHub Actions** | Automated CI/CD test runner |

---

## 4. Test Strategy

1. **Positive Testing**: Validates standard successful user journeys, valid HTTP 200/201 responses, correct JSON schemas, and accurate UI state transitions.
2. **Negative Testing**: Validates application resilience against invalid inputs, duplicate registrations, bad credentials, missing required fields, non-existent endpoints, and unauthorized access attempts.
3. **Edge-Case & Boundary Testing**: Evaluates behavior under large payloads, multi-line unicode/emojis, special characters, and empty bodies.
4. **Security & Authentication Testing**: Validates JWT token creation, token expiration, unauthorized access rejection (HTTP 401), and frontend auth route guards.
5. **UI & E2E Testing**: Utilizes explicit synchronization waits (`WebDriverWait`, `expected_conditions`) to test critical user flows headlessly without fragile arbitrary sleeps.
6. **Data Isolation**: Unique identifiers and fixtures are dynamically generated for each test run to ensure deterministic, isolated executions.

---

## 5. Automated Test Cases & Execution Matrix

| Test ID | Module | Test Function | Test Type | Expected Result | Actual Result |
|---|---|---|---|---|---|
| `TC-API-01` | Auth | `test_register_valid_user` | Positive | Status 201, `success: true`, confirmation message | **PASS** |
| `TC-API-02` | Auth | `test_login_valid_credentials` | Positive | Status 200, valid JWT token, correct user metadata | **PASS** |
| `TC-API-03` | Auth | `test_register_duplicate_email` | Negative | Status 400, `success: false`, "User already exists" | **PASS** |
| `TC-API-04` | Auth | `test_login_invalid_password` | Negative | Status 400, `success: false`, "Invalid Password" | **PASS** |
| `TC-API-05` | Auth | `test_login_nonexistent_user` | Negative | Status 400, `success: false`, "User not found" | **PASS** |
| `TC-API-06` | Auth | `test_register_missing_required_fields` | Negative | Status >= 400, `success: false` | **PASS** |
| `TC-API-07` | Auth | `test_register_with_special_characters_and_unicode` | Edge Case | Status 201, `success: true` with unicode/emojis | **PASS** |
| `TC-API-08` | Auth | `test_register_large_string_payload` | Edge Case | Status 201, handles large string inputs safely | **PASS** |
| `TC-API-09` | Misc | `test_backend_root_health` | Positive | Status 200, "CampusConnect Backend Running" | **PASS** |
| `TC-API-10` | Misc | `test_auth_test_endpoint` | Positive | Status 200, "Auth Route Working" | **PASS** |
| `TC-API-11` | Misc | `test_nonexistent_endpoint_returns_404` | Negative | Status 404 for undefined routes | **PASS** |
| `TC-API-12` | Misc | `test_invalid_http_method_on_login` | Negative | Status 404 / 405 on invalid HTTP method | **PASS** |
| `TC-API-13` | Misc | `test_malformed_json_body` | Negative | Status 400 / 500 on malformed JSON | **PASS** |
| `TC-API-14` | Posts | `test_create_post_success` | Positive | Status 201, returns created post object with ID | **PASS** |
| `TC-API-15` | Posts | `test_get_posts_public` | Positive | Status 200, returns array containing public posts | **PASS** |
| `TC-API-16` | Posts | `test_create_post_unauthorized` | Negative | Status 401, "No token provided" | **PASS** |
| `TC-API-17` | Posts | `test_create_post_missing_fields` | Negative | Status >= 400, rejected on missing fields | **PASS** |
| `TC-API-18` | Posts | `test_like_post_endpoint` | Positive | Status 200, "Like route working" | **PASS** |
| `TC-API-19` | Posts | `test_like_post_unauthorized` | Negative | Status 401 without Bearer token | **PASS** |
| `TC-API-20` | Posts | `test_comment_post_endpoint` | Positive | Status 200, "Comment route working" | **PASS** |
| `TC-API-21` | Posts | `test_delete_post_endpoint` | Positive | Status 200, "Delete route working" | **PASS** |
| `TC-API-22` | Posts | `test_create_post_large_payload_and_unicode` | Edge Case | Status 201, long markdown & emojis preserved | **PASS** |
| `TC-API-23` | Users | `test_get_profile_valid_token` | Positive | Status 200, profile returned, password excluded | **PASS** |
| `TC-API-24` | Users | `test_get_profile_missing_token` | Negative | Status 401, "No token provided" | **PASS** |
| `TC-API-25` | Users | `test_get_profile_invalid_token` | Negative | Status 401, "Invalid token" | **PASS** |
| `TC-API-26` | Users | `test_update_profile_valid_data` | Positive | Status 200, updated bio/branch/year saved | **PASS** |
| `TC-API-27` | Users | `test_update_profile_unauthorized` | Negative | Status 401 on unauthorized profile update | **PASS** |
| `TC-API-28` | Users | `test_update_profile_special_characters_and_emojis` | Edge Case | Status 200, multiline & special chars saved | **PASS** |
| `TC-API-29` | Users | `test_update_profile_empty_payload` | Edge Case | Status 200, empty update payload handled | **PASS** |
| `TC-UI-01` | UI-Post | `test_create_and_view_post_flow` | E2E Flow | Post created via UI form appears in Feed list | **PASS** |
| `TC-UI-02` | UI-Post | `test_like_post_interactive_flow` | UI Interactive | Like button increments reaction count | **PASS** |
| `TC-UI-03` | UI-Auth | `test_signup_and_login_e2e_flow` | E2E Flow | Registration redirects to Login; Login opens Feed | **PASS** |
| `TC-UI-04` | UI-Auth | `test_invalid_login_shows_error_message` | UI Negative | Error banner rendered on invalid login | **PASS** |
| `TC-UI-05` | UI-Auth | `test_logout_flow` | E2E Flow | Logout clears session token and redirects to login | **PASS** |
| `TC-UI-06` | UI-Profile | `test_update_profile_flow` | E2E Flow | Profile edit form updates and reflects new bio | **PASS** |
| `TC-UI-07` | UI-Auth | `test_protected_route_unauthenticated_redirect` | Security UI | Direct unauthenticated access redirects to login | **PASS** |

---

## 6. Defects Found & Resolved

| Defect ID | Description | Severity | Status | Verification |
|---|---|---|---|---|
| `BUG-001` | Profile page attributes rendered blank due to unhandled `res.data.user` API wrapper in `frontend/src/pages/Profile.jsx`. | High | **Fixed** | Verified by `TC-UI-06` |
| `BUG-002` | Controller import casing mismatch (`usercontroller.js` vs `userController.js`) caused module crash on Linux CI. | High | **Fixed** | Verified across all test runs |

*Detailed defect reproduction steps and root causes are documented in [docs/defects.md](file:///c:/Users/shail/Downloads/campus%20connect%20qa%20automation/docs/defects.md).*

---

## 7. Continuous Integration (CI/CD)

Automated testing is configured in [.github/workflows/tests.yml](file:///c:/Users/shail/Downloads/campus%20connect%20qa%20automation/.github/workflows/tests.yml):
- **Triggers**: On every `push` and `pull_request` to `main` and `master`.
- **Services**: MongoDB 6.0 service container.
- **Build & Run**:
  1. Installs Node.js dependencies for backend and frontend.
  2. Sets up Python 3.11 and installs `requirements.txt`.
  3. Starts backend and frontend servers in the background with health readiness check.
  4. Runs PyTest REST API suite (`pytest api_tests -v -m api`).
  5. Runs Selenium UI suite (`pytest ui_tests -v -m ui`) using headless Chrome.
  6. Automatically captures and uploads screenshot artifacts on any failure.

---

## 8. Execution Summary

- **Total Test Cases**: **36**
- **Total API Tests**: **29** (Passed: **29**, Failed: **0**, Skipped: **0**)
- **Total UI Tests**: **7** (Passed: **7**, Failed: **0**, Skipped: **0**)
- **Overall Pass Rate**: **100%**
- **Defects Discovered**: **2**
- **Defects Fixed & Verified**: **2**
- **Total Execution Time**: ~40 seconds
