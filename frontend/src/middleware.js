import { NextResponse } from 'next/server';

const WARP_TO_HOME_ENABLED = false;

export function middleware(request) {
  const { pathname } = request.nextUrl;

  // If warp mode is enabled AND the user is not already on the homepage
  if (WARP_TO_HOME_ENABLED && pathname !== '/') {
    // Get the original request's URL base (protocol, hostname, port)
    const url = request.nextUrl.clone();
    url.pathname = '/';
    // Perform a temporary redirect to the homepage
    return NextResponse.redirect(url, 307);
  }

  // Else if not in warp mode or already on the homepage, continue as normal
  return NextResponse.next();
}

// Config for which paths the middleware should run on
// Match all request paths except for the ones starting/ending with:
export const config = {
  matcher: [
    '/((?!api/|_next/static/|_next/image/|favicon.ico|.*\\.(?:png|jpg|jpeg|gif|svg|webp|ico|css|js)$).*)',
  ],
};