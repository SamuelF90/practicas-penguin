🐧 Operación Microservicios - Los Pingüinos del MonolitoEste proyecto consiste en la descomposición de un sistema monolítico ("EL MAMUT") en una arquitectura basada en microservicios independientes, modulares y escalables desarrollada con FastAPI y SQLite.  🏗️ Arquitectura del SistemaEl sistema está dividido en 4 microservicios con responsabilidades bien definidas y sus propias bases de datos aisladas:  Servicio de Autenticación (autenticacion.py): Emite y valida tokens JWT para autorizar las solicitudes entre servicios y clientes.  Servicio de Productos (productos.py): Gestiona la creación y el catálogo de productos (productos.db).  Servicio de Inventario (inventario.py): Controla la disponibilidad y disminución de stock por producto (inventario.db).  Servicio de Pedidos (pedidos.py): Coordina la creación de pedidos consumiendo la API de productos e inventario mediante tokens de servicio (pedidos.db).  🛠️ Requisitos e InstalaciónClonar el repositorio:Bashgit clone https://github.com/SamuelF90/practicas-penguin.git
cd "THE HUDDLE/CHA 6"
Instalar dependencias:Bashpip install fastapi uvicorn PyJWT requests pydantic
🚀 Ejecución de los MicroserviciosPara probar el flujo completo, ejecutá cada microservicio en una terminal independiente asignándole su correspondiente puerto:Bash# Terminal 1 - Autenticación
uvicorn autenticacion:app --port 8000 --reload

# Terminal 2 - Productos
uvicorn productos:app --port 8001 --reload

# Terminal 3 - Inventario
uvicorn inventario:app --port 8002 --reload

# Terminal 4 - Pedidos
uvicorn pedidos:app --port 8003 --reload
🔒 Autenticación y Flujo de ComunicaciónObtener Token de Servicio: Se realiza una petición POST /token al servicio de autenticación con el secreto configurado.  Consultar/Modificar Recurso: Cada petición hacia los endpoints protegidos requiere la cabecera Authorization: Bearer <token>.  Creación de Pedido: El servicio de pedidos solicita su propio token de servicio y valida el catálogo y el stock antes de registrar la transacción.