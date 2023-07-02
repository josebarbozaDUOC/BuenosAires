using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;
using System.Windows.Forms;
using BuenosAires.BodegaBA.ServicioValidarLogin;

namespace BuenosAires.BodegaBA
{
    public partial class VentanaInicioSesion : Form
    {

        public VentanaInicioSesion()
        {
            InitializeComponent();
        }

        private async void btnIngresar_Click(object sender, EventArgs e)
        {
            var ws = new ServicioValidarLoginClient();
            ws.InnerChannel.OperationTimeout = new TimeSpan(1, 0, 0);
            Respuesta respuesta = ws.ValidarLoginEscritorio(txtCorreo.Text, txtContrasena.Text, "Bodeguero");
            //if (respuesta.Mensaje != "") Util.MostrarMensaje(respuesta.Mensaje, respuesta.HayErrores);
            var autenticado = respuesta.JsonValidarLoginEscritorio.Contains("\"autenticado\": true");
            if (autenticado)
            {
                this.MostrarMensaje(true, "Autenticado correctamente");
                await Task.Delay(2000);
                this.MostrarMensaje(false, "");
                //Util.MostrarMensajeInformativo("Autenticado correctamente");
                var ventana = new VentanaPrincipal();
                ventana.Show();
                this.Hide();
            }
            else
            {
                this.MostrarMensaje(true, "La cuenta o la contraseña son incorrectos");
                await Task.Delay(2000);
                this.MostrarMensaje(false, "");
                //Util.MostrarMensajeInformativo("La cuenta o la contraseña son incorrectos");
            }
        }
        private void MostrarMensaje(bool panel, string mensaje)
        {
            pnlMensaje.Visible = panel;
            txtMensaje.Text = mensaje;
        }

        private void checkBoxChangeColor_CheckedChanged(object sender, EventArgs e)
        {
            if(checkBoxChangeColor.Checked) this.BackColor = Color.Purple;
            else this.BackColor = Color.LightSteelBlue;
        }
    }
}
