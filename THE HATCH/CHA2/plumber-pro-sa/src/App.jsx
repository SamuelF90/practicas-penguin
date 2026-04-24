import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import Navegacion from './componentes/Navegacion';
import Inicio from './paginas/Inicio';
import Registro from './paginas/Registro';
import Contacto from './paginas/Contacto';
import { profesionales as datosIniciales } from './datos/profesionales';

function App() {
  // 1. Cargamos desde LocalStorage o usamos los datos iniciales si está vacío
  const [listaProfesionales, setListaProfesionales] = useState(() => {
    const persistencia = localStorage.getItem('plumber_db');
    return persistencia ? JSON.parse(persistencia) : datosIniciales;
  });

  // 2. Guardamos en LocalStorage cada vez que la lista cambie
  useEffect(() => {
    localStorage.setItem('plumber_db', JSON.stringify(listaProfesionales));
  }, [listaProfesionales]);

  // 3. Función para agregar un nuevo profesional (se la pasamos a Registro)
  const agregarProfesional = (nuevoPro) => {
    setListaProfesionales([nuevoPro, ...listaProfesionales]);
  };

  return (
    <Router>
      <div className="min-h-screen bg-slate-50 font-sans antialiased text-slate-900 flex flex-col">
        <Navegacion />

        <div className="flex-grow">
          <Routes>
            {/* Pasamos la lista a Inicio */}
            <Route path="/" element={<Inicio profesionales={listaProfesionales} />} />
            
            {/* Pasamos la función de agregar a Registro */}
            <Route path="/registro" element={<Registro alAgregar={agregarProfesional} />} />

            <Route path="/contacto" element={<Contacto />} />
          </Routes>
        </div>

        <footer className="py-12 text-center text-slate-500 text-sm border-t border-slate-200 mt-20">
          <p className="font-semibold text-slate-600 uppercase tracking-wider">
            © 2026 Plumber Pro S.A. - Asunción
          </p>
          <p className="mt-2 text-slate-400">Hecho con ❤️ para el Challenge</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;