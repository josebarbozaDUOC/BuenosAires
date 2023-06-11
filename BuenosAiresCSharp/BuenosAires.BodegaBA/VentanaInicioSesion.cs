﻿using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using BuenosAires.BodegaBA.ServicioStockProducto;

namespace BuenosAires.BodegaBA
{
    public partial class VentanaInicioSesion : Form
    {
        public VentanaInicioSesion()
        {
            InitializeComponent();
        }

        private void btnIngresar_Click(object sender, EventArgs e)
        {
            var ws = new ServicioStockProductoClient();
            ws.InnerChannel.OperationTimeout = new TimeSpan(1, 0, 0);
            //Respuesta respuesta = ws.VerificarPassword(txtCorreo.Text, txtContrasena.Text);
            Respuesta respuesta = ws.ValidarLoginEscritorio(txtCorreo.Text, txtContrasena.Text, "Bodeguero");
            if (respuesta.Mensaje != "") Util.MostrarMensaje(respuesta.Mensaje, respuesta.HayErrores);
            //var autenticado = respuesta.JsonVerificarPassword.Contains("\"autenticado\": true");
            var autenticado = respuesta.JsonValidarLoginEscritorio.Contains("\"autenticado\": true");
            if (autenticado)
            {
                Util.MostrarMensajeInformativo("Autenticado correctamente");
                var ventana = new VentanaPrincipal();
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