[CmdletBinding(SupportsShouldProcess, ConfirmImpact = "Medium")]
param(
    [ValidatePattern("^[a-zA-Z0-9._-]+$")]
    [string]$RepositoryName = "build-character-panel-skill",

    [ValidateSet("private", "public", "internal")]
    [string]$Visibility = "private"
)

$ErrorActionPreference = "Stop"

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw "GitHub CLI is required. Install gh, then run this script again."
}

cmd /d /c "gh auth status >nul 2>nul"
if ($LASTEXITCODE -ne 0) {
    throw "GitHub CLI is not authenticated. Run 'gh auth login', then run this script again."
}

$insideWorkTree = git rev-parse --is-inside-work-tree 2>$null
if ($LASTEXITCODE -ne 0 -or $insideWorkTree -ne "true") {
    throw "Run this script from inside the build-character-panel Git repository."
}

$pending = @(git status --porcelain)
if ($pending.Count -gt 0) {
    throw "The Git working tree must be clean before publication."
}

$branch = git branch --show-current
if (-not $branch) {
    throw "Cannot publish from a detached HEAD."
}

$owner = gh api user --jq .login
if ($LASTEXITCODE -ne 0 -or -not $owner) {
    throw "Could not determine the authenticated GitHub account."
}

$fullName = "$owner/$RepositoryName"
gh repo view $fullName --json nameWithOwner 1>$null 2>$null
$repositoryExists = $LASTEXITCODE -eq 0

if (-not $repositoryExists) {
    if (-not $PSCmdlet.ShouldProcess(
        $fullName,
        "Create a $Visibility GitHub repository and push $branch"
    )) {
        return
    }

    switch ($Visibility) {
        "private" {
            gh repo create $fullName --private --source . --remote origin --push
        }
        "public" {
            gh repo create $fullName --public --source . --remote origin --push
        }
        "internal" {
            gh repo create $fullName --internal --source . --remote origin --push
        }
    }

    if ($LASTEXITCODE -ne 0) {
        throw "GitHub repository creation or initial push failed."
    }
}
else {
    $origin = git remote get-url origin 2>$null
    if ($LASTEXITCODE -ne 0) {
        git remote add origin "https://github.com/$fullName.git"
    }
    else {
        $originRepository = gh repo view $origin --json nameWithOwner --jq .nameWithOwner
        if ($LASTEXITCODE -ne 0 -or $originRepository -ne $fullName) {
            throw "Existing origin points to '$originRepository', not '$fullName'."
        }
    }

    if (-not $PSCmdlet.ShouldProcess($fullName, "Push $branch to the existing repository")) {
        return
    }

    git push -u origin $branch
    if ($LASTEXITCODE -ne 0) {
        throw "Git push failed."
    }
}

$url = gh repo view $fullName --json url --jq .url
if ($LASTEXITCODE -ne 0 -or -not $url) {
    throw "Publication completed, but the repository URL could not be verified."
}

Write-Output "Published: $url"
Write-Output "Branch: $branch"
Write-Output "Commit: $(git rev-parse HEAD)"
