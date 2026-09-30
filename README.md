# Nurture

Nurture is an experimental, beginner-friendly programming language and IDE using `.usd` source files.

## Current release: 0.1.0

- Prefix autocomplete from the first character
- `web.` / `net.` / `file.` / `system.` member autocomplete
- Registry-driven documentation
- Variables and expressions
- `if / elif / else`
- `while`
- `loop`
- `function / return`
- `try / except`
- `link module`
- Files, folders, JSON, math, crypto
- HTTP and basic network diagnostics
- System/process information
- Tkinter IDE
- F5 execution

## Run

Python 3.10+:

```bash
python nurture.py
```

Try:

```text
name = "Udit"
write("Hello " + name)

loop i in 1..5:
    write(i)
```

Press **F5**.

## Autocomplete

Typing `w` immediately suggests `while`, `web`, and `write`.

Typing `web.` suggests:

```text
web.get()
web.post()
web.put()
web.delete()
web.request()
web.download()
web.screenshot()
web.status()
web.headers()
web.cookies()
```

The same registry powers autocomplete and documentation.

## Project layout

```text
Nurture/
├── nurture.py
├── launcher.py
├── nurture_lang/
├── nurture_std/
├── docs/
├── examples/
├── tests/
├── LICENSE
├── PRIVACY_POLICY.md
├── COPYRIGHT.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── requirements.txt
└── .gitignore
```

## Security

Nurture is intended for programming, administration, diagnostics, defensive security engineering, and authorized security research. Network APIs must only be used against systems you own or are authorized to test.

The project intentionally does not implement credential theft, malware deployment, unauthorized access, exploit chains, stealth/evasion, or privilege-bypass automation.

## AI

AI is kept separate from the deterministic interpreter. The project is designed so an optional AI assistant can later explain errors, generate Nurture code, and provide contextual suggestions without becoming a hidden runtime dependency.

See `docs/AI.md`.

## License

MIT. See `LICENSE`.

## Copyright

See `COPYRIGHT.md`.

## Running a `.usd` script from the command line

```text
python launcher.py examples/showcase.usd
```

`input()` reads directly from the terminal in CLI mode. When running the IDE, `input()` opens a native input dialog instead.
