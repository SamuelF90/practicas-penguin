const express = require('express');
const mongoose = require('mongoose');
const jwt = require('jsonwebtoken');
const path = require('path');
const app = express();

const SECRET_KEY = "pinguino_secreto_paula"; 

// Conexión a la base de datos de los pingüinos
mongoose.connect('mongodb://localhost:27017/imperio_pinguino');

// Definición de Modelos (Aseguramos que coincidan con la DB de Go)
const Producto = mongoose.model('Producto', { 
    nombre: String, 
    precio: Number, 
    imagen: String 
}, 'productos');

const Pedido = mongoose.model('Pedido', { 
    producto: String, 
    total: Number, 
    iglu: String, 
    fecha: { type: Date, default: Date.now } 
}, 'pedidos');

app.set('view engine', 'pug');
app.set('views', path.join(__dirname, 'views')); 

app.use(express.urlencoded({ extended: true }));

// Middleware de seguridad
const verificarToken = (req, res, next) => {
    const token = req.query.token; 
    if (!token) return res.status(401).send("<h1>Acceso denegado: Paula necesita su token</h1>");
    try {
        const verificado = jwt.verify(token, SECRET_KEY);
        req.user = verificado;
        next();
    } catch (err) {
        res.status(400).send("Token inválido o expirado.");
    }
};

// --- RUTAS DE ACCESO ---

app.get('/login', (req, res) => { res.render('login'); });

app.post('/login', (req, res) => {
    if (req.body.password === 'paula123') {
        const token = jwt.sign({ user: 'paula' }, SECRET_KEY, { expiresIn: '1h' });
        res.redirect(`/escritorio?token=${token}`);
    } else {
        res.send('Contraseña incorrecta');
    }
});

app.get('/escritorio', verificarToken, async (req, res) => {
    const productos = await Producto.find();
    const pedidos = await Pedido.find().sort({ fecha: -1 });
    
    let editando = null;
    if (req.query.editarId) {
        editando = await Producto.findById(req.query.editarId);
    }

    res.render('escritorio', { 
        productos, 
        pedidos, 
        token: req.query.token,
        editando, 
        error: req.query.error,
        linkTienda: "http://localhost:8080" // Enviamos el link de Go a la plantilla
    });
});

// --- OPERACIONES CRUD ---

// GUARDAR (Crea si no hay ID, Actualiza si existe ID)
app.post('/productos/guardar', verificarToken, async (req, res) => {
    const { id, nombre, precio, link_imagenes } = req.body;
    const token = req.query.token;

    try {
        if (id) {
            // LÓGICA DE EDICIÓN
            await Producto.findByIdAndUpdate(id, { 
                nombre, 
                precio: parseInt(precio), 
                imagen: link_imagenes 
            });
        } else {
            // LÓGICA DE AGREGAR + PREVENIR DUPLICADOS
            const existe = await Producto.findOne({ nombre: { $regex: new RegExp("^" + nombre.trim() + "$", "i") } });
            if (existe) {
                return res.redirect(`/escritorio?token=${token}&error=duplicado`);
            }
            await Producto.create({ 
                nombre: nombre.trim(), 
                precio: parseInt(precio), 
                imagen: link_imagenes 
            });
        }
        res.redirect(`/escritorio?token=${token}`);
    } catch (err) {
        res.status(500).send("Error al procesar el producto");
    }
});

app.get('/productos/borrar/:id', verificarToken, async (req, res) => {
    await Producto.findByIdAndDelete(req.params.id);
    res.redirect(`/escritorio?token=${req.query.token}`);
});

app.get('/enviar_pedido/:id', verificarToken, async (req, res) => {
    await Pedido.findByIdAndDelete(req.params.id);
    res.redirect(`/escritorio?token=${req.query.token}`);
});

// --- INICIO DEL SERVIDOR ---

app.listen(3000, () => {
    console.log('\n' + '='.repeat(40));
    console.log('🚀 PANEL DE PAULA: http://localhost:3000/login');
    console.log('='.repeat(40) + '\n');
});