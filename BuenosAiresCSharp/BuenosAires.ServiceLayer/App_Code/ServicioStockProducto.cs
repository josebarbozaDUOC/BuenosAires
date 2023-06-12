using BuenosAires.BusinessLayer;
using BuenosAires.Model;
using System;
using System.Net.Http;

public class ServicioStockProducto : IServicioStockProducto
{
    public Respuesta ObtenerRespuesta(BcStockProducto bc)
    {
        var respuesta = new Respuesta();
        respuesta.Accion = bc.Accion;
        respuesta.Mensaje = bc.Mensaje;
        respuesta.HayErrores = bc.HayErrores;
        respuesta.XmlStockProducto = Util.SerializarXML(bc.StockProducto);
        respuesta.XmlListaStockProducto = Util.SerializarXML(bc.Lista);
        respuesta.XmlEquipoAnwo = Util.SerializarXML(bc.StockProducto);
        respuesta.XmlListaEquipoAnwo = Util.SerializarXML(bc.ListaEquiposAnwo);
        return respuesta;
    }

    public Respuesta ObtenerRespuestaPerfilusuario(BcPerfilUsuario bc)
    {
        var respuesta = new Respuesta();
        respuesta.Accion = bc.Accion;
        respuesta.Mensaje = bc.Mensaje;
        respuesta.HayErrores = bc.HayErrores;
        respuesta.XmlPerfilUsuario = Util.SerializarXML(bc.PerfilUsuario);
        respuesta.XmlListaPerfilUsuario = Util.SerializarXML(bc.PerfilUsuario);
        return respuesta;
    }

    public Respuesta ValidarStockProducto(StockProducto stockProducto)
    {
        var bc = new BcStockProducto();
        bc.ValidarStockProducto(stockProducto);
        return ObtenerRespuesta(bc);
    }

    public Respuesta Crear(StockProducto stockProducto)
    {
        var bc = new BcStockProducto();
        bc.Crear(stockProducto);
        return ObtenerRespuesta(bc);
    }

    public Respuesta LeerTodos()
    {
        var bc = new BcStockProducto();
        bc.LeerTodos();
        return ObtenerRespuesta(bc);
    }

    public Respuesta Leer(int id)
    {
        var bc = new BcStockProducto();
        bc.Leer(id);
        return ObtenerRespuesta(bc);
    }

    public Respuesta Actualizar(StockProducto stockProducto)
    {
        var bc = new BcStockProducto();
        bc.Actualizar(stockProducto);
        return ObtenerRespuesta(bc);
    }

    public Respuesta Eliminar(int id)
    {
        var bc = new BcStockProducto();
        bc.Eliminar(id);
        return ObtenerRespuesta(bc);
    }

    public Respuesta LeerTodosEnJson()
    {
        var respuesta = new Respuesta();
        respuesta.Accion = "obtener lista de productos";
        respuesta.Mensaje = "";
        respuesta.HayErrores = false;
        respuesta.JsonProducto = "";
        respuesta.JsonListaProducto = "";

        string apiUrl = "http://127.0.0.1:8000/api/obtener_equipos_en_bodega";

        try
        {
            using (HttpClient client = new HttpClient())
            {
                HttpResponseMessage response = client.GetAsync(apiUrl).Result;

                if (response.IsSuccessStatusCode)
                {
                    respuesta.JsonListaProducto = response.Content.ReadAsStringAsync().Result; // Leer la respuesta como cadena JSON
                }
                else
                {
                    respuesta.Mensaje = "No fue posible " + respuesta.Accion;
                    respuesta.HayErrores = true;
                }
            }
        }
        catch(Exception ex)
        {
            respuesta.HayErrores = true;
            respuesta.Mensaje = Util.MensajeError("No fue posible " + respuesta.Accion, ex);
        }

        return respuesta;
    }

    public Respuesta ProductosLeerTodosEnJson()
    {
        var respuesta = new Respuesta();
        respuesta.Accion = "obtener lista de productos";
        respuesta.Mensaje = "";
        respuesta.HayErrores = false;
        respuesta.JsonProducto = "";
        respuesta.JsonListaProducto = "";

        string apiUrl = "http://127.0.0.1:8000/api/obtener_productos";

        try
        {
            using (HttpClient client = new HttpClient())
            {
                HttpResponseMessage response = client.GetAsync(apiUrl).Result;

                if (response.IsSuccessStatusCode)
                {
                    respuesta.JsonListaProducto = response.Content.ReadAsStringAsync().Result; // Leer la respuesta como cadena JSON
                }
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

    //métodos api
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

    public Respuesta ObtenerEquiposAnwo()
    {
        var bc = new BcStockProducto();
        bc.ObtenerEquiposAnwo();
        return ObtenerRespuesta(bc);
    }
    public Respuesta ReservarEquipoAnwo(string nroserie)
    {
        var bc = new BcStockProducto();
        bc.ReservarEquipoAnwo(nroserie);
        return ObtenerRespuesta(bc);
    }

}