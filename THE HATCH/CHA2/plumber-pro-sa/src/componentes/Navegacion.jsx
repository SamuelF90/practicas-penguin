import React, { useState } from 'react'; 
import { Link, useLocation } from 'react-router-dom';
import logoPng from '../assets/logo.png';

export default function Navegacion() {
  const location = useLocation();
  const [menuAbierto, setMenuAbierto] = useState(false);

  // Diccionario para el título dinámico
  const nombresRutas = {
    '/': 'Directorio',
    '/registro': 'Unite al Equipo',
    '/contacto': 'Contacto'
  };

  const paginaActual = nombresRutas[location.pathname] || 'Directorio';

  // Función para resaltar el link activo en PC
  const esActivo = (ruta) => location.pathname === ruta ? "text-acento-pro font-black" : "hover:text-acento-pro";

  return (
    <nav className="bg-azul-pro text-white p-4 shadow-md sticky top-0 z-50">
      <div className="max-w-6xl mx-auto">
        
        {/* FILA PRINCIPAL: Logo, Hamburguesa y Menú PC */}
        <div className="flex justify-between items-center">
          
          {/* LOGO */}
          <Link to="/" className="text-xl font-extrabold tracking-tighter hover:opacity-90 transition flex items-center gap-2 z-50">
             PLUMBER PRO <span className="text-acento-pro">S.A.</span>  
          </Link>

          {/* BOTÓN HAMBURGUESA (Solo se ve en móvil) */}
          <button 
            onClick={() => setMenuAbierto(!menuAbierto)}
            className="md:hidden p-2 z-50 focus:outline-none"
          >
            <div className="space-y-1.5">
              <span className="block w-6 h-0.5 bg-white"></span>
              <span className="block w-6 h-0.5 bg-white"></span>
              <span className="block w-6 h-0.5 bg-white"></span>
            </div>
          </button>

          {/* MENÚ DE NAVEGACIÓN (PC) */}
          <div className="hidden md:flex items-center space-x-6 text-xs font-black uppercase">
            <Link to="/" className={`${esActivo('/')} transition-colors`}>Directorio</Link>
            <Link to="/contacto" className={`${esActivo('/contacto')} transition-colors`}>Contacto</Link>
            <Link to="/registro" className="bg-acento-pro text-azul-pro px-5 py-2.5 rounded-xl shadow-lg hover:bg-white transition-all">
               Unirse al equipo
            </Link>
          </div>
        </div>

        {/* --- TÍTULO DINÁMICO (VISIBLE EN PC Y CELULAR) --- */}
        {/* Le quité el 'md:hidden' para que salga siempre */}
        <div className="mt-3 text-center border-t border-white/10 pt-2">
           <p className="text-[11px] font-bold uppercase tracking-[0.2em] text-acento-pro">
             Estas en: {paginaActual}
           </p>
        </div>
      </div>

      {/* MENÚ MÓVIL FULLSCREEN */}
      <div className={`
        fixed inset-0 bg-azul-pro flex flex-col items-center justify-center space-y-8 text-2xl transition-transform duration-300 ease-in-out
        ${menuAbierto ? 'translate-x-0' : 'translate-x-full'}
        md:hidden z-40
      `}>
        <Link to="/" onClick={() => setMenuAbierto(false)} className={esActivo('/')}>Directorio</Link>
        <Link to="/contacto" onClick={() => setMenuAbierto(false)} className={esActivo('/contacto')}>Contacto</Link>
        <Link to="/registro" onClick={() => setMenuAbierto(false)} className="bg-acento-pro text-azul-pro px-10 py-5 rounded-2xl font-black">
          Unirse al equipo
        </Link>
      </div>
    </nav>
  );
}