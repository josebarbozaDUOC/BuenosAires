using BuenosAires.BusinessLayer;
using BuenosAires.Model;
using System;
using System.Net.Http;

public class ServicioValidarLogin : IServicioValidarLogin
{
    public Respuesta ValidarLoginEscritorio(string username, string password, string tipousu)
    {
        var respuesta = new Respuesta();
        respuesta.Accion = "Validar Login Escritorio";
        respuesta.Mensaje = "";
        respuesta.HayErrores = false;
        respuesta.JsonValidarLoginEscritorio = "";
        string apiUrl = "http://127.0.0.1:8000/api/validar_login_escritorio/" + username + "/" + password + "/" + tipousu;

        try{
            using (HttpClient client = new HttpClient()){
                HttpResponseMessage response = client.GetAsync(apiUrl).Result;
                if (response.IsSuccessStatusCode)
                    respuesta.JsonValidarLoginEscritorio = response.Content.ReadAsStringAsync().Result;
                else{
                    respuesta.Mensaje = "No fue posible " + respuesta.Accion;
                    respuesta.HayErrores = true;
                }
            }
        }
        catch (Exception ex){
            respuesta.HayErrores = true;
            respuesta.Mensaje = Util.MensajeError("No fue posible " + respuesta.Accion, ex);
        }
        return respuesta;
    }
}