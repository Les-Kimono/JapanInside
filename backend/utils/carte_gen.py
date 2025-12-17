from typing import Dict, List

# Données des villes
villes_data = {
    "Tokyo": {
        "nom": "Tokyo",
        "latitude": 35.6762,
        "longitude": 139.6503,
        "description": "Capitale du Japon, mégapole vibrante et centre économique",
        "population": "~14 millions",
        "attractions": ["Tour de Tokyo", "Senso-ji", "Shibuya Crossing", "Palais Impérial"],
        "informations_supp": {
            "climat": "Subtropical humide",
            "meilleure_saison": "Printemps (mars-mai)",
            "specialites": "Sushi, Ramen, Tempura"
        }
    },
    "Hakone": {
        "nom": "Hakone",
        "latitude": 35.2324,
        "longitude": 139.1063,
        "description": "Station thermale dans les montagnes, vue sur le Mont Fuji",
        "population": "~13,000",
        "attractions": ["Lac Ashi", "Owakudani", "Musée en plein air", "Sources chaudes"],
        "informations_supp": {
            "climat": "Montagnard",
            "meilleure_saison": "Automne pour les couleurs",
            "specialites": "Œufs noirs (Kuro-tamago), Onsen"
        }
    },
    "Kyoto": {
        "nom": "Kyoto",
        "latitude": 35.0116,
        "longitude": 135.7681,
        "description": "Ancienne capitale impériale, cœur culturel du Japon",
        "population": "~1.5 million",
        "attractions": ["Fushimi Inari", "Kinkaku-ji", "Gion", "Kiyomizu-dera"],
        "informations_supp": {
            "climat": "Tempéré",
            "meilleure_saison": "Printemps (cerisiers) et Automne (érables)",
            "specialites": "Kaiseki, Matcha, Yatsuhashi"
        }
    },
    "Nara": {
        "nom": "Nara",
        "latitude": 34.6851,
        "longitude": 135.8048,
        "description": "Ancienne capitale, connue pour ses temples et ses daims",
        "population": "~350,000",
        "attractions": ["Todai-ji", "Parc de Nara", "Daibutsu", "Kasuga-taisha"],
        "informations_supp": {
            "climat": "Tempéré",
            "meilleure_saison": "Printemps",
            "specialites": "Kaki-no-hazushi (sushi au persimmon)"
        }
    },
    "Osaka": {
        "nom": "Osaka",
        "latitude": 34.6937,
        "longitude": 135.5023,
        "description": "Ville dynamique connue pour sa cuisine et son château",
        "population": "~2.7 millions",
        "attractions": ["Château d'Osaka", "Dotonbori", "Universal Studios", "Umeda Sky Building"],
        "informations_supp": {
            "climat": "Subtropical humide",
            "meilleure_saison": "Printemps et Automne",
            "specialites": "Takoyaki, Okonomiyaki, Kushikatsu"
        }
    },
    "Hiroshima": {
        "nom": "Hiroshima",
        "latitude": 34.3853,
        "longitude": 132.4553,
        "description": "Ville historique, symbole de paix et de reconstruction",
        "population": "~1.2 million",
        "attractions": ["Mémorial de la Paix", "Dôme de Genbaku", "Miyajima", "Château d'Hiroshima"],
        "informations_supp": {
            "climat": "Subtropical humide",
            "meilleure_saison": "Printemps",
            "specialites": "Okonomiyaki d'Hiroshima, Huîtres"
        }
    }
}

# Itinéraire
itineraire = ["Tokyo", "Hakone", "Kyoto", "Nara", "Osaka", "Hiroshima", "Tokyo"]

def generate_map_html() -> str:
    """Génère le HTML complet de la carte interactive"""
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Carte Interactive du Japon - Japan Inside</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body { 
            margin: 0; 
            padding: 0; 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, sans-serif;
            overflow: hidden;
        }
        
        #map { 
            height: 100vh; 
            width: 100vw; 
        }

        /* Panneau d'information */
        .info-panel {
            position: absolute;
            top: 20px;
            right: 20px;
            z-index: 1000;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.2);
            max-width: 350px;
            max-height: 80vh;
            overflow-y: auto;
            display: none;
            animation: slideIn 0.3s ease;
        }
        
        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }

        .info-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }
        
        .close-btn {
            cursor: pointer;
            font-size: 24px;
            color: #666;
            transition: color 0.3s;
        }
        
        .close-btn:hover {
            color: #ff4444;
        }
        
        .ville-details {
            line-height: 1.6;
        }
        
        .ville-details h3 {
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 1.5rem;
        }
        
        .ville-details p {
            color: #555;
            margin-bottom: 10px;
        }
        
        .attractions-list {
            margin: 15px 0;
            padding-left: 20px;
        }
        
        .attractions-list li {
            margin-bottom: 5px;
            color: #444;
        }
        
        .info-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            margin: 15px 0;
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
        }
        
        .info-item {
            font-size: 0.9rem;
        }
        
        .info-item strong {
            color: #333;
            display: block;
            margin-bottom: 3px;
        }
        
        .action-btn {
            display: block;
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 6px;
            font-weight: bold;
            cursor: pointer;
            margin-top: 15px;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        
        .action-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }

        /* Légende */
        .legende {
            position: absolute;
            bottom: 30px;
            left: 20px;
            z-index: 1000;
            background: rgba(255, 255, 255, 0.95);
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 3px 15px rgba(0,0,0,0.1);
            font-size: 13px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        .legende h4 {
            margin-bottom: 10px;
            color: #2c3e50;
            font-size: 14px;
        }
        
        .legende-item {
            display: flex;
            align-items: center;
            margin-bottom: 8px;
            color: #444;
        }
        
        .color-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 10px;
            border: 2px solid white;
            box-shadow: 0 0 3px rgba(0,0,0,0.3);
        }
        
        /* Titre */
        .map-title {
            position: absolute;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 1000;
            background: rgba(255, 255, 255, 0.95);
            padding: 15px 30px;
            border-radius: 10px;
            box-shadow: 0 3px 15px rgba(0,0,0,0.1);
            text-align: center;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        .map-title h1 {
            color: #2c3e50;
            font-size: 1.2rem;
            margin-bottom: 5px;
        }
        
        .map-title p {
            color: #666;
            font-size: 0.9rem;
        }
        
        /* Popups personnalisés */
        .leaflet-popup-content {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        
        .custom-popup {
            text-align: center;
        }
        
        .popup-title {
            color: #2c3e50;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .popup-etape {
            background: #667eea;
            color: white;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 0.8rem;
            display: inline-block;
            margin-top: 5px;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .info-panel {
                max-width: 90%;
                right: 5%;
                left: 5%;
            }
            
            .legende {
                bottom: 10px;
                left: 10px;
                right: 10px;
                font-size: 12px;
            }
            
            .map-title {
                width: 90%;
                padding: 10px;
                top: 10px;
            }
        }
    </style>
</head>
<body>

<!-- Titre de la carte -->
<div class="map-title">
    <h1>🇯🇵 Japan Inside - Itinéraire au Japon</h1>
    <p>Tokyo → Hakone → Kyoto → Nara → Osaka → Hiroshima → Tokyo</p>
</div>

<!-- Carte -->
<div id="map"></div>

<!-- Panneau d'information -->
<div id="infoPanel" class="info-panel">
    <div class="info-header">
        <h3 id="villeTitle"></h3>
        <span class="close-btn" onclick="closeInfoPanel()">×</span>
    </div>
    <div id="villeContent" class="ville-details"></div>
</div>

<!-- Légende -->
<div class="legende">
    <h4>📋 LÉGENDE DES VILLES</h4>
    <div class="legende-item">
        <div class="color-dot" style="background-color: #ff4444;"></div>
        <span>Tokyo (Départ/Arrivée)</span>
    </div>
    <div class="legende-item">
        <div class="color-dot" style="background-color: #4444ff;"></div>
        <span>Hakone (Étape 2)</span>
    </div>
    <div class="legende-item">
        <div class="color-dot" style="background-color: #44cc44;"></div>
        <span>Kyoto (Étape 3)</span>
    </div>
    <div class="legende-item">
        <div class="color-dot" style="background-color: #ffa500;"></div>
        <span>Nara (Étape 4)</span>
    </div>
    <div class="legende-item">
        <div class="color-dot" style="background-color: #aa44ff;"></div>
        <span>Osaka (Étape 5)</span>
    </div>
    <div class="legende-item">
        <div class="color-dot" style="background-color: #cc0000;"></div>
        <span>Hiroshima (Étape 6)</span>
    </div>
</div>

<script>
    // Initialisation de la carte centrée sur le Japon
    var map = L.map('map').setView([36.2048, 138.2529], 6);
    
    // Ajout des tuiles OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
        maxZoom: 12,
        minZoom: 5
    }).addTo(map);
    
    // Limiter la vue au Japon
    map.setMaxBounds([[30, 128], [46, 146]]);
    
    // Données des villes
    var villes = {
        "Tokyo": {
            lat: 35.6762, 
            lon: 139.6503, 
            color: "red", 
            etape: 1,
            icon: "🏙️"
        },
        "Hakone": {
            lat: 35.2324, 
            lon: 139.1063, 
            color: "blue", 
            etape: 2,
            icon: "🏔️"
        },
        "Kyoto": {
            lat: 35.0116, 
            lon: 135.7681, 
            color: "green", 
            etape: 3,
            icon: "🏯"
        },
        "Nara": {
            lat: 34.6851, 
            lon: 135.8048, 
            color: "orange", 
            etape: 4,
            icon: "🦌"
        },
        "Osaka": {
            lat: 34.6937, 
            lon: 135.5023, 
            color: "purple", 
            etape: 5,
            icon: "🏰"
        },
        "Hiroshima": {
            lat: 34.3853, 
            lon: 132.4553, 
            color: "darkred", 
            etape: 6,
            icon: "☮️"
        }
    };
    
    // Itinéraire
    var itineraire = ["Tokyo", "Hakone", "Kyoto", "Nara", "Osaka", "Hiroshima", "Tokyo"];
    
    // Fonction pour afficher les détails d'une ville
    function onVilleClick(nom) {
        // Appel à l'API backend
        fetch(`/api/villes/${nom}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Ville non trouvée');
                }
                return response.json();
            })
            .then(data => {
                // Mettre à jour le titre
                document.getElementById("villeTitle").textContent = `${data.nom} ${villes[nom].icon}`;
                
                // Construire le contenu
                let content = `
                    <p><strong>Description:</strong> ${data.description}</p>
                    <p><strong>Population:</strong> ${data.population}</p>
                    <p><strong>Étape ${villes[nom].etape} sur 6</strong></p>
                    
                    <div class="info-grid">
                        <div class="info-item">
                            <strong>📍 Coordonnées</strong>
                            ${data.latitude.toFixed(4)}°N, ${data.longitude.toFixed(4)}°E
                        </div>
                `;
                
                // Ajouter les informations supplémentaires si disponibles
                if (data.informations_supp) {
                    content += `
                        <div class="info-item">
                            <strong>🌤️ Climat</strong>
                            ${data.informations_supp.climat}
                        </div>
                        <div class="info-item">
                            <strong>🌸 Meilleure saison</strong>
                            ${data.informations_supp.meilleure_saison}
                        </div>
                        <div class="info-item">
                            <strong>🍜 Spécialités</strong>
                            ${data.informations_supp.specialites}
                        </div>
                    `;
                }
                
                content += `</div>`;
                
                // Ajouter les attractions
                content += `
                    <p><strong>🏛️ Attractions principales:</strong></p>
                    <ul class="attractions-list">
                        ${data.attractions.map(attr => `<li>${attr}</li>`).join('')}
                    </ul>
                    
                    <button class="action-btn" onclick="window.open('/ville/${nom.toLowerCase()}', '_blank')">
                        <i class="fas fa-external-link-alt"></i> Voir la page complète
                    </button>
                `;
                
                document.getElementById("villeContent").innerHTML = content;
                document.getElementById("infoPanel").style.display = "block";
                
                // Centrer la carte sur la ville
                map.setView([villes[nom].lat, villes[nom].lon], 10);
            })
            .catch(error => {
                document.getElementById("villeTitle").textContent = nom;
                document.getElementById("villeContent").innerHTML = `
                    <p>Impossible de charger les détails de la ville.</p>
                    <p>Erreur: ${error.message}</p>
                `;
                document.getElementById("infoPanel").style.display = "block";
            });
    }
    
    // Fermer le panneau d'information
    function closeInfoPanel() {
        document.getElementById("infoPanel").style.display = "none";
    }
    
    // Points pour l'itinéraire
    var points = [];
    
    // Créer les marqueurs pour chaque ville
    Object.keys(villes).forEach(ville => {
        var v = villes[ville];
        
        // Ajouter aux points pour l'itinéraire
        points.push([v.lat, v.lon]);
        
        // Créer une icône personnalisée
        var icon = L.icon({
            iconUrl: `https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-${v.color}.png`,
            shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
            iconSize: [30, 46],
            iconAnchor: [15, 46],
            popupAnchor: [0, -46]
        });
        
        // Créer le marqueur
        var marker = L.marker([v.lat, v.lon], { 
            icon: icon,
            title: ville 
        }).addTo(map);
        
        // Ajouter un popup
        marker.bindPopup(`
            <div class="custom-popup">
                <div class="popup-title">${ville} ${v.icon}</div>
                <div>Étape ${v.etape} du voyage</div>
                <div class="popup-etape">Cliquez pour plus d'infos</div>
            </div>
        `);
        
        // Ajouter l'événement de clic
        marker.on('click', function() {
            onVilleClick(ville);
        });
    });
    
    // Tracer l'itinéraire
    var polyline = L.polyline(points, {
        color: "#667eea",
        weight: 4,
        opacity: 0.8,
        dashArray: "10, 10",
        lineCap: 'round'
    }).addTo(map);
    
    // Ajouter des flèches directionnelles
    for (var i = 0; i < points.length - 1; i++) {
        var pointA = points[i];
        var pointB = points[i + 1];
        
        // Calculer le point milieu
        var midPoint = [
            (pointA[0] + pointB[0]) / 2,
            (pointA[1] + pointB[1]) / 2
        ];
        
        // Ajouter une flèche
        L.marker(midPoint, {
            icon: L.divIcon({
                html: '<i class="fas fa-arrow-right" style="color: #667eea; font-size: 18px; text-shadow: 0 0 3px white;"></i>',
                iconSize: [20, 20],
                className: 'arrow-icon'
            })
        }).addTo(map);
    }
    
    // Ajouter le contour approximatif du Japon
    var japonCoords = [
        [45.523, 141.934], [45.408, 148.153], [43.385, 146.922],
        [42.150, 143.256], [41.407, 141.456], [40.782, 140.203],
        [38.581, 139.543], [37.805, 138.904], [36.750, 137.203],
        [36.204, 133.325], [33.466, 129.975], [31.556, 130.557],
        [30.949, 131.391], [31.391, 132.413], [32.680, 133.005],
        [33.539, 135.772], [34.677, 137.609], [35.338, 139.022],
        [35.178, 140.042], [35.553, 140.856], [36.790, 140.753],
        [37.857, 140.985], [39.447, 142.013], [41.257, 141.352],
        [45.523, 141.934]
    ];
    
    L.polygon(japonCoords, {
        color: "#2c3e50",
        weight: 2,
        opacity: 0.3,
        fillOpacity: 0.05,
        fillColor: "#3498db"
    }).addTo(map);
    
    // Gérer le clic en dehors du panneau pour le fermer
    map.on('click', function() {
        closeInfoPanel();
    });
    
    // Permettre la communication avec la page parent
    window.addEventListener('message', function(event) {
        if (event.data.action === 'focusOnVille') {
            const ville = event.data.ville;
            if (villes[ville]) {
                onVilleClick(ville);
            }
        }
    });
</script>

</body>
</html>
"""

def generate_japan_map(output_path: str = None) -> str:
    """
    Génère la carte du Japon et la sauvegarde si un chemin est fourni
    Retourne le HTML généré
    """
    html_content = generate_map_html()

    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Carte sauvegardée à : {output_path}")

    return html_content

if __name__ == "__main__":
    # Test : générer et sauvegarder la carte
    generate_japan_map("carte_japon_test.html")
    print("Carte générée avec succès !")