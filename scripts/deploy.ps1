param(
    [string]$Region = "ap-south-1",
    [string]$StackName = "smart-crop-disease",
    [string]$PublicAccessCidr = "",
    [ValidateSet("t3.small", "t3.medium")]
    [string]$InstanceType = "t3.small",
    [string]$Profile = ""
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$modelPath = Join-Path $projectRoot "models\crop_disease_model.keras"
$classPath = Join-Path $projectRoot "models\class_names.json"
$templatePath = Join-Path $projectRoot "infra\template.yaml"

if ([string]::IsNullOrWhiteSpace($PublicAccessCidr)) {
    throw "Set -PublicAccessCidr to the reviewer or office IPv4 CIDR (for example, your current public IP with /32). The deployment does not open the app to everyone."
}
$cidrParts = $PublicAccessCidr.Split('/')
$parsedAddress = [System.Net.IPAddress]::Any
$prefixLength = -1
if ($cidrParts.Count -ne 2 -or
    -not [System.Net.IPAddress]::TryParse($cidrParts[0], [ref]$parsedAddress) -or
    $parsedAddress.AddressFamily -ne [System.Net.Sockets.AddressFamily]::InterNetwork -or
    -not [int]::TryParse($cidrParts[1], [ref]$prefixLength) -or
    $prefixLength -lt 1 -or $prefixLength -gt 32) {
    throw "PublicAccessCidr must be an IPv4 CIDR with a prefix from /1 to /32."
}

if (-not (Get-Command aws -ErrorAction SilentlyContinue)) {
    throw "AWS CLI v2 is not installed. Install it using the official AWS guide, configure access, then rerun this script."
}
if (-not (Test-Path -LiteralPath $modelPath) -or -not (Test-Path -LiteralPath $classPath)) {
    throw "A trained model is required. Add models\crop_disease_model.keras and models\class_names.json before deploying."
}
if (-not (Test-Path -LiteralPath $templatePath)) {
    throw "CloudFormation template not found: $templatePath"
}

$awsArgs = @("--region", $Region)
if ($Profile) { $awsArgs += @("--profile", $Profile) }
& aws sts get-caller-identity @awsArgs | Out-Null
if ($LASTEXITCODE -ne 0) { throw "AWS credentials are not ready for region $Region." }

$amiArgs = @(
    "ec2", "describe-images",
    "--owners", "amazon",
    "--filters",
    "Name=name,Values=al2023-ami-2023.*-kernel-*-x86_64",
    "Name=state,Values=available",
    "--query", "Images | sort_by(@, &CreationDate)[-1].ImageId",
    "--output", "text",
    "--region", $Region
)
if ($Profile) { $amiArgs += @("--profile", $Profile) }
$imageId = & aws @amiArgs
if ($LASTEXITCODE -ne 0 -or $imageId -notmatch "^ami-") {
    throw "Could not find a current Amazon Linux 2023 x86_64 AMI in $Region."
}

Write-Host "Deploying CloudFormation stack '$StackName' in $Region..."
$deployArgs = @(
    "cloudformation", "deploy",
    "--template-file", $templatePath,
    "--stack-name", $StackName,
    "--capabilities", "CAPABILITY_IAM",
    "--region", $Region,
    "--parameter-overrides",
    "ImageId=$imageId",
    "InstanceType=$InstanceType",
    "PublicAccessCidr=$PublicAccessCidr"
)
if ($Profile) { $deployArgs += @("--profile", $Profile) }
& aws @deployArgs
if ($LASTEXITCODE -ne 0) { throw "CloudFormation deployment failed. Check the stack events in AWS CloudFormation." }

$describeArgs = @(
    "cloudformation", "describe-stacks",
    "--stack-name", $StackName,
    "--query", "Stacks[0].Outputs",
    "--output", "json",
    "--region", $Region
)
if ($Profile) { $describeArgs += @("--profile", $Profile) }
$outputsJson = & aws @describeArgs
if ($LASTEXITCODE -ne 0) { throw "Could not read CloudFormation outputs." }
$outputs = $outputsJson | ConvertFrom-Json
$bucket = ($outputs | Where-Object OutputKey -eq "ImageBucketName").OutputValue
$url = ($outputs | Where-Object OutputKey -eq "AppUrl").OutputValue
if (-not $bucket -or -not $url) { throw "CloudFormation outputs did not include the app URL and bucket." }

$workRoot = [IO.Path]::GetFullPath((Join-Path $projectRoot "work"))
$stage = [IO.Path]::GetFullPath((Join-Path $workRoot "release"))
$stagePrefix = $workRoot.TrimEnd([IO.Path]::DirectorySeparatorChar) + [IO.Path]::DirectorySeparatorChar
if (-not $stage.StartsWith($stagePrefix, [StringComparison]::OrdinalIgnoreCase)) {
    throw "Refusing to remove an unexpected staging path: $stage"
}
$releaseZip = Join-Path $workRoot "app-release.zip"
New-Item -ItemType Directory -Path $workRoot -Force | Out-Null
if (Test-Path -LiteralPath $stage) { Remove-Item -LiteralPath $stage -Recurse -Force }
New-Item -ItemType Directory -Path $stage -Force | Out-Null
Copy-Item -LiteralPath (Join-Path $projectRoot "app") -Destination $stage -Recurse
Copy-Item -LiteralPath (Join-Path $projectRoot "requirements.txt") -Destination $stage
Copy-Item -LiteralPath (Join-Path $projectRoot "Dockerfile") -Destination $stage
New-Item -ItemType Directory -Path (Join-Path $stage "models") -Force | Out-Null
Copy-Item -LiteralPath $modelPath -Destination (Join-Path $stage "models")
Copy-Item -LiteralPath $classPath -Destination (Join-Path $stage "models")
if (Test-Path -LiteralPath $releaseZip) { Remove-Item -LiteralPath $releaseZip -Force }
Compress-Archive -Path (Join-Path $stage "*") -DestinationPath $releaseZip -CompressionLevel Optimal

$uploadArgs = @(
    "s3", "cp", $releaseZip, "s3://$bucket/release/app-release.zip",
    "--region", $Region,
    "--sse", "AES256"
)
if ($Profile) { $uploadArgs += @("--profile", $Profile) }
& aws @uploadArgs
if ($LASTEXITCODE -ne 0) { throw "Could not upload the application bundle to the private S3 bucket." }

Write-Host "Waiting for the EC2 instance to build the app and load the model..."
$ready = $false
for ($attempt = 0; $attempt -lt 60; $attempt++) {
    try {
        $response = Invoke-WebRequest -Uri "$url/healthz" -TimeoutSec 8
        if ($response.StatusCode -eq 200 -and $response.Content -match '"status"\s*:\s*"ok"') {
            $ready = $true
            break
        }
    } catch {
        Start-Sleep -Seconds 15
    }
}
if (-not $ready) {
    Write-Warning "The stack is created, but the app did not become ready within 15 minutes. Review EC2 system and CloudWatch logs."
    Write-Host "App URL: $url"
    exit 2
}

Write-Host "Deployment ready: $url"
