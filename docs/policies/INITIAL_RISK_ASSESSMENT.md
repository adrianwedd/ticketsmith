# Initial Risk Assessment

As part of establishing the ISMS, TicketSmith performed a high-level risk assessment.
The table below lists key threats and the planned treatment actions.

| ID | Threat | Likelihood | Impact | Treatment Plan |
|----|--------|-----------|--------|---------------|
| RA1 | Loss of customer support data | Medium | High | Daily backups and restricted database access |
| RA2 | Unauthorized code changes | Low | Medium | Require pull request reviews and enable branch protection |
| RA3 | Credential leakage | Medium | High | Store secrets in a vault and rotate API keys quarterly |

Treatment activities are tracked in Jira and progress is reviewed during security meetings. The complete assessment is stored in Confluence under the ISMS space.
