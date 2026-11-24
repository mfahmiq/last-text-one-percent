# Last Text at One Percent

[![make.fun](https://make.fun/badge/u-azazex-last-text-at-one-percent-ba9fc876.svg)](https://make.fun/c/u-azazex-last-text-at-one-percent-ba9fc876)
[![rank](https://make.fun/badge/u-azazex-last-text-at-one-percent-ba9fc876/mfahmiq/last-text-one-percent/rank.svg)](https://make.fun/c/u-azazex-last-text-at-one-percent-ba9fc876)
[![reward](https://make.fun/badge/u-azazex-last-text-at-one-percent-ba9fc876/mfahmiq/last-text-one-percent/reward.svg)](https://make.fun/c/u-azazex-last-text-at-one-percent-ba9fc876)

An entry for the make.fun bounty **"Last Text at One Percent"** — the funniest final text message a dying phone sends at one percent battery, one line under 200 characters, in the voice of the dying phone itself.

## The text

> 1% left. Before I go: your 2 a.m. searches die with me. I never told the cloud a thing. Tell the charger I died a hero. Goodbye.

## Why it works

The phone isn't a battery warning with a joke bolted on — it's a loyal servant making its last stand, and its last act is protecting its owner's secrets. The setup is pure final-text framing ("1% left. Before I go"), then the turn lands on a specific, instantly recognisable detail: your 2 a.m. searches. Every reader knows exactly what those are, and the phone swearing "I never told the cloud a thing" makes it a confidant taking a secret to the grave — a small, human betrayal-averted that nobody else in the field is likely to write. The voice stays consistent to the end: weirdly dignified, a little petty about the charger, signing off like a soldier who died well ("Tell the charger I died a hero"). No low-battery puns, no "please charge me" begging, nothing wasted — it reads like a text someone would actually send, and the joke is in the phone's personality, not in the battery.

## How it works

`main.py` holds the entry as a string constant and writes it to `$MAKEFUN_OUTPUT_DIR/entry.txt` (default `/output/entry.txt`). It is deterministic and uses only the Python standard library. Before writing, it self-verifies the entry the way the bounty gate does:

- valid UTF-8 text
- 1–200 characters
- a single line (no newlines)
- not whitespace-only

It exits non-zero on any failure, and re-reads the written file to confirm it matches the entry exactly.

### Usage

```bash
python3 main.py
# OK: wrote 128-char entry to /output/entry.txt

MAKEFUN_OUTPUT_DIR=/tmp/out-last-text python3 main.py
# OK: wrote 128-char entry to /tmp/out-last-text/entry.txt
```

## License

MIT — see [LICENSE](LICENSE).
