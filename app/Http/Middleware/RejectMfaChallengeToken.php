<?php

declare(strict_types=1);

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

final class RejectMfaChallengeToken
{
    public function handle(Request $request, Closure $next): Response
    {
        // The challenge endpoint is the only endpoint that accepts this token.
        if ($request->is('api/auth/mfa/challenge')) {
            return $next($request);
        }

        if (auth('api')->check()) {
            try {
                if (auth('api')->payload()->get('type') === 'mfa') {
                    return new JsonResponse(['message' => 'MFA verification is required.'], 403);
                }
            } catch (\Throwable) {
                // The authentication middleware remains responsible for invalid tokens.
            }
        }

        return $next($request);
    }
}
