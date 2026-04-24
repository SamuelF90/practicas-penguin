import React, { useState } from 'react';
import Tarjeta from '../componentes/Tarjeta';

// Ahora recibe "profesionales" desde las props
export default function Inicio({ profesionales }) {
  const [busqueda, setBusqueda] = useState("");

  // Filtramos sobre la lista que viene por props
  const profesionalesFiltrados = profesionales.filter((pro) =>
    pro.nombre.toLowerCase().includes(busqueda.toLowerCase()) ||
    pro.rubro.toLowerCase().includes(busqueda.toLowerCase())
  );

  return (
    <main className="max-w-6xl mx-auto px-4 py-12 flex-grow">
      <header className="mb-12 text-center">
        <h2 className="text-4xl md:text-5xl font-black text-slate-900 mb-4 tracking-tight">
          Héroes de Asunción 🛠️
        </h2>
        <p className="text-slate-600 text-lg max-w-xl mx-auto mb-10 leading-relaxed">
          Encontrá profesionales de confianza que sí responden y cuidan tu hogar.
        </p>

        <div className="max-w-md mx-auto relative group">
          <input 
            type="text"
            placeholder="Buscá por rubro (ej. Plomería)..."
            className="w-full p-5 pl-14 rounded-3xl border-2 border-slate-200 focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10 outline-none transition-all shadow-sm group-hover:border-slate-300"
            value={busqueda}
            onChange={(e) => setBusqueda(e.target.value)}
          />
          <span className="absolute left-5 top-5 text-xl opacity-40">🔍</span>
        </div>
      </header>

      {profesionalesFiltrados.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {profesionalesFiltrados.map((pro) => (
            <Tarjeta key={pro.id} profesional={pro} />
          ))}
        </div>
      ) : (
        <div className="text-center py-24 bg-white rounded-3xl border-2 border-dashed border-slate-200">
          <p className="text-slate-400 text-xl font-medium">
            No hay rastros de ese profesional... 
            <br />
            <span className="text-sm font-normal italic">
              Probá con "Plomería", "Electricidad" o "Refrigeración".
            </span>
          </p>
        </div>
      )}
    </main>
  );
}