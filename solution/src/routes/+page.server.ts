// src/routes/+page.server.js
import { redirect } from '@sveltejs/kit';

export function load() {
    // Perform server-side redirection
    throw redirect(307, '/1');
}
