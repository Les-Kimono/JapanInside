import { useEffect, useState } from 'react';

function ArticleList() {
    const [articles, setArticles] = useState([]);

    useEffect(() => {
        fetch('http://localhost:8000/articles')
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