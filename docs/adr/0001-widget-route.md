# Widgets: text skeleton first, one generated block

The README is mostly plain Markdown; only the Activity block is machine-generated, and it comes from GitHub Actions rather than a third-party URL service. We rejected both pure alternatives: an all-URL-service README (one line to add, but public instances rate-limit and the whole block turns into `Something went wrong`), and an all-Action README (stable, but every section then costs a workflow and the repo fills with commit noise).

Considered options: all URL-service, all Action, hybrid. Hybrid won because the page has to stay readable when every image 404s — the six text blocks carry the whole message, and the Activity block is deletable without leaving a hole.

Consequences: adding a widget now means adding a workflow, so widgets are expensive by design. The two URL-shaped exceptions (shields badges in Stack) were kept because a broken badge costs one word, not a paragraph.
