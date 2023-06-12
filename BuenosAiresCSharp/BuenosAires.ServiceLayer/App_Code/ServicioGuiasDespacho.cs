using BuenosAires.BusinessLayer;
using BuenosAires.Model;
using System;
using System.Net.Http;
using Newtonsoft.Json;
using System.Collections.Generic;

public class ServicioGuiasDespacho : IServicioGuiasDespacho
{
    public List<GuiaDespachoConEstado> ListaGuias = null;
    public Respuesta ObtenerGuiasDespacho()
    {
        var respuesta = new Respuesta();
        respuesta.Accion = "obtener guias de despacho";
        respuesta.Mensaje = "";
        respuesta.HayErrores = false;
        respuesta.ObtenerGuiasDespacho = "";
        string apiUrl = "http://127.0.0.1:8000/api/obtener_guias_de_despacho";

        try
        {
            using (HttpClient client = new HttpClient())
            {
                HttpResponseMessage response = client.GetAsync(apiUrl).Result;

                if (response.IsSuccessStatusCode)
                    respuesta.ObtenerGuiasDespacho = response.Content.ReadAsStringAsync().Result;
                else
                {
                    respuesta.Mensaje = "No fue posible " + respuesta.Accion;
                    respuesta.HayErrores = true;
                }
            }
        }
        catch (Exception ex)
        {
            respuesta.HayErrores = true;
            respuesta.Mensaje = Util.MensajeError("No fue posible " + respuesta.Accion, ex);
        }
        return respuesta;
    }
    public Respuesta ModificarEstadoGuiaDespacho(string nro, string estado)
    {
        var respuesta = new Respuesta();
        respuesta.Accion = "modificar estado de guia de despacho";
        respuesta.Mensaje = "";
        respuesta.HayErrores = false;
        respuesta.ModificarEstadoGuiaDespacho = "";
        string apiUrl = "http://127.0.0.1:8000/api/modificar_estado_guia_de_despacho/" + nro + "/" + estado;

        try
        {
            using (HttpClient client = new HttpClient())
            {
                HttpResponseMessage response = client.PutAsync(apiUrl, null).Result;

                if (response.IsSuccessStatusCode)
                    respuesta.ModificarEstadoGuiaDespacho = response.Content.ReadAsStringAsync().Result;
                else
                {
                    respuesta.Mensaje = "No fue posible " + respuesta.Accion;
                    respuesta.HayErrores = true;
                }
            }
        }
        catch (Exception ex)
        {
            respuesta.HayErrores = true;
            respuesta.Mensaje = Util.MensajeError("No fue posible " + respuesta.Accion, ex);
        }
        return respuesta;
    }

    public Respuesta Crear(GuiaDespachoConEstado guiaDespacho)
    {
        var respuesta = new Respuesta();
        return respuesta;
    }
}