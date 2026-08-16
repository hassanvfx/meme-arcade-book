# Interior template

`lulu-us-trade-interior-template.docx` is generated deterministically from `template-source.md` by `make template`, then committed as the DOCX layout reference. Its immutable production identity and geometry are in [`lulu-us-trade-6x9-no-bleed-v1.json`](lulu-us-trade-6x9-no-bleed-v1.json). It targets a no-bleed 6×9 US Trade interior. The final interior is exported through LibreOffice headless with an isolated temporary profile, then assembled, flattened where needed, audited, and visually reviewed.
