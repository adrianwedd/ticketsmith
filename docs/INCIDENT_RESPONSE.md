# PII Incident Response Procedures

This document outlines the steps to follow when Personally Identifiable Information (PII) is detected in logs or anywhere in the system.

1. **Detection** – Automated scanning with the PII detection pipeline raises an alert if sensitive data is found.
2. **Containment** – Immediately restrict access to affected logs or data stores and rotate any exposed credentials.
3. **Notification** – Notify the Security Lead and legal/compliance teams. If required, inform impacted users and regulatory bodies.
4. **Eradication** – Remove the PII from all locations. Verify that log processors are redacting future occurrences.
5. **Postmortem** – Document the incident, root cause, and remediation steps in Confluence.

Following this playbook satisfies the escalation plan described in task SEC-PII-001.
