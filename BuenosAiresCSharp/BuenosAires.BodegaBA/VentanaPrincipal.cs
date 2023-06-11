using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace BuenosAires.BodegaBA
{
    public partial class VentanaPrincipal : Form
    {
        public VentanaPrincipal()
        {
            InitializeComponent();
        }

        private void btnGuias_Click(object sender, EventArgs e)
        {
            var ventana = new VentanaGuiasDespacho();
            ventana.Show();
            this.Hide();
        }
        private void btnBodega_Click(object sender, EventArgs e)
        {
            var ventana = new VentanaConsultarBodega();
            ventana.Show();
            this.Hide();
        }
        private void btnAnwo_Click(object sender, EventArgs e)
        {
            var ventana = new VentanaReservarAnwo();
            ventana.Show();
            this.Hide();
        }

        private void btnSalir_Click(object sender, EventArgs e)
        {
            Application.Exit();
        }
    }
}
