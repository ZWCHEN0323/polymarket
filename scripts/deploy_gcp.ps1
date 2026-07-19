<#
.SYNOPSIS
    Deploy Polymarket bot to Cloud Run via Cloud Build.

.DESCRIPTION
    Submits cloudbuild.yaml to Google Cloud Build, builds the container image,
    pushes to Artifact Registry, and deploys to Cloud Run.
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

function Get-ServiceUrl {
    # Return the deployed Cloud Run service URL.
    return gcloud run services describe $ServiceName `
        --region=$Region `
        --project=$ProjectId `
        --format="value(status.url)"
}

Assert-GcloudInstalled
gcloud config set project $ProjectId

Write-Host "Submitting Cloud Build for project $ProjectId ..."
gcloud builds submit . `
    --config=cloudbuild.yaml `
    --project=$ProjectId `
    --substitutions=_REGION=$Region,_SERVICE_NAME=$ServiceName,_REPOSITORY=$Repository

if ($LASTEXITCODE -ne 0) {
    throw "Cloud Build deployment failed."
}

$serviceUrl = Get-ServiceUrl
Write-Host ""
Write-Host "Deployment successful."
Write-Host "Service URL: $serviceUrl"
Write-Host ""
Write-Host "Verify:"
Write-Host "  curl $serviceUrl/"
Write-Host "  curl $serviceUrl/health"
