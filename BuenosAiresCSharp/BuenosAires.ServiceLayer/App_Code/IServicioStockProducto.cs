﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.ServiceModel;
using System.ServiceModel.Web;
using System.Text;
using BuenosAires.Model;
using BuenosAires.BusinessLayer;

[ServiceContract]
public interface IServicioStockProducto
{
	[OperationContract]
	Respuesta ObtenerRespuesta(BcStockProducto bc);

	[OperationContract]
	Respuesta ValidarStockProducto(StockProducto stockProducto);

	[OperationContract]
	Respuesta Crear(StockProducto stockProducto);

	[OperationContract]
	Respuesta LeerTodos();

	[OperationContract]
	Respuesta Leer(int id);

	[OperationContract]
	Respuesta Actualizar(StockProducto stockProducto);

	[OperationContract]
	Respuesta Eliminar(int id);

	[OperationContract]
	Respuesta LeerTodosEnJson();

	[OperationContract]
	Respuesta ProductosLeerTodosEnJson();

	[OperationContract]
	Respuesta PerfilUsuarioLeerTodos();

	[OperationContract]
	Respuesta VerificarPassword(string cuenta, string password);

	/*[OperationContract]
	Respuesta ValidarLoginEscritorio(string cuenta, string password, string tipousu);*/

	[OperationContract]
	Respuesta ObtenerGuiasDespacho();
	[OperationContract]
	Respuesta ObtenerEquiposAnwo();
}