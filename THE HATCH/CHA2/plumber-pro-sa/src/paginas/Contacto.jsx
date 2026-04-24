import React from 'react';

export default function Contacto() {
  // 1. Esta función maneja el envío
  const manejarEnvioContacto = (e) => {
    e.preventDefault(); // Evita que la página se refresque
    alert("📧 ¡Mensaje enviado con éxito! Nos pondremos en contacto contigo pronto.");
    
    // Opcional: Limpiar el formulario después del envío
    e.target.reset();
  };

  return (
    <div className="max-w-4xl mx-auto py-16 px-4 flex-grow">
      <div className="text-center mb-12">
        <h2 className="text-4xl font-black text-slate-900 mb-4 tracking-tight">¡Contactanos! 📞</h2>
        <p className="text-slate-600 text-lg font-medium">Estamos en Asunción para ayudarte con cualquier duda.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Información de contacto */}
        <div className="bg-azul-pro text-white p-10 rounded-3xl shadow-2xl flex flex-col justify-center">
          <h3 className="text-2xl font-black mb-8 border-b border-white/20 pb-4">Información de la Empresa</h3>
          <ul className="space-y-8">
            <li className="flex items-center gap-5">
              <span className="bg-white/10 p-3 rounded-2xl text-2xl">📍</span>
              <span className="font-medium">Av. Mariscal López, Asunción</span>
            </li>
            <li className="flex items-center gap-5">
              <span className="bg-white/10 p-3 rounded-2xl text-2xl">📱</span>
              <span className="font-medium">+595 981 123 456</span>
            </li>
            <li className="flex items-center gap-5">
              <span className="bg-white/10 p-3 rounded-2xl text-2xl">✉️</span>
              <span className="font-medium">hola@plumberpro.com.py</span>
            </li>
          </ul>
        </div>

        {/* Formulario rápido */}
        <div className="bg-white p-10 rounded-3xl shadow-2xl border border-slate-100">
          {/* 2. Conectamos la función al onSubmit */}
          <form className="space-y-5" onSubmit={manejarEnvioContacto}>
            <div>
              <label className="block text-sm font-bold text-slate-700 mb-2 ml-1">Tu nombre</label>
              <input 
                required 
                type="text" 
                placeholder="Ej: Juan González" 
                className="w-full p-4 rounded-2xl border-2 border-slate-100 focus:border-acento-pro outline-none transition-all placeholder:opacity-30" 
              />
            </div>

            <div>
              <label className="block text-sm font-bold text-slate-700 mb-2 ml-1">¿En qué podemos ayudarte?</label>
              <textarea 
                required 
                placeholder="Escribí tu consulta aquí..." 
                rows="4" 
                className="w-full p-4 rounded-2xl border-2 border-slate-100 focus:border-acento-pro outline-none resize-none transition-all placeholder:opacity-30"
              ></textarea>
            </div>

            {/* 3. El botón ahora es type="submit" */}
            <button 
              type="submit" 
              className="w-full bg-acento-pro text-white font-black py-4 rounded-2xl hover:bg-blue-500 hover:scale-[1.02] transition-all shadow-xl shadow-blue-500/20 active:scale-95 mt-2"
            >
              Enviar Mensaje
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}