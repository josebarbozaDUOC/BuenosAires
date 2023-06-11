using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using BuenosAires.VentaBA.ServicioStockProducto;
using Newtonsoft.Json;

namespace BuenosAires.VentaBA
{
    public partial class VentanaLogin : Form
    {
        public VentanaLogin()
        {
            InitializeComponent();
        }

        private void BtnIngresar_Click(object sender, EventArgs e)
        {
            var ws = new ServicioStockProductoClient();
            ws.InnerChannel.OperationTimeout = new TimeSpan(1, 0, 0);
            Respuesta respuesta = ws.VerificarPassword(TxtCuenta.Text, TxtPassword.Text);
            if (respuesta.Mensaje != "") Util.MostrarMensaje(respuesta.Mensaje, respuesta.HayErrores);
            var autenticado = respuesta.JsonVerificarPassword.Contains("\"autenticado\": true");
            if (autenticado)
            {
                Util.MostrarMensajeInformativo("Autenticado correctamente");
                var ventana = new VentanaStockProducto();
                ventana.Show();
                this.Hide();
            }
            else
            {
                Util.MostrarMensajeInformativo("La cuenta o la contraseña son incorrectos");
            }
            
        }
    }
}
