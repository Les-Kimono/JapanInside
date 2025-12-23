# Deploy JapanInside to Kubernetes
# Usage: .\deploy.ps1

Write-Host ">> Deploying to Kubernetes..." -ForegroundColor Green

# Check if kubectl is available
if (-not (Get-Command kubectl -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] kubectl not found. Please install it first." -ForegroundColor Red
    Write-Host "Install with: choco install kubernetes-cli" -ForegroundColor Yellow
    exit 1
}

# Deploy namespace and config
Write-Host "`n[1/5] Deploying namespace and configuration..." -ForegroundColor Cyan
kubectl apply -f k8s/config/

# Deploy database
Write-Host "`n[2/5] Deploying PostgreSQL..." -ForegroundColor Cyan
kubectl apply -f k8s/db/

# Wait for PostgreSQL
Write-Host "`n[WAIT] Waiting for PostgreSQL to be ready..." -ForegroundColor Yellow
kubectl wait --namespace=japaninside --for=condition=ready pod -l app=postgres --timeout=180s

# Deploy backend
Write-Host "`n[3/5] Deploying Backend..." -ForegroundColor Cyan
kubectl apply -f k8s/backend/

# Deploy frontend
Write-Host "`n[4/5] Deploying Frontend..." -ForegroundColor Cyan
kubectl apply -f k8s/frontend/

# Wait for all pods
Write-Host "`n[WAIT] Waiting for all pods to be ready..." -ForegroundColor Yellow
kubectl wait --namespace=japaninside --for=condition=ready pod -l app=backend --timeout=120s
kubectl wait --namespace=japaninside --for=condition=ready pod -l app=frontend --timeout=120s

# Show status
Write-Host "`n[SUCCESS] Deployment complete!" -ForegroundColor Green
Write-Host "`n=== Pods ===" -ForegroundColor Cyan
kubectl get pods -n japaninside

Write-Host "`n=== Services ===" -ForegroundColor Cyan
kubectl get svc -n japaninside

Write-Host "`n=== Persistent Volume Claims ===" -ForegroundColor Cyan
kubectl get pvc -n japaninside

Write-Host "`n=== Access the application ===" -ForegroundColor Green
Write-Host "  Frontend: minikube service frontend -n japaninside" -ForegroundColor White
Write-Host "  Backend:  minikube service backend -n japaninside" -ForegroundColor White

