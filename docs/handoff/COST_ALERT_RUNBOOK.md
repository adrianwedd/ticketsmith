# Cost Alert Runbook

This runbook outlines the steps to take when the cloud cost alert fires.

1. **Identify Source** – Review the alert details in the monitoring dashboard to determine which service triggered the cost spike.
2. **Stop the Bleeding** – If costs are rapidly increasing due to a runaway process, scale down or pause the offending service immediately.
3. **Notify Stakeholders** – Inform the Operations Lead and Finance team about the incident.
4. **Investigate** – Use cloud billing tools to narrow down the cause. Check recent deployments or configuration changes.
5. **Remediate** – Roll back deployments or adjust resource allocations as needed.
6. **Postmortem** – Document the incident in Confluence, including root cause and preventive actions.

Store this document in Confluence and update it whenever procedures change.
