# Data Encryption Policy

TicketSmith encrypts sensitive data in transit and at rest.

- TLS 1.2+ is required for all network communications.
- PostgreSQL (including the `pgvector` extension) runs on a cloud-managed
  service with storage encryption enabled. In AWS this means using RDS with a
  customer managed [KMS](https://aws.amazon.com/kms/) key.
- File and object storage such as S3 buckets use server-side encryption with the
  same KMS keys.
- Backups are encrypted at rest and stored in the provider's managed backup
  service.
- Encryption keys are kept in the secret manager and managed through KMS with
  annual rotation and IAM-restricted access.

