Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "   JapanInside - Statut" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

$namespace = kubectl get namespace japaninside -o jsonpath='{.metadata.name}' 2>$null
if (-not $namespace) {
    Write-Host "X Application non deployee" -ForegroundColor Red
    Write-Host "  Lancer: deploy.ps1" -ForegroundColor Yellow
    exit 1
}

Write-Host "Pods:" -ForegroundColor Cyan
kubectl get pods -n japaninside

Write-Host "`nServices:" -ForegroundColor Cyan
kubectl get svc -n japaninside

# Verifier les IPs de LoadBalancer
$backendIP = kubectl get svc backend -n japaninside -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>$null
$frontendIP = kubectl get svc frontend -n japaninside -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>$null

Write-Host "`nURLs d'acces:" -ForegroundColor Magenta
if ($frontendIP) {
    Write-Host "  Frontend: http://${frontendIP}:5173" -ForegroundColor Green
} else {
    Write-Host "  Frontend: <en attente - tunnel non lance?>" -ForegroundColor Yellow
}
if ($backendIP) {
    Write-Host "  Backend:  http://${backendIP}:8000" -ForegroundColor Green
} else {
    Write-Host "  Backend:  <en attente - tunnel non lance?>" -ForegroundColor Yellow
}

Write-Host ""
