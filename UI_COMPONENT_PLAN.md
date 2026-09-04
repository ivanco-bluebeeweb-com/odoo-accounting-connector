# Odoo Accounting Connector — UI Component Plan

## Sidebar structure
Use a plain full-width vertical layout; no decorative cards. The sidebar contains: connection status/list, connect form when needed, a help modal trigger, and **App settings as the final item**.

## Form rules (mandatory)
- Each `Input` has a visible `Label`; placeholders are specific to the requested value.
- The form container spans the complete sidebar width and its inner content is stretched to that width.
- Setup instructions exist only in the help modal, never duplicated next to the form.
- Secrets use secret inputs and never re-render their stored values.
- Validation feedback appears next to the relevant field and preserves non-secret user input.

## Views to implement after discovery
- **Connection:** connect, list masked connections, reauthorization state and settings-only disconnect.
- **Overview:** a read-only health/audit summary derived from verified endpoints.
- **Resources:** searchable/paginated lists and detail drawer/view for verified provider resources.
- **Operations:** forms for verified create/update operations; destructive or financial actions visually marked.
- **Webhooks:** verified subscriptions only, including signing-secret guidance and delivery state when available.

## Acceptance checks
Test narrow and wide sidebar rendering, empty/connected/error states, keyboard navigation, visible labels, contextual placeholders, and absence of duplicated onboarding instructions.
