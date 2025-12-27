Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "   Minikube Tunnel - LoadBalancer" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

# Verifier Minikube
$status = minikube status --format='{{.Host}}' 2>$null
if ($status -ne "Running") {
    Write-Host "X Minikube n'est pas demarre!" -ForegroundColor Red
    Write-Host "  Demarrer avec: minikube start" -ForegroundColor Yellow
    exit 1
}

Write-Host "OK Minikube est demarre" -ForegroundColor Green
Write-Host ""
Write-Host "IMPORTANT:" -ForegroundColor Yellow
Write-Host "  - Ce terminal doit rester OUVERT" -ForegroundColor Yellow
Write-Host "  - Appuyer sur Ctrl+C pour arreter le tunnel" -ForegroundColor Yellow
Write-Host "  - Necessite les privileges Administrateur" -ForegroundColor Yellow
Write-Host ""
Write-Host "Demarrage du tunnel..." -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Gray
Write-Host ""

# Demarrer le tunnel
minikube tunnel
