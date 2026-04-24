import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function Registro({ alAgregar }) {
  const navigate = useNavigate();

  const [nombre, setNombre] = useState("");
  const [rubro, setRubro] = useState("Plomería");
  const [telefono, setTelefono] = useState("");
  const [ubicacion, setUbicacion] = useState("");
  const [descripcion, setDescripcion] = useState("");


  const manejarEnvio = (e) => {
    e.preventDefault();

    const nuevoProfesional = {
      id: Date.now(),
      nombre: nombre,
      rubro: rubro,
      telefono: telefono,
      ubicacion: ciudad + " - " ,
      descripcion: descripcion,
      puntuacion: 5.0,
      imagen: "https://images.unsplash.com/photo-1621905251189-08b45d6a269e?q=80&w=400&h=400&fit=crop"
    };

    alAgregar(nuevoProfesional);
    alert("✅ ¡Registro exitoso! Ya apareces en el directorio con tu descripción.");
    navigate("/");
  };

  return (
    <div className="max-w-2xl mx-auto py-16 px-4 flex-grow">
      <div className="bg-white p-10 rounded-3xl shadow-2xl border border-slate-100">
        
        <h2 className="text-3xl font-black text-slate-900 mb-2">Unite al equipo 🛠️</h2>
        <p className="text-slate-500 mb-10 font-medium">
          Completá tus datos para que los clientes sepan qué problemas podés resolver.
        </p>

        <form className="space-y-6" onSubmit={manejarEnvio}>
          
          {/* Fila 1: Nombre y Rubro */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-bold text-slate-700 mb-2 ml-1">Nombre Completo</label>
              <input required type="text" value={nombre} onChange={(e) => setNombre(e.target.value)} className="w-full p-4 rounded-2xl border-2 border-slate-100 focus:border-acento-pro outline-none transition-all" placeholder="Ej: Juan Pérez" />
            </div>
            <div>
              <label className="block text-sm font-bold text-slate-700 mb-2 ml-1">Rubros</label>
              <select value={rubro} onChange={(e) => setRubro(e.target.value)} className="w-full p-4 rounded-2xl border-2 border-slate-100 focus:border-acento-pro outline-none transition-all bg-white cursor-pointer appearance-none">
                <option value="Plomeria">Plomeria</option>
                <option value="Electricidad">Electricidad</option>
                <option value="Refrigeracion">Refrigeracion</option>
                <option value="Construccion">Construccion</option>
              </select>
            </div>
          </div>

          {/* Fila 2: WhatsApp y Barrio/Dirección */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-bold text-slate-700 mb-2 ml-1">WhatsApp</label>
              <input required type="text" value={telefono} onChange={(e) => setTelefono(e.target.value)} className="w-full p-4 rounded-2xl border-2 border-slate-100 focus:border-acento-pro outline-none transition-all" placeholder="+595 9xx..." />
            </div>
            <div>
              <label className="block text-sm font-bold text-slate-700 mb-2 ml-1">Barrio / Dirección</label>
              <input required type="text" value={ubicacion} onChange={(e) => setUbicacion(e.target.value)} className="w-full p-4 rounded-2xl border-2 border-slate-100 focus:border-acento-pro outline-none transition-all" placeholder="Ej: Villa Morra" />
            </div>
          </div>

          
          {/* Fila 4: Descripción (Sola abajo y ancha) */}
          <div className="w-full">
            <label className="block text-sm font-bold text-slate-700 mb-2 ml-1">Descripción de tus servicios</label>
            <textarea
              required
              value={descripcion}
              onChange={(e) => setDescripcion(e.target.value)}
              placeholder="Contanos tu experiencia, si hacés urgencias 24hs, etc."
              rows="4"
              className="w-full p-4 rounded-2xl border-2 border-slate-100 focus:border-acento-pro outline-none resize-none transition-all"
            ></textarea>
          </div>

          <button type="submit" className="w-full bg-azul-pro hover:bg-slate-800 text-white font-black py-4 rounded-2xl shadow-xl transition-all active:scale-95">
            Confirmar Registro
          </button>
        </form>
      </div>
    </div>
  );
}

