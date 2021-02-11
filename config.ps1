param (
    [Parameter(mandatory=$true)]
    [string]$Devices,
    [Parameter(mandatory=$true)]
    [string]$Username,
    [Parameter(mandatory=$true)]
    [string]$Password,
    [Parameter(mandatory=$true)]
    [string]$Enablepass,
    [Parameter(mandatory=$true)]
    [string]$Commands
)

python $PSScriptRoot/configure_device.py --devices $PSScriptRoot/$Devices --username $Username --password $Password --enablepass $Enablepass --commands $PSScriptRoot/configs/$Commands --verbose

# Return the exit code of the python script [0=success, 1=error]
exit $LASTEXITCODE