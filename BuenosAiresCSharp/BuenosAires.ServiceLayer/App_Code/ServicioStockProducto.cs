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

    public Respuesta VerificarPassword(string username, string password)
    {
        var respuesta = new Respuesta();
        respuesta.Accion = "verificar password";
        respuesta.Mensaje = "";
        respuesta.HayErrores = false;
        respuesta.JsonVerificarPassword = "";

        string apiUrl = "http://127.0.0.1:8000/api/verificar_password/" + username + "/" + password;

        try
        {
            using (HttpClient client = new HttpClient())
            {
                HttpResponseMessage response = client.GetAsync(apiUrl).Result;

                if (response.IsSuccessStatusCode)
                {
                    respuesta.JsonVerificarPassword = response.Content.ReadAsStringAsync().Result; // Leer la respuesta como cadena JSON
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

    /*public Respuesta ValidarLoginEscritorio(string username, string password, string tipousu)
    {
        var respuesta = new Respuesta();
        respuesta.Accion = "Validar Login Escritorio";
        respuesta.Mensaje = "";
        respuesta.HayErrores = false;
        respuesta.JsonValidarLoginEscritorio = "";

        string apiUrl = "http://127.0.0.1:8000/api/validar_login_escritorio/" + username + "/" + password + "/" + tipousu;

        try
        {
            using (HttpClient client = new HttpClient())
            {
                HttpResponseMessage response = client.GetAsync(apiUrl).Result;

                if (response.IsSuccessStatusCode)
                {
                    respuesta.JsonValidarLoginEscritorio = response.Content.ReadAsStringAsync().Result; // Leer la respuesta como cadena JSON
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
    }*/

    public Respuesta PerfilUsuarioLeerTodos()
    {
        var bc = new BcPerfilUsuario();
        bc.LeerTodos();
        return ObtenerRespuestaPerfilusuario(bc);
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

    public Respuesta ObtenerEquiposAnwo()
    {
        var respuesta = new Respuesta();
        respuesta.Accion = "obtener equipos de anwo";
        respuesta.Mensaje = "";
        respuesta.HayErrores = false;
        respuesta.ObtenerEquiposAnwo = "";

        string apiUrl = "http://127.0.0.1:8000/api/obtener_equipos_anwo";

        try
        {
            using (HttpClient client = new HttpClient())
            {
                HttpResponseMessage response = client.GetAsync(apiUrl).Result;

                if (response.IsSuccessStatusCode)
                    respuesta.ObtenerEquiposAnwo = response.Content.ReadAsStringAsync().Result;
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

}