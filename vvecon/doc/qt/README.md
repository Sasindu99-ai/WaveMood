## vvecon (Qt) Documentation

vvecon is a lightweight PyQt6 application framework used by the MKT app in this repo. It provides:

- Window/View architecture with simple navigation and lifecycle hooks
- UI utilities for density-independent sizing (dp/sp), margins and padding
- Theming (colors, images), icon set access, and reusable styled widgets
- Shared signals, a minimal thread pool, and a small HTTP Controller
- Optional DB helper for quick local persistence

Docs set:
- Getting Started: `getting-started.md`
- Core Concepts: `core-concepts.md`
- Theming, Icons, UI utils: `theming-icons-ui.md`
- API Reference (core/res/util/models/signals/thread/db): `reference.md`
- Widgets & Styles: `widgets.md`
- Threading & Signals: `threading-signals.md`
- API Controller: `api-controller.md`
- Environment: `env.md`
- Database: `database.md`
- Logging: `logging.md`
- Examples from MKT: `examples-mkt.md`

Icon explorer (browse available icons):
```bash
python -m vvecon qt icons
```


