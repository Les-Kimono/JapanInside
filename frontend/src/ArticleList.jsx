import { useEffect, useState } from 'react';
import axios from "axios";
function ArticleList() {
    const [articles, setArticles] = useState([]);
    const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
    axios.get(API_URL + '/api/hello').then((res) => {
        console.log(res.data.message)
    })
    useEffect(() => {
 const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
    fetch(API_URL + '/api/articles')
            .then(res => res.json())
            .then(data => setArticles(data));
    }, []);

    return (
        <div>
            <h2>Articles culturels</h2>
            {articles.map(a => (
                <div key={a.id}>
                    <h3>{a.titre}</h3>
                    <p>{a.contenu}</p>
                </div>
            ))}
        </div>
    );
}

export default ArticleList;