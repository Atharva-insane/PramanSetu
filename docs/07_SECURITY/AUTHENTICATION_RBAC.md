# 🔑 Authentication & Role-Based Access Control (RBAC)

- **Token Format**: HS256 JWT Bearer Token (`/api/auth/login`).
- **Password Hashing**: PBKDF2-HMAC-SHA256 with random salt ($100,000$ iterations).
- **Default Roles**: `SUPER_ADMIN`, `VIGILANCE_OFFICER`, `SOCIAL_AUDITOR`.
