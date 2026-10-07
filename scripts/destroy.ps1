param(
    [string]$Region = "ap-south-1",
    [string]$StackName = "smart-crop-disease",
    [string]$Profile = ""
)

$ErrorActionPreference = "Stop"
if (-not (Get-Command aws -ErrorAction SilentlyContinue)) {
    throw "AWS CLI is required to remove this stack."
}

$common = @("--region", $Region)
if ($Profile) { $common += @("--profile", $Profile) }
$outputs = & aws cloudformation describe-stacks --stack-name $StackName --query "Stacks[0].Outputs" --output json @common 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Stack '$StackName' was not found in $Region."
    exit 0
}
$bucket = ($outputs | ConvertFrom-Json | Where-Object OutputKey -eq "ImageBucketName").OutputValue
if ($bucket) {
    Write-Host "Removing objects from this stack's bucket: $bucket"
    & aws s3 rm "s3://$bucket" --recursive @common
    if ($LASTEXITCODE -ne 0) { throw "Could not empty bucket $bucket. Stack was not deleted." }
}
& aws cloudformation delete-stack --stack-name $StackName @common
if ($LASTEXITCODE -ne 0) { throw "Could not start stack deletion." }
& aws cloudformation wait stack-delete-complete --stack-name $StackName @common
if ($LASTEXITCODE -ne 0) { throw "Stack deletion did not complete. Check CloudFormation events." }
Write-Host "Stack '$StackName' and its bucket contents were removed."
