Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "   Test du Proxy Frontend <-> Backend" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

function Test-Endpoint {
    param(
        [string]$Url,
        [string]$Description
    )
    
    Write-Host "Testing: $Description" -ForegroundColor Yellow
    Write-Host "  URL: $Url" -ForegroundColor Gray
    
    try {
        $response = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 5
        Write-Host "  ✅ Status: $($response.StatusCode)" -ForegroundColor Green
        
        # Afficher un aperçu de la réponse
        $content = $response.Content
        if ($content.Length -gt 200) {
            $content = $content.Substring(0, 200) + "..."
        }
        Write-Host "  Response: $content" -ForegroundColor Gray
        return $true
    }
    catch {
        Write-Host "  ❌ Error: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
    Write-Host ""
}

# Test 1: Backend direct
Write-Host "`n[1] Test Backend Direct" -ForegroundColor Cyan
Write-Host "----------------------------------------" -ForegroundColor Gray
$backendOk = Test-Endpoint "http://localhost:8000/api/health" "Backend Health Check"
$backendOk = Test-Endpoint "http://localhost:8000/api/villes" "Backend Villes" -and $backendOk

# Test 2: Frontend
Write-Host "`n[2] Test Frontend" -ForegroundColor Cyan
Write-Host "----------------------------------------" -ForegroundColor Gray
$frontendOk = Test-Endpoint "http://localhost:5173" "Frontend Root"

# Test 3: Proxy (Frontend -> Backend)
Write-Host "`n[3] Test Proxy (Frontend -> Backend)" -ForegroundColor Cyan
Write-Host "----------------------------------------" -ForegroundColor Gray
$proxyOk = Test-Endpoint "http://localhost:5173/api/health" "Proxy Health Check"
$proxyOk = Test-Endpoint "http://localhost:5173/api/villes" "Proxy Villes" -and $proxyOk

# Résumé
Write-Host "`n========================================================" -ForegroundColor Cyan
Write-Host "   Résumé" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

if ($backendOk) {
    Write-Host "✅ Backend accessible" -ForegroundColor Green
} else {
    Write-Host "❌ Backend NON accessible" -ForegroundColor Red
    Write-Host "   Démarrer avec: cd backend && uvicorn main:app --reload" -ForegroundColor Yellow
}

if ($frontendOk) {
    Write-Host "✅ Frontend accessible" -ForegroundColor Green
} else {
    Write-Host "❌ Frontend NON accessible" -ForegroundColor Red
    Write-Host "   Démarrer avec: cd frontend && npm run dev" -ForegroundColor Yellow
}

if ($proxyOk) {
    Write-Host "✅ Proxy fonctionne correctement" -ForegroundColor Green
    Write-Host "   Le frontend peut communiquer avec le backend !" -ForegroundColor Green
} else {
    Write-Host "❌ Proxy NE fonctionne PAS" -ForegroundColor Red
    Write-Host "   Vérifier:" -ForegroundColor Yellow
    Write-Host "   1. vite.config.js : proxy configuré ?" -ForegroundColor Yellow
    Write-Host "   2. VITE_BACKEND_URL définie ?" -ForegroundColor Yellow
    Write-Host "   3. Backend accessible depuis le frontend ?" -ForegroundColor Yellow
}

Write-Host ""

# Test Docker Compose si disponible
Write-Host "`n[4] Test Docker Compose (optionnel)" -ForegroundColor Cyan
Write-Host "----------------------------------------" -ForegroundColor Gray

$dockerRunning = docker-compose ps 2>$null
if ($LASTEXITCODE -eq 0 -and $dockerRunning) {
    Write-Host "Docker Compose détecté, test des variables..." -ForegroundColor Yellow
    
    # Vérifier les variables d'environnement
    Write-Host "`nVariables d'environnement Frontend:" -ForegroundColor Yellow
    docker-compose exec -T frontend printenv | Select-String "BACKEND|VITE" 2>$null
    
    Write-Host "`nTest depuis le conteneur frontend:" -ForegroundColor Yellow
    docker-compose exec -T frontend wget -qO- http://backend:8000/api/health 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Frontend peut joindre Backend via réseau Docker" -ForegroundColor Green
    } else {
        Write-Host "❌ Frontend ne peut pas joindre Backend" -ForegroundColor Red
    }
} else {
    Write-Host "Docker Compose non actif (OK si dev local)" -ForegroundColor Gray
}

Write-Host ""
Write-Host "========================================================" -ForegroundColor Cyan

