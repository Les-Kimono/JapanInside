import { useEffect, useRef } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "./mapStyle.css";

const Map = ({ villes, onVilleClick }) => {
  const mapRef = useRef(null);
useEffect(() => {
    document.body.style.overflow = "hidden";

    return () => {
      document.body.style.overflow = "scroll";
    };
  }, []);
  useEffect(() => {
    if (mapRef.current) return;

    const map = L.map("map").setView([36.2048, 138.2529], 6);
    mapRef.current = map;

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "© OpenStreetMap",
      maxZoom: 12,
      minZoom: 5,
    }).addTo(map);

    map.setMaxBounds([
      [30, 128],
      [46, 146],
    ]);
    map.on("click", () => onVilleClick(null));
  }, [onVilleClick]);

  useEffect(() => {
    if (!mapRef.current) return;

    // supprimer tous les marqueurs existants
    if (mapRef.current.markers) {
      mapRef.current.markers.forEach((m) => m.remove());
    }
    mapRef.current.markers = [];

    const points = [];

    villes.forEach((v) => {
      points.push([v.latitude, v.longitude]);

      const icon = L.icon({
        iconUrl:
            "https://cdn-icons-png.flaticon.com/512/684/684908.png",
        shadowUrl:
          "https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png",
        iconSize: [30, 30],
        iconAnchor: [15, 46],
        popupAnchor: [0, -46],
      });

      const marker = L.marker([v.latitude, v.longitude], { icon, title: v.nom }).addTo(mapRef.current);
      marker.on("click", () => onVilleClick(v.nom));
      marker.bindTooltip(`
     
        <b>${v.nom}</b>
        <div style="background-color: #6832a8;border-radius:15px;color:white;padding: 5px 10px 5px 10px;">
        Etape : ${v.position} / ${villes.length}
        </div>
    
        `, {
        permanent: true,    
        direction: "top",   
        className: "custom-tooltip" 
      });
      mapRef.current.markers.push(marker);
    });

    // tracer la polyline
    if (points.length) {
      if (mapRef.current.polyline) mapRef.current.polyline.remove();
      mapRef.current.polyline = L.polyline(points, {
        color: "#667eea",
        weight: 4,
        opacity: 0.8,
        dashArray: "10,10",
        lineCap: "round",
      }).addTo(mapRef.current);
    }
  }, [villes, onVilleClick]);

  return <div id="map" style={{ width: "100vw", height: "100vh", }}></div>;
};

export default Map;
