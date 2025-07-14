# Data Deletion and Export Workflow

Users may request deletion or export of their personal data at any time. Follow this process to handle requests and maintain auditability.

1. **Submit Request** – The user opens a support ticket or emails compliance.
2. **Verify Identity** – Confirm the requester owns the account and data.
3. **Track in Jira** – Create a Jira ticket referencing the request.
4. **Run Tools** – Use the `delete_user_data` or `export_user_data` scripts to locate and process the user's data.
5. **Log Actions** – All tool executions write to `audit.log` for compliance records.
6. **Notify User** – Inform the requester when the task is complete and attach the Jira ticket.

Store completed requests and logs in Confluence for future audits.
