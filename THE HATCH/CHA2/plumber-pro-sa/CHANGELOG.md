# CHANGELOG - Plumber Pro S.A.

## [1.0.0] - 2026-02-13
### Added
- **Estructura Multipágina:** Implementación de `react-router-dom` con 3 rutas principales: Inicio, Registro y Contacto.
- **Navegación SPA:** Transiciones instantáneas con componentes `Link` para evitar el "parpadeo" de carga.
- **Identidad Visual:** Sistema de colores personalizado (`azul-pro`, `acento-pro`) y tipografía moderna (`font-sans`).

### 🧪 User Testing Updates (Pruebas de Usuario)
- **Prueba 1 (Navegación):** Los usuarios reportaron que al hacer scroll perdián el buscador. **Cambio:** Se implementó `Navegacion.jsx` con diseño **Sticky** (siempre visible).
- **Prueba 2 (Interacción):** En móviles, los usuarios no sabían si el clic en la tarjeta funcionaba. **Cambio:** Se agregó un **Efecto de Presión (Feedback Táctil)** en `Tarjeta.jsx`.
- **Prueba 3 (Accesibilidad):** Se detectó que el texto negro puro sobre blanco cansaba la vista en sesiones largas. **Cambio:** Se ajustó el fondo a `bg-slate-50` y el texto a `text-slate-900` (Azul Oxford).
- **Prueba 4 (Funcionalidad):** Los usuarios pedían una forma más rápida de contactar sin escribir. **Cambio:** Se añadió el **Enlace Directo para llamadas** (`tel:`) en cada tarjeta.
- **Prueba 5 (Estructura):** Usuarios de prueba se confundían con términos en inglés en la URL. **Cambio:** Se refactorizaron las rutas y carpetas al **español** para mejorar la claridad local.

### Fixed
- Error 404 en `localhost:5173` corrigiendo la ruta del script en `index.html`.
- Problemas de renderizado de Tailwind inyectando las directivas en `index.css`.
- Configuración de `_redirects` para evitar errores 404 en el despliegue de Netlify.

---

## [0.0.3] - 2026-02-13
### Added
- Creación de base de datos estática en `profesionales.js` con barrios de Asunción.
- Diseño responsivo de tarjetas (Grid System).

## [0.0.1] - 2026-02-13
### Added
- Inicialización del proyecto con Vite y React.
- Definición de la arquitectura inicial y paleta de colores.