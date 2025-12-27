# Supprime tout le deploiement
# Usage: .\scripts\clean.ps1

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "   JapanInside - Nettoyage" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Ceci va supprimer toutes les ressources JapanInside" -ForegroundColor Yellow
$confirm = Read-Host "Continuer? (o/N)"

if ($confirm -ne 'o' -and $confirm -ne 'O') {
    Write-Host "Annule." -ForegroundColor Gray
    exit 0
}

Write-Host "`nNettoyage en cours..." -ForegroundColor Cyan
kubectl delete -f k8s/frontend/ --ignore-not-found
kubectl delete -f k8s/backend/ --ignore-not-found
kubectl delete -f k8s/db/ --ignore-not-found
kubectl delete -f k8s/config/ --ignore-not-found

Write-Host "`nOK Nettoyage termine!" -ForegroundColor Green
Write-Host ""
