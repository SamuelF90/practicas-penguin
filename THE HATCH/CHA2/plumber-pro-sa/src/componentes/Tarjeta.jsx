import React from 'react';

export default function Tarjeta({ profesional }) {
  // Limpiamos el número de teléfono para el enlace de WhatsApp
  const numTelefono = profesional.telefono ? profesional.telefono.replace(/\D/g, '') : '';
  const mensajeWA = encodeURIComponent(`Hola ${profesional.nombre}, te vi en Plumber Pro y necesito una consulta.`);

  return (
    <div className="bg-white rounded-3xl shadow-md border border-slate-100 p-6 hover:shadow-xl transition-all flex flex-col justify-between">
      <div>
        <div className="flex justify-between items-start mb-4">
          <span className="bg-blue-50 text-azul-pro text-[10px] font-black px-3 py-1 rounded-lg uppercase tracking-wider border border-blue-100">
            {profesional.rubro}
          </span>
          <div className="bg-yellow-50 text-yellow-700 text-xs font-bold px-2 py-1 rounded-lg flex items-center gap-1">
            {profesional.puntuacion || "5"} <span className="text-yellow-500">★</span>
          </div>
        </div>

        <h3 className="text-xl font-extrabold text-slate-900 mb-2 leading-tight">
          {profesional.nombre}
        </h3>
        
        <p className="text-slate-400 text-sm mb-4 flex items-center gap-1">
          <span className="text-base">📍</span> {profesional.ubicacion || "Asunción, Paraguay"}
        </p>

        {profesional.descripcion && (
          <p className="text-slate-600 text-sm mb-6 line-clamp-2 leading-relaxed">
            {profesional.descripcion}
          </p>
        )}
      </div>

      {/* BOTÓN AZUL CON ICONO VERDE DE WHATSAPP */}
      <a 
        href={`https://wa.me/${numTelefono}?text=${mensajeWA}`}
        target="_blank"
        rel="noopener noreferrer"
        className="flex items-center justify-center gap-3 bg-azul-pro hover:bg-slate-800 text-white font-black py-4 rounded-2xl transition-all shadow-lg shadow-blue-900/10 active:scale-95"
      >
        {/* Icono SVG con el color verde oficial de WhatsApp */}
        <svg 
          xmlns="http://www.w3.org/2000/svg" 
          width="20" 
          height="20" 
          fill="#25D366" 
          viewBox="0 0 16 16"
        >
          <path d="M13.601 2.326A7.854 7.854 0 0 0 7.994 0C3.627 0 .068 3.558.064 7.926c0 1.399.366 2.76 1.06 3.973L0 16l4.104-1.076a7.859 7.859 0 0 0 3.886 1.035h.005c4.367 0 7.926-3.558 7.93-7.93a7.86 7.86 0 0 0-2.324-5.703zM7.994 14.52a6.573 6.573 0 0 1-3.356-.92l-.24-.144-2.494.654.666-2.433-.156-.251a6.56 6.56 0 0 1-1.007-3.505c0-3.626 2.957-6.584 6.591-6.584a6.56 6.56 0 0 1 4.66 1.931 6.557 6.557 0 0 1 1.928 4.66c-.004 3.639-2.961 6.592-6.592 6.592zm3.615-4.934c-.197-.099-1.17-.578-1.353-.646-.182-.065-.315-.099-.445.099-.133.197-.513.646-.627.775-.114.133-.232.148-.43.05-.197-.1-.836-.308-1.592-.985-.59-.525-.985-1.175-1.103-1.372-.114-.198-.011-.304.088-.403.087-.088.197-.232.296-.346.1-.114.133-.198.198-.33.065-.134.034-.248-.015-.347-.05-.099-.445-1.076-.612-1.47-.16-.389-.323-.335-.445-.34-.114-.007-.247-.007-.38-.007a.729.729 0 0 0-.529.247c-.182.198-.691.677-.691 1.654 0 .977.71 1.916.81 2.049.098.133 1.394 2.132 3.383 2.992.47.205.84.326 1.129.418.475.152.904.129 1.246.08.38-.058 1.171-.48 1.338-.943.164-.464.164-.86.114-.943-.049-.084-.182-.133-.38-.232z"/>
        </svg>
        Contactar por WhatsApp
      </a>
    </div>
  );
}