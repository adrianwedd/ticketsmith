# Compliance Framework Gap Analysis

This document summarizes the regulatory frameworks relevant to the TicketSmith project and highlights current gaps between required controls and the implemented features.

## Applicable Frameworks
- **HIPAA** – Health Insurance Portability and Accountability Act for handling protected health information.
- **ISO/IEC 27001** – International standard for information security management systems (ISMS).
- **FISMA** – Federal Information Security Modernization Act for U.S. government data.
- **SOC 2** – Service Organization Control 2 for SaaS vendors.
- **GDPR** – General Data Protection Regulation for personal data of EU residents.

## Gap Analysis

### HIPAA
**Current Controls**
- PII detection and redaction pipeline implemented (task SEC-PII-001).
- Incident response process documented in `INCIDENT_RESPONSE.md`.
- OAuth-based access control planned for tool APIs (task SEC-OAUTH-001).
- BAA template and workflow documented in [BAA Management Workflow](policies/BAA_WORKFLOW.md).
- Data encryption at rest documented in [Data Encryption Policy](policies/DATA_ENCRYPTION_POLICY.md).

**Gaps**
- Detailed audit logging not documented.
- Role-based access controls and training programs incomplete.

### ISO 27001
**Current Controls**
- Security policies and ISMS framework planned (task SEC-POLICY-001).
- Initial security model includes token-based authentication and PII handling.

**Gaps**
- Formal ISMS documentation and risk assessments not yet created.
- No regular internal audit process defined.
- Limited evidence of continuous improvement or management review.

### FISMA
**Current Controls**
- Basic access controls and PII safeguards exist.

**Gaps**
- Comprehensive implementation of NIST 800-53 controls missing.
- Continuous monitoring and authority to operate processes not defined.
- System categorization and impact analysis incomplete.

### SOC 2
**Current Controls**
- Logging, incident response, and OAuth scopes planned provide a baseline for security and availability.

**Gaps**
- Formal policies for change management, vendor management, and business continuity not documented.
- Independent SOC 2 audit has not been scheduled.

### GDPR
**Current Controls**
- PII detection reduces risk of storing personal data.
- Incident response outlines notification steps.

**Gaps**
- Data Processing Agreement (DPA) templates not provided.
- Processes for user data deletion and export requests not implemented.
- No record of processing activities or Data Protection Impact Assessments.

## Remediation Plan
A detailed remediation plan should be created in Jira to address the gaps above. Each gap should correspond to new tasks with owners and due dates. Policies and procedures should be published in Confluence once drafted.
