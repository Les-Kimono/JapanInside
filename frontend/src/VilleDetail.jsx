import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import "./villeStyle.css"
import Card from "./templates/Card";
const VilleDetail = () => {
    const { villeP } = useParams();
    const [ville, setVille] = useState(null);


  useEffect(() => {
    fetch('/api/villes/' + villeP)
      .then(res => {
        if (!res.ok) throw new Error('Ville non trouvée');
        return res.json();
      })
      .then(data => {
        
        setVille(data);
      })
      .catch(err => {
  
        console.error(err);
      });
  }, [villeP]);
   if (!ville) return <p>Chargement...</p>;

   return  (

<Card ville={ville}/>
   
        )
}
export default VilleDetail;