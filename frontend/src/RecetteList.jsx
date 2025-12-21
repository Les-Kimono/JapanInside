import { useEffect, useState } from 'react';

function RecetteList() {
    const [recettes, setRecettes] = useState([]);

    useEffect(() => {
         const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
    fetch(API_URL + '/api/recettes')
            .then(res => res.json())
            .then(data => setRecettes(data));
    }, []);

    return (
        <div>
            <h2>Recettes japonaises</h2>
            {recettes.map(r => (
                <div key={r.id}>
                    <h3>{r.nom}</h3>
                    <p>{r.description}</p>
                </div>
            ))}
        </div>
    );
}

export default RecetteList;