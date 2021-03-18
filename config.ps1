param (
    [Parameter(mandatory=$true)]
    [string]$Commands
)

python $PSScriptRoot/configure_device.py -c $PSScriptRoot/configs/$Commands

# Return the exit code of the python script [0=success, 1=error]
exit $LASTEXITCODE
