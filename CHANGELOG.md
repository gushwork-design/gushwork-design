# Changelog

Every released version, newest first. **Generated from git history** by
`scripts/changelog.sh` — do not edit by hand, the next release will overwrite it.

`Session` is the chat the change came from — a `claude://resume/<uuid>` deep link that
reopens that conversation in the Claude desktop app, recorded as a `Session:` trailer on
the release commit.

**The link only resolves on the machine holding the transcript.** It is a pointer for the
maintainer, not something a teammate can follow — for everyone else the commit link is the
one that works. Entries before the trailer convention are backfilled from first-hand
knowledge only; a blank cell means nobody could vouch for it.

To check what you are running: the skill announces its own version and date at the start of
every session. Trust that line over memory — it is stamped into the file, so **a stale copy
reports its own stale date.**

| Version | Date | What changed | Commit | Session |
|---|---|---|---|---|
| **v1.28.1** | 08 Aug 2026 18:06 | fall back to the backfill table when a trailer has no uuid | [`5a8df70`](https://github.com/utsav-gushwork/gushwork-design/commit/5a8df70cce32dde46da01cfdabdc9cbae07972b5) | [Gushwork Design System plugin](claude://resume/5a7c696b-5bbf-4aee-adf8-603e744f9018) |
| **v1.28.0** | 08 Aug 2026 18:05 | the Session column is a claude://resume deep link | [`6388221`](https://github.com/utsav-gushwork/gushwork-design/commit/6388221e9e506db19c6281d1165ff0c41f24ad16) | [Gushwork Design System plugin](claude://resume/5a7c696b-5bbf-4aee-adf8-603e744f9018) |
| **v1.27.0** | 08 Aug 2026 17:59 | a derived changelog, so multi-chat releases stay traceable | [`732d4df`](https://github.com/utsav-gushwork/gushwork-design/commit/732d4dff9b864016028460b97ae381bc268fd624) | [Gushwork Design System plugin](claude://resume/5a7c696b-5bbf-4aee-adf8-603e744f9018) |
| **v1.26.0** | 08 Aug 2026 17:50 | the creator stamp carries a time, and the login screen's build rules | [`499cdde`](https://github.com/utsav-gushwork/gushwork-design/commit/499cdde30f8d32b21cbff129a906a42c775da22d) | [Website performance dashboard](claude://resume/5eeaa384-81a5-460f-8fff-20a987090035) |
| **v1.25.0** | 08 Aug 2026 17:40 | R12/R13: the login screen's text props have jobs, and the subtext is two lines | [`bdfa56a`](https://github.com/utsav-gushwork/gushwork-design/commit/bdfa56ac2a1af971479edc8be9f7aacad18b0608) | [Website performance dashboard](claude://resume/5eeaa384-81a5-460f-8fff-20a987090035) |
| **v1.24.1** | 08 Aug 2026 17:08 | stamp the mirror-divergence guard so it actually propagates | [`d8c6bb8`](https://github.com/utsav-gushwork/gushwork-design/commit/d8c6bb82267a94a5d8152ec7dd5935aa22fe4f80) | [Gushwork Design System plugin](claude://resume/5a7c696b-5bbf-4aee-adf8-603e744f9018) |
| **v1.24.0** | 08 Aug 2026 14:05 | the dashboard surface is fully measured | [`8a77366`](https://github.com/utsav-gushwork/gushwork-design/commit/8a77366a9bb98c52220057109ee003f4af33154d) | [Gushwork Design System plugin](claude://resume/5a7c696b-5bbf-4aee-adf8-603e744f9018) |
| **v1.23.0** | 08 Aug 2026 13:59 | six more dashboard components measured; chart palette blocker resolved | [`281a606`](https://github.com/utsav-gushwork/gushwork-design/commit/281a6062579a00f318e6e762df475e3acb18953a) | [Gushwork Design System plugin](claude://resume/5a7c696b-5bbf-4aee-adf8-603e744f9018) |
| **v1.22.0** | 08 Aug 2026 13:43 | lock in every open decision; promote the text field to a shared atom | [`49f980b`](https://github.com/utsav-gushwork/gushwork-design/commit/49f980b5e265631985af7f908b3c92bdc206a4ba) | [Gushwork Design System plugin](claude://resume/5a7c696b-5bbf-4aee-adf8-603e744f9018) |
| **v1.21.0** | 08 Aug 2026 13:23 | re-measure the login screen, correct all three Button hover values | [`8de9b9b`](https://github.com/utsav-gushwork/gushwork-design/commit/8de9b9b85cfef0c8579f18714ed454b3b8ba31c5) | [Gushwork Design System plugin](claude://resume/5a7c696b-5bbf-4aee-adf8-603e744f9018) |
| **v1.19.0** | 07 Aug 2026 22:24 | lock in the rulings, fixes and components from the website-performance build | [`9af4649`](https://github.com/utsav-gushwork/gushwork-design/commit/9af46490b7be124ec8c6bab69bb7fc70c02345f8) | [Website performance dashboard](claude://resume/5eeaa384-81a5-460f-8fff-20a987090035) |
