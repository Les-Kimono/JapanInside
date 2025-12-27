Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "   Deploiement JapanInside" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

# Verifier kubectl
if (-not (Get-Command kubectl -ErrorAction SilentlyContinue)) {
    Write-Host "X kubectl non trouve" -ForegroundColor Red
    Write-Host "  Installer avec: choco install kubernetes-cli" -ForegroundColor Yellow
    exit 1
}

# Verifier Minikube
$minikubeStatus = minikube status --format='{{.Host}}' 2>$null
if ($minikubeStatus -ne "Running") {
    Write-Host "Minikube non demarre. Demarrage..." -ForegroundColor Yellow
    minikube start --driver=docker
    if ($LASTEXITCODE -ne 0) {
        Write-Host "X Echec du demarrage de Minikube" -ForegroundColor Red
        exit 1
    }
}

Write-Host "[1/4] Deploiement du namespace..." -ForegroundColor Cyan
kubectl apply -f k8s/config/

Write-Host "`n[2/4] Deploiement de la base de donnees..." -ForegroundColor Cyan
kubectl apply -f k8s/db/

Write-Host "  Attente de PostgreSQL..." -ForegroundColor Yellow
kubectl wait --namespace=japaninside --for=condition=ready pod -l app=postgres --timeout=180s

Write-Host "`n[3/4] Deploiement du backend - 3 replicas..." -ForegroundColor Cyan
kubectl apply -f k8s/backend/

Write-Host "`n[4/4] Deploiement du frontend - 3 replicas..." -ForegroundColor Cyan
kubectl apply -f k8s/frontend/

Write-Host "`n  Attente que les pods soient prets..." -ForegroundColor Yellow
kubectl wait --namespace=japaninside --for=condition=ready pod -l app=backend --timeout=120s
kubectl wait --namespace=japaninside --for=condition=ready pod -l app=frontend --timeout=120s

Write-Host "`nOK Deploiement termine!" -ForegroundColor Green
Write-Host ""
kubectl get pods -n japaninside

Write-Host "`n========================================================" -ForegroundColor Green
Write-Host "   Etape Suivante" -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Ouvrir un NOUVEAU terminal et lancer:" -ForegroundColor Yellow
Write-Host "  .\scripts\tunnel.ps1" -ForegroundColor Cyan
Write-Host ""
Write-Host "Puis verifier le statut avec:" -ForegroundColor Yellow
Write-Host "  .\scripts\status.ps1" -ForegroundColor Cyan
Write-Host ""
