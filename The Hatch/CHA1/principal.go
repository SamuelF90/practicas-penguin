package main

import (
	"context"
	"fmt"
	"html/template"
	"log"
	"net/http"
	"strconv"
	"strings" // <--- NUEVO: Necesario para procesar varios productos
	"time"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

type Producto struct {
	ID     primitive.ObjectID `bson:"_id,omitempty"`
	Nombre string             `bson:"nombre"`
	Precio int                `bson:"precio"`
	Imagen string             `bson:"imagen"`
}

type Pedido struct {
	ID       primitive.ObjectID `bson:"_id,omitempty"`
	Producto string             `bson:"producto"`
	Total    int                `bson:"total"`
	Iglu     string             `bson:"iglu"`
	Fecha    time.Time          `bson:"fecha"`
}

var cliente *mongo.Client

func main() {
	ctx, _ := context.WithTimeout(context.Background(), 10*time.Second)
	var err error
	cliente, err = mongo.Connect(ctx, options.Client().ApplyURI("mongodb://localhost:27017"))
	if err != nil {
		log.Fatal(err)
	}

	http.Handle("/imagenes/", http.StripPrefix("/imagenes/", http.FileServer(http.Dir("./imagenes"))))

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		col := cliente.Database("imperio_pinguino").Collection("productos")
		cursor, _ := col.Find(context.Background(), bson.D{})
		var prods []Producto
		cursor.All(context.Background(), &prods)
		tmpl, _ := template.ParseFiles("plantillas/tienda.html")
		tmpl.Execute(w, prods)
	})

	http.HandleFunc("/comprar", func(w http.ResponseWriter, r *http.Request) {
		if r.Method == http.MethodPost {
			r.ParseForm()
			iglu := r.FormValue("direccion_iglu")
			totalVenta := 0
			resumenProductos := ""

			// Revisamos todos los campos enviados
			for key, values := range r.PostForm {
				if strings.HasPrefix(key, "cant_") {
					cantidad, _ := strconv.Atoi(values[0])
					if cantidad > 0 {
						// Extraemos nombre y precio del nombre del input (cant_Sardina_100)
						partes := strings.Split(key, "_")
						nombre := partes[1]
						precio, _ := strconv.Atoi(partes[2])

						totalVenta += (precio * cantidad)
						resumenProductos += fmt.Sprintf("%s (x%d) ", nombre, cantidad)
					}
				}
			}

			if totalVenta > 0 {
				col := cliente.Database("imperio_pinguino").Collection("pedidos")
				col.InsertOne(context.Background(), Pedido{
					Producto: resumenProductos,
					Total:    totalVenta,
					Iglu:     iglu,
					Fecha:    time.Now(),
				})
			}

			w.Header().Set("Content-Type", "text/html; charset=utf-8")
			fmt.Fprintf(w, `
				<!DOCTYPE html>
				<html>
				<head>
					<meta charset="UTF-8">
					<style>
						body { background: radial-gradient(circle at center, #1a3a5f 0%%, #001524 100%%) no-repeat center center fixed; color: #e0f7fa; font-family: 'Segoe UI', sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
						.card { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px); padding: 40px; border-radius: 30px; border: 1px solid #00d2ff; text-align: center; box-shadow: 0 0 30px rgba(0, 210, 255, 0.2); }
						h1 { color: #00d2ff; }
						.total { font-size: 2em; color: #ffffff; margin: 20px 0; }
						.btn { display: inline-block; margin-top: 20px; color: #001524; text-decoration: none; background: #00d2ff; padding: 12px 25px; border-radius: 10px; font-weight: bold; }
					</style>
				</head>
				<body>
					<div class="card">
						<h1>❄️ ¡PEDIDO RECIBIDO!</h1>
						<p>Llevas: <b>%s</b></p>
						<div class="total">TOTAL: %d $</div>
						<p>Destino: <b>Iglú %s</b></p>
						<a href="/" class="btn">VOLVER A LA TIENDA</a>
					</div>
				</body>
				</html>`, resumenProductos, totalVenta, iglu)
		}
	})

	fmt.Println("\n🚀 SISTEMA MULTI-COMPRA: http://localhost:8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
