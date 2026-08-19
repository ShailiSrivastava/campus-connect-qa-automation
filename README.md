# Campus Connect QA Automation Suite

A full-scale automated QA framework for the **Campus Connect** social platform. This suite provides automated **REST API validation using PyTest and Requests**, **End-to-End UI testing with Selenium WebDriver and Headless Chrome**, and continuous integration through **GitHub Actions**.

---

## 🛠️ Testing Stack

- **Test Framework**: [PyTest](https://docs.pytest.org/) (v8+)
- **API Automation**: [Requests](https://requests.readthedocs.io/) & [Python-Dotenv](https://pypi.org/project/python-dotenv/)
- **UI Automation**: [Selenium WebDriver](https://www.selenium.dev/) (Chrome / Headless Chrome)
- **CI / CD Pipeline**: [GitHub Actions](https://github.com/features/actions)
- **Application Stack**: Node.js, Express, React 19, Vite, MongoDB / MongoMemoryServer

---

## 📁 Project Structure

```
campus-connect-qa-automation/
│
├── api_tests/                          # PyTest REST API Automation Suite
│   ├── __init__.py
│   ├── conftest.py                     # API fixtures, auth tokens, session headers
│   ├── test_auth.py                    # Register & login positive/negative/edge tests
│   ├── test_users.py                   # Profile retrieval & update tests
│   ├── test_posts.py                   # Post CRUD, like, comment, delete tests
│   └── test_misc.py                    # Root health, 404 handling, invalid methods
│
├── ui_tests/                           # Selenium UI / E2E Automation Suite
│   ├── __init__.py
│   ├── conftest.py                     # WebDriver fixtures, Chrome options, screenshot hooks
│   ├── test_signup_login.py            # Signup E2E, Login, Invalid Login, Logout flow
│   ├── test_create_post.py             # Post creation and interactive reaction flows
│   └── test_update_profile.py          # Profile update flow and auth route guards
│
├── backend/                            # Node.js + Express API server
│   ├── config/                         # Database connection with MongoMemoryServer fallback
│   ├── controllers/                    # Auth, User, and Post controllers
│   ├── middleware/                     # JWT authentication protection middleware
│   ├── models/                         # Mongoose User and Post schemas
│   ├── routes/                         # Express API route declarations
│   ├── server.js                       # Server entry point
│   ├── package.json
│   └── .env.example
│
├── frontend/                           # React 19 + Vite client application
│   ├── src/                            # Components, pages, and Axios API service
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
│
├── docs/                               # QA Documentation
│   ├── test-plan.md                    # Comprehensive test plan and test case matrix
│   └── defects.md                      # Genuine defect reports and root-cause analysis
│
├── .github/
│   └── workflows/
│       └── tests.yml                   # CI automation workflow for GitHub Actions
│
├── requirements.txt                    # Python test dependencies
├── pytest.ini                          # PyTest discovery, output formatting, markers
├── .env.example                        # Environment variable configuration template
└── README.md                           # Documentation and usage guide
```

---

## 🔌 API Testing

The API test suite contains **29 test cases** providing complete coverage of all backend endpoints:

- **Authentication (`/api/auth`)**:
  - `POST /register`: Valid registration, duplicate email rejection (400), missing required fields, unicode/special characters, large payloads.
  - `POST /login`: Valid credentials authentication with JWT verification, wrong password rejection (400), unregistered user handling (400).
- **User Profile (`/api/user`)**:
  - `GET /profile`: Authenticated profile retrieval (200), missing token rejection (401), invalid token rejection (401).
  - `PUT /update`: Valid bio/branch/year update (200), unauthorized update rejection (401), multiline unicode text handling, empty payload handling.
- **Posts & Social (`/api/posts`)**:
  - `POST /create`: Authenticated post creation (201), unauthorized creation rejection (401), missing fields, large payloads.
  - `GET /`: Public post list retrieval with author population and descending date sorting.
  - `POST /like/:id`: Post reaction endpoint verification.
  - `POST /comment/:id`: Comment creation endpoint verification.
  - `DELETE /:id`: Post deletion endpoint verification.
- **Health & Security (`/`, `/api/auth/test`)**:
  - Root backend health status, auth test route, 404 response on undefined routes, invalid HTTP methods, malformed JSON body handling.

---

## 🖥️ UI / E2E Testing

The UI test suite contains **7 automated Selenium scenarios** executing against the live React client:

1. **Signup + Login E2E Flow**: Signs up a new unique student, validates automatic redirect to `#/login`, performs login, and verifies arrival at the Feed dashboard (`#/feed`).
2. **Invalid Login**: Enters wrong credentials and asserts that `.auth-message` error is displayed without navigating away.
3. **Logout Flow**: Logs in, clicks Logout in `.cc-navbar`, verifies redirect to `#/login`, and confirms removal of JWT from `localStorage`.
4. **Create Post Flow**: Fills post title and content in `CreatePost` form, submits, verifies confirmation status, and asserts the new post card is rendered in the feed.
5. **Interactive Like Reaction**: Clicks the Like button on a post card and verifies the like counter updates dynamically.
6. **Update Profile Flow**: Opens Profile (`#/profile`), toggles the edit form, updates Branch, Year, and Bio, saves changes, and asserts the updated information renders in the profile summary.
7. **Security Route Guards**: Directly navigates unauthenticated browsers to `#/feed` and `#/profile`, verifying immediate redirection to `#/login`.

---

## 🚀 Running Locally

### 1. Prerequisites
- Python 3.11+
- Node.js 18+ and npm
- Google Chrome browser installed

### 2. Setup Python Environment & Dependencies
```bash
# Optional: Create virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate
# Linux / macOS:
source venv/bin/activate

# Install QA automation dependencies
pip install -r requirements.txt
```

### 3. Start Campus Connect Services

#### Terminal 1 — Start Backend Server:
```bash
cd backend
npm install
npm start
```
*Backend starts on `http://localhost:5000` (automatically initializes in-memory MongoDB if remote Atlas is unreachable).*

#### Terminal 2 — Start Frontend Client:
```bash
cd frontend
npm install
npm run dev -- --port 5173
```
*Frontend starts on `http://localhost:5173`.*

---

### 4. Execute Test Suites

#### Run Complete Test Suite (API + UI):
```bash
python -m pytest -v
```

#### Run REST API Tests Only:
```bash
python -m pytest api_tests -v
```

#### Run Selenium UI Tests Only:
```bash
python -m pytest ui_tests -v
```

#### Run Smoke Tests Only:
```bash
python -m pytest -m smoke -v
```

#### Run UI Tests with Visible Browser (Non-Headless):
```bash
# Windows PowerShell:
$env:HEADLESS="false"; python -m pytest ui_tests -v

# Linux / macOS:
HEADLESS=false python -m pytest ui_tests -v
```

---

## ⚙️ Environment Variables

Copy `.env.example` to `.env` to configure custom endpoints:

| Variable | Description | Default Value |
|---|---|---|
| `API_BASE_URL` | Base URL for backend Express server | `http://localhost:5000` |
| `UI_BASE_URL` | Base URL for frontend React/Vite server | `http://localhost:5173` |
| `HEADLESS` | Whether to run Chrome headlessly (`true` / `false`) | `true` |
| `TEST_USER_NAME` | Default test user name | `Test Student` |
| `TEST_USER_EMAIL` | Default test user email | `teststudent@campus.edu` |
| `TEST_USER_PASSWORD` | Default test user password | `Password123!` |

---

## 🔄 CI / CD Pipeline

The GitHub Actions workflow at [.github/workflows/tests.yml](file:///c:/Users/shail/Downloads/campus%20connect%20qa%20automation/.github/workflows/tests.yml) automatically runs on every push and pull request to `main` and `master`:

1. Starts MongoDB 6.0 container.
2. Sets up Node.js 20 & Python 3.11 with caching.
3. Installs dependencies and launches Backend & Frontend in the background.
4. Waits for health endpoints to confirm services are online.
5. Executes the PyTest API test suite.
6. Executes the Selenium UI test suite using Headless Chrome.
7. Uploads failure screenshots automatically if any test fails.

---

## 🐞 Bug Tracking & Discovered Defects

During automated testing, **2 genuine defects** were identified, documented, and fixed:

- **BUG-001 (High)**: User profile attributes rendered blank on Profile page due to an unhandled `res.data.user` API wrapper in `frontend/src/pages/Profile.jsx`. *Fixed & verified via `TC-UI-06`.*
- **BUG-002 (High)**: File import casing mismatch in `backend/routes/userRoutes.js` (`usercontroller.js` vs `userController.js`) caused module crashes on Linux CI. *Fixed by standardizing file casing.*

*Full defect reports, reproduction steps, and root causes are available in [docs/defects.md](file:///c:/Users/shail/Downloads/campus%20connect%20qa%20automation/docs/defects.md).*

---

## 📊 Final Test Results

| Test Category | Total Tests | Passed | Failed | Skipped | Pass Rate | Execution Time |
|---|---|---|---|---|---|---|
| **REST API Suite** | 29 | 29 | 0 | 0 | 100% | ~2.5s |
| **Selenium UI Suite** | 7 | 7 | 0 | 0 | 100% | ~37.0s |
| **Complete Regression** | **36** | **36** | **0** | **0** | **100%** | **~40.0s** |
