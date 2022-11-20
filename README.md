# elonmusk
Microblogging service similar to Twitter

## Development

**Install python dependencies**

`pip install -r requirements.txt`

**Use VSCode with the following extensions**

- Python
- Pylance
- isort

**Add to settings.json**

`Ctrl`+`Shift`+`P` -> Open User Settings (JSON) -> `enter`

```json
"[python]": {
  "python.formatting.provider": "black",
  "python.linting.flake8Enabled": true,
  "python.linting.flake8Args": [
    "--max-line-length=88"
  ],
  "python.languageServer": "Pylance",
  "python.analysis.typeCheckingMode": "strict",
  "files.insertFinalNewline": true,
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  },
  "python.analysis.diagnosticMode": "workspace"
}
```

**Create empty database for testing**

`python create_blank_database.py 1.db`

**Run development server**

`python -m elonmuskserver`
