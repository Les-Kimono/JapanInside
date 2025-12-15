import { useEffect, useState } from 'react';

function RecetteList() {
    const [recettes, setRecettes] = useState([]);

    useEffect(() => {
        fetch('http://localhost:8000/recettes')
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