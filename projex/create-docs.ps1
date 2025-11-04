$files = @{
    "docs\cli\create.md" = "# projex create`n`nCreate new projects.`n`nSee main documentation for details."
    "docs\cli\add.md" = "# projex add`n`nAdd components to existing projects.`n`nSee main documentation for details."
    "docs\cli\env.md" = "# projex env`n`nManage environment configurations.`n`nSee main documentation for details."
    "docs\cli\deps.md" = "# projex deps`n`nManage project dependencies.`n`nSee main documentation for details."
    "docs\cli\validate.md" = "# projex validate`n`nValidate project structure.`n`nSee main documentation for details."
    "docs\cli\info.md" = "# projex info`n`nShow project information.`n`nSee main documentation for details."
    "docs\cli\list.md" = "# projex list`n`nList available templates.`n`nSee main documentation for details."
    "docs\features\scaffolding.md" = "# Smart Scaffolding`n`nGenerate code components automatically.`n`nComing soon!"
    "docs\features\authentication.md" = "# Authentication`n`n4 authentication methods supported.`n`nComing soon!"
    "docs\features\databases.md" = "# Database Support`n`n5 database options available.`n`nComing soon!"
    "docs\features\styles.md" = "# Template Styles`n`nMinimal, Standard, and Full styles.`n`nComing soon!"
    "docs\features\cicd.md" = "# CI/CD Pipelines`n`nAutomatic pipeline generation.`n`nComing soon!"
    "docs\features\environments.md" = "# Environment Management`n`nMultiple environment support.`n`nComing soon!"
    "docs\features\dependencies.md" = "# Dependency Management`n`nCheck, update, and audit packages.`n`nComing soon!"
    "docs\features\docs-setup.md" = "# Documentation Setup`n`nMkDocs and Sphinx integration.`n`nComing soon!"
    "docs\features\testing.md" = "# Testing`n`nEnhanced pytest configuration.`n`nComing soon!"
    "docs\features\quality.md" = "# Code Quality`n`nPre-commit hooks and linting.`n`nComing soon!"
}

foreach ($file in $files.Keys) {
    $content = $files[$file]
    New-Item -Path $file -ItemType File -Force | Out-Null
    Set-Content -Path $file -Value $content
    Write-Host "✅ Created: $file" -ForegroundColor Green
}

Write-Host "`n🎉 All documentation files created!" -ForegroundColor Cyan
Write-Host "Run: mkdocs serve" -ForegroundColor Yellow