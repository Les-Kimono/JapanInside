# Supprime les ressources Kubernetes JapanInside
# Usage: 
#   .\scripts\clean.ps1            # Demande confirmation
#   .\scripts\clean.ps1 -Force     # Supprime sans confirmation
#   .\scripts\clean.ps1 -All       # Supprime tout + Minikube

param(
    [switch]$Force,
    [switch]$All
)

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "   JapanInside - Nettoyage Kubernetes" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

if ($All) {
    Write-Host "[WARNING] Mode -All : Suppression complete (Minikube inclus)" -ForegroundColor Red
} else {
    Write-Host "Suppression des ressources JapanInside uniquement" -ForegroundColor Yellow
}

# Demander confirmation si -Force n'est pas specifie
if (-not $Force) {
    $confirm = Read-Host "`nContinuer? (o/N)"
    if ($confirm -ne 'o' -and $confirm -ne 'O') {
        Write-Host "Operation annulee." -ForegroundColor Gray
        exit 0
    }
}

Write-Host "`n[CLEAN] Suppression des ressources Kubernetes..." -ForegroundColor Cyan
kubectl delete -f k8s/frontend/ --ignore-not-found
kubectl delete -f k8s/backend/ --ignore-not-found
kubectl delete -f k8s/db/ --ignore-not-found
kubectl delete -f k8s/config/ --ignore-not-found

if ($All) {
    Write-Host "`n[CLEAN] Arret et suppression de Minikube..." -ForegroundColor Red
    minikube stop
    minikube delete
}

Write-Host "`n[SUCCESS] Nettoyage termine!" -ForegroundColor Green
Write-Host ""
