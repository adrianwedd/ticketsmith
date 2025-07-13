# Access Control Policy

Access to TicketSmith systems is granted based on job role and the principle of least privilege.

- User accounts must be unique and authenticated via SSO.
- Privileged access requires MFA.
- Access reviews are performed quarterly and documented in Confluence.

## Roles and Permissions

- **User** – Read access to personal tickets and the knowledge base.
- **Support** – Modify tickets and view operational metrics.
- **Administrator** – Manage user accounts, system settings, and audit logs.
- **Service** – Programmatic access scoped to required APIs only.

The application enforces these roles through RBAC. All staff must complete RBAC
training, and completion records are tracked in `SECURITY_TRAINING_LOG.md`.

