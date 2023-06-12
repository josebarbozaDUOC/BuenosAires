using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.ServiceModel;
using System.ServiceModel.Web;
using System.Text;
using BuenosAires.Model;
using BuenosAires.BusinessLayer;

[ServiceContract]
public interface IServicioGuiasDespacho
{
	[OperationContract]
	Respuesta ObtenerGuiasDespacho();
	[OperationContract]
	Respuesta ModificarEstadoGuiaDespacho(string nro, string estado);

	[OperationContract]
	Respuesta Crear(GuiaDespachoConEstado guiaDespacho);

}