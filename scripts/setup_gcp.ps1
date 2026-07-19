<#
.SYNOPSIS
    One-time Google Cloud resource setup for Polymarket bot deployment.

.DESCRIPTION
    Enables required APIs, creates Artifact Registry repository, and grants
    Cloud Build permissions to deploy Cloud Run services.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$ProjectId,

    [string]$Region = "asia-northeast1",

    [string]$Repository = "polymarket-bot",

    [string]$ServiceName = "polymarket-bot"
)

$ErrorActionPreference = "Stop"

function Assert-GcloudInstalled {
    # Ensure Google Cloud SDK is available in PATH.
    $gcloud = Get-Command gcloud -ErrorAction SilentlyContinue
    if (-not $gcloud) {
        throw "gcloud CLI not found. Install Google Cloud SDK first."
    }
}

function Enable-RequiredApis {
    # Enable GCP services required for Cloud Build and Cloud Run.
    $services = @(
        "run.googleapis.com",
        "cloudbuild.googleapis.com",
        "artifactregistry.googleapis.com",
        "secretmanager.googleapis.com",
        "cloudscheduler.googleapis.com"
    )

    gcloud services enable $services --project=$ProjectId
}

function New-ArtifactRegistryRepository {
    # Create Docker Artifact Registry repository when it does not exist.
    $existing = gcloud artifacts repositories describe $Repository `
        --location=$Region `
        --project=$ProjectId `
        2>$null

    if ($LASTEXITCODE -eq 0) {
        Write-Host "Artifact Registry repository already exists: $Repository"
        return
    }

    gcloud artifacts repositories create $Repository `
        --repository-format=docker `
        --location=$Region `
        --description="Polymarket bot container images" `
        --project=$ProjectId
}

function Grant-CloudBuildPermissions {
    # Grant Cloud Build service account permissions for deploy.
    $projectNumber = gcloud projects describe $ProjectId --format="value(projectNumber)"
    $cloudBuildServiceAccount = "$projectNumber@cloudbuild.gserviceaccount.com"

    $roles = @(
        "roles/run.admin",
        "roles/iam.serviceAccountUser",
        "roles/artifactregistry.writer"
    )

    foreach ($role in $roles) {
        gcloud projects add-iam-policy-binding $ProjectId `
            --member="serviceAccount:$cloudBuildServiceAccount" `
            --role=$role `
            --quiet | Out-Null
    }

    Write-Host "Granted Cloud Build permissions to $cloudBuildServiceAccount"
}

Assert-GcloudInstalled
gcloud config set project $ProjectId
Enable-RequiredApis
New-ArtifactRegistryRepository
Grant-CloudBuildPermissions

Write-Host ""
Write-Host "GCP setup complete."
Write-Host "Project ID : $ProjectId"
Write-Host "Region     : $Region"
Write-Host "Repository : $Repository"
Write-Host "Service    : $ServiceName"
Write-Host ""
Write-Host "Next step: run scripts/deploy_gcp.ps1 -ProjectId $ProjectId"
