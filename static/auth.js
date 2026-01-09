
// Black Pearl Authentication System v2.1
// WARNING: This file contains security-critical logic
// DO NOT expose in production!

// ⚠️ VULNERABILITY: Credentials hardcoded in client-side JavaScript
const VALID_CREDENTIALS = {
    'jack_sparrow': 'rumrunner',
    'will_turner': 'elizabeth',
    'joshamee': 'cotton_parrot',
    'deckhand_tom': 'anchor123'
};

// ⚠️ VULNERABILITY: Roles determined client-side
const USER_ROLES = {
    'jack_sparrow': 'captain',
    'will_turner': 'officer',
    'joshamee': 'quartermaster',
    'deckhand_tom': 'sailor'
};

// ⚠️ VULNERABILITY: User IDs exposed
const USER_IDS = {
    'jack_sparrow': 1,
    'will_turner': 2,
    'joshamee': 3,
    'deckhand_tom': 4
};

// Check if user is authenticated (client-side only!)
function isAuthenticated() {
    return localStorage.getItem('authenticated') === 'true';
}

// Check user role (client-side only!)
function getUserRole() {
    return localStorage.getItem('role') || 'sailor';
}

// Get username
function getUsername() {
    return localStorage.getItem('username') || 'unknown';
}

// Admin check (client-side only!)
function isAdmin() {
    const role = getUserRole();
    return role === 'captain' || role === 'officer';
}

// Logout function
function logout() {
    localStorage.clear();
    window.location.href = '/';
}

console.log('[Auth System] Client-side authentication active');
console.log('[WARNING] All security l1ogic runs in the browser!');
console.log('[HINT] Valid users:', Object.keys(VALID_CREDENTIAL));
console.log('[HINT] Roles:', USER_ROLES);
console.log('[HINT] Try changing localStorage values manually!');
