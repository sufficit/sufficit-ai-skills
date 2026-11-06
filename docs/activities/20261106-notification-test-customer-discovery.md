# Customer discovery before requesting notification test identifiers

The tablet's official event-test workflow discovered POST /Notification/Test,
but asked for internal customer/contact GUIDs before executing a customer name
or notification-destination lookup. Package 1.0.26 now requires discovery of the
live /Sales/Clients and /Notification/Contact/Search contracts and execution of
those reads. Genuine multiple customer matches still require a short human
identity choice; internal GUIDs are not a substitute for doing the lookup.
The reference also separates a service-generated notification from the personal
WhatsApp gateway. No real message was sent during this failed acceptance attempt.

Version metadata, release.json and reviewed catalog are aligned at 1.0.26.
Validation: 185 packages, version/index/Markdown checks, 40 installation tests.
The complete layperson workflow remains pending device acceptance.
