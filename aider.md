# aider - Your Coding Assistant Framework

## Folder Structure
```
aider/
├── .env.example          # API key configuration
├── aider.psm1           # PowerShell automation module
├── prompts/             # AI instruction templates
│   ├── conventions.md   # Coding standards
│   ├── fix-errors.md    # Error fixing guidelines
│   ├── fix-params.md    # Parameter validation rules
│   └── template.md      # Base interaction template
└── readme.md            # Framework documentation
```

## Key Features
- **Automated Code Review**: Review and improve code quality automatically
- **Iterative Fixing**: Process files until all issues are resolved
- **Standards Enforcement**: Ensure consistent coding practices
- **Documentation Generation**: Automatically create and update docs

## Example Workflow
```powershell
# Import the module
Import-Module .aider/aider.psm1

# Configure API keys
Set-AiderConfig -ApiKey $env:OPENAI_API_KEY

# Run automated tasks
Automate-CodeReview -FilePath "src/main.ps1"
Generate-Docs -FilePath "src/main.ps1"
Fix-Bugs -FilePath "src/main.ps1"
```

## Monitoring & Logging
Track assistant activity with:
```powershell
Start-Transcript -Path "aider-log.txt"
```
