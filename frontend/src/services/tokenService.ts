// src/services/tokenService.ts

const TOKEN_KEY = 'token';

// Toggle this flag to control whether you use localStorage or rely on httpOnly cookies.
// In production with httpOnly cookies, set this to false.
const USE_LOCAL_STORAGE = import.meta.env.VITE_AUTH_MODE !== 'cookie';

/**
 * Save the JWT token (only in localStorage mode).
 * In httpOnly mode, the token is stored via a Set-Cookie header from the backend.
 */
export function setToken(token: string): void {
  if (USE_LOCAL_STORAGE) {
    localStorage.setItem(TOKEN_KEY, token);
  } else {
    console.warn('TokenService: Cannot set token manually in cookie mode.');
  }
}

/**
 * Retrieve the JWT token from localStorage.
 * In httpOnly mode, this will return null (since cookies aren't accessible from JS).
 */
export function getToken(): string | null {
  if (USE_LOCAL_STORAGE) {
    return localStorage.getItem(TOKEN_KEY);
  } else {
    return null; // Token will be sent automatically via cookies
  }
}

/**
 * Remove the JWT token from localStorage.
 * In httpOnly mode, the backend must clear the cookie with Set-Cookie.
 */
export function removeToken(): void {
  if (USE_LOCAL_STORAGE) {
    localStorage.removeItem(TOKEN_KEY);
  } else {
    console.warn('TokenService: Cannot remove token manually in cookie mode.');
  }
}

/**
 * Check if the user is authenticated (i.e., token exists).
 * In cookie mode, this just returns true since the token isn't accessible.
 */
export function isAuthenticated(): boolean {
  if (USE_LOCAL_STORAGE) {
    return !!localStorage.getItem(TOKEN_KEY);
  } else {
    // For cookie-based auth, consider pinging a `/me` endpoint to confirm
    return true;
  }
}