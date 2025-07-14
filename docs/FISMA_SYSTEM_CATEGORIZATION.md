# FISMA System Categorization

The table below lists the primary information types handled by TicketSmith and their FIPS 199 impact levels for confidentiality, integrity, and availability (CIA).

| Information Type | Description | Confidentiality | Integrity | Availability |
|------------------|-------------|-----------------|-----------|--------------|
| Support Ticket Data | Customer support tickets and attachments stored in Jira | Moderate | Moderate | Moderate |
| Knowledge Base Content | Confluence articles and documentation served to users | Low | Moderate | Low |
| User Account Information | User profiles and authentication data required for access control | Moderate | Moderate | Moderate |
| Audit Logs | Security and operational logs used for investigations | Low | High | Moderate |
| Vendor Integration Data | Data exchanged with third-party services such as Atlassian APIs | Moderate | Moderate | Moderate |

The impact levels were determined based on the importance of each information type to business operations and compliance requirements.
