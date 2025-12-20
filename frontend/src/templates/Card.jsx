
import { Link } from "react-router-dom";
const Card = ({ ville }) => {
    return (
        
   <div className="container">

            <div className="header">
                <h1>🇯🇵 {ville.nom}</h1>
                <p>{ville.description}</p>
            </div>
            
            <div className="content">
                <div className="info-section">
                    <h2>📊 Informations</h2>
                    <p><strong>Population:</strong> {ville.population}</p>
                    <p><strong>Coordonnées:</strong> {ville.latitude}°N, {ville.longitude}°E</p>
                    
                    
                    <div style={{"marginTop": "20px"}}>
                        <h3>🌤️ Climat & Spécialités</h3>
                        <p><strong>Climat:</strong> {ville.informations_supp.climat}</p>
                        <p><strong>Meilleure saison:</strong> {ville['informations_supp']['meilleure_saison']}</p>
                        <p><strong>Spécialités culinaires:</strong> {ville['informations_supp']['specialites']}</p>
                    </div>
                
                    <Link to="/" className="back-btn">← Retour à la carte</Link>
                </div>
                
                <div className="attractions-section">
                    <h2>🏛️ Attractions</h2>
                    <ul>
                       
                    </ul>
                    
                    <div className="map-container">
                        <iframe 
                            width="100%" 
                            height="100%" 
                            frameBorder="0" 
                            scrolling="no" 
                            marginHeight="0" 
                            marginWidth="0" 
                            src={`https://www.openstreetmap.org/export/embed.html?bbox=${ville.longitude-0.1},${ville.latitude-0.1},${ville.longitude+0.1},${ville.latitude+0.1}&layer=mapnik&marker=${ville.latitude},${ville.longitude}`}>
                        </iframe>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Card;