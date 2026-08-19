# Campus Connect — Defect Tracking & Bug Log

This document records **genuine defects** discovered in the Campus Connect application during automated test execution.

---

## Defect Log

### BUG-001: Profile Data Not Rendered Due to Unhandled API Response Envelope

- **Bug ID**: `BUG-001`
- **Title**: User profile attributes (name, email, college, bio, branch, year) fail to render on Profile page due to nested `res.data.user` response object.
- **Severity**: `High`
- **Component**: Frontend (`frontend/src/pages/Profile.jsx`) & Backend Integration (`/api/user/profile`, `/api/user/update`)
- **Environment**: Local & CI (All Browsers)
- **Status**: `Fixed` (Verified via automated regression test `ui_tests/test_update_profile.py`)

#### Description
When navigating to the Profile page (`#/profile`), the page loads empty strings for user Name and Email, and fallback values ("Unknown", "Not set", "N/A") for College, Branch, Year, and Bio. When saving profile updates, the update payload erroneously sends the entire root response object instead of user fields.

#### Root Cause
1. In `backend/controllers/userController.js`, `GET /api/user/profile` returns `{ success: true, user: { ... } }`.
2. In `frontend/src/pages/Profile.jsx`, `fetchProfile()` assigned `setProfile(res.data)` directly instead of unwrapping `res.data.user || res.data`.
3. Consequently, `profile.name`, `profile.email`, `profile.college`, etc. evaluated to `undefined` in React render.

#### Reproduction Steps
1. Register a new user with name "Alex", email "alex@campus.edu", and college "MIT".
2. Log into the application.
3. Click "Profile" in the navigation bar (`#/profile`).
4. **Expected Result**: User's name "Alex", email "alex@campus.edu", and college "MIT" are displayed.
5. **Actual Result**: Name and email are blank; college displays "Unknown"; bio displays placeholder fallback.

#### Resolution
Updated `frontend/src/pages/Profile.jsx`:
- Extracted `const profileData = res.data?.user || res.data;` in `fetchProfile()`.
- Explicitly passed `{ bio: form.bio, branch: form.branch, year: form.year }` in profile update submission.

---

### BUG-002: Cross-Platform Linux File Casing Inconsistency in Backend Controller Import

- **Bug ID**: `BUG-002`
- **Title**: Backend fails to start on Linux CI environments due to case mismatch between `userRoutes.js` and `usercontroller.js`.
- **Severity**: `High`
- **Component**: Backend (`backend/routes/userRoutes.js`, `backend/controllers/usercontroller.js`)
- **Environment**: Linux (Ubuntu CI / GitHub Actions)
- **Status**: `Fixed`

#### Description
`backend/routes/userRoutes.js` imports `require("../controllers/userController")` with PascalCase `userController`, while the file on disk was named `usercontroller.js`. On Windows (case-insensitive file system), this worked, but in Linux environments like GitHub Actions (`ubuntu-latest`), Node.js throws `Cannot find module '../controllers/userController'` and crashes the server.

#### Resolution
Renamed `backend/controllers/usercontroller.js` to `backend/controllers/userController.js` to match the exact casing required by `userRoutes.js`.
