Write-Host "Cloning repo..."

# This installation script will prefer cloning by ssh if it is setup on the client machine
# Check for presence of common SSH key names
$ssh_dir = "$($env:HOME)\.ssh"
$keys = @("id_rsa", "id_ed25519", "id_dsa", "id_ecdsa")

$found = $false
foreach ($key in $keys) {
  if (Test-Path -Path "$ssh_dir\$key" -PathType Leaf) {
    $found = $true
    Write-Host "SSH key found. Cloning with SSH..."
    git clone ssh://git@github.com/cdf144/bookstore-web-app.git
    break
  }
}

# Fallback to HTTPS if SSH key check fails
if (!$found) {
  Write-Host "SSH key not found. Cloning with HTTPS..."
  git clone https://github.com/cdf144/bookstore-web-app.git
}

cd bookstore-web-app/

Write-Host "Creating virtual environment..."
python -m venv .venv
.\.venv\Scripts\activate.ps1

Write-Host "Upgrading pip and installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
