using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Data.SqlClient;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using BuenosAires.BodegaBA.ServicioStockProducto;
using Newtonsoft.Json;

namespace BuenosAires.BodegaBA
{
    public partial class VentanaReservarAnwo : Form
    {
        private List<EquiposAnwo> equiposAnwo;

        public VentanaReservarAnwo()
        {
            InitializeComponent();

            dgvEquiposAnwo.AutoGenerateColumns = false;
            dgvEquiposAnwo.Columns.AddRange(new DataGridViewColumn[] {
                new DataGridViewTextBoxColumn() { Name = "nroserie", DataPropertyName = "nroserie", HeaderText = "nroserie" },
                new DataGridViewTextBoxColumn() { Name = "producto", DataPropertyName = "producto", HeaderText = "producto" },
                new DataGridViewTextBoxColumn() { Name = "precio", DataPropertyName = "precio", HeaderText = "precio" },
                new DataGridViewTextBoxColumn() { Name = "reservado", DataPropertyName = "reservado", HeaderText = "reservado" },
                new DataGridViewButtonColumn() { Name = "opciones", HeaderText = "Opciones" }
            });
            dgvEquiposAnwo.ReadOnly = true;
            dgvEquiposAnwo.SelectionMode = DataGridViewSelectionMode.FullRowSelect;
            dgvEquiposAnwo.MultiSelect = false;
            dgvEquiposAnwo.CellFormatting += dgvEquiposAnwo_CellFormatting;
            dgvEquiposAnwo.CellContentClick += dgvEquiposAnwo_CellContentClick;
            MostrarEquiposAnwoApi();
        }

        private void MostrarEquiposAnwoApi()
        {
            //Consume Servicio Anwo Soap
            var ws = new ServicioStockProductoClient();
            ws.InnerChannel.OperationTimeout = new TimeSpan(1, 0, 0);
            Respuesta respuesta = ws.ObtenerEquiposAnwo();

            if (respuesta.Mensaje != "") Util.MostrarMensaje(respuesta.Mensaje, respuesta.HayErrores);
            equiposAnwo = Util.DeserializarXML<List<EquiposAnwo>>(respuesta.XmlListaEquipoAnwo);

            dgvEquiposAnwo.DataSource = equiposAnwo;
            dgvEquiposAnwo.Refresh();
            dgvEquiposAnwo.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.AllCells;
            AgregarBotonesReservar();
        }

        private void AgregarBotonesReservar()
        {
            DataGridViewButtonColumn btnColumn = (DataGridViewButtonColumn)dgvEquiposAnwo.Columns["opciones"];
            btnColumn.UseColumnTextForButtonValue = true;
            btnColumn.Text = "Reservar";
        }

        private void dgvEquiposAnwo_CellFormatting(object sender, DataGridViewCellFormattingEventArgs e)
        {
            if (e.ColumnIndex == dgvEquiposAnwo.Columns["reservado"].Index)
            {
                if (e.Value.ToString() == "Si")
                    e.CellStyle.BackColor = Color.LightGreen;
                else
                    e.CellStyle.BackColor = Color.LightGray;
            }
        }

        private void dgvEquiposAnwo_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {
            if (e.ColumnIndex == dgvEquiposAnwo.Columns["opciones"].Index && e.RowIndex >= 0)
            {
                string nroserie = dgvEquiposAnwo.Rows[e.RowIndex].Cells["nroserie"].Value.ToString();
                CambiarEstadoReservado(nroserie);
            }
        }

        private void CambiarEstadoReservado(string nroserie)
        {
            //Consume Servicio Anwo Soap
            var ws = new ServicioStockProductoClient();
            ws.InnerChannel.OperationTimeout = new TimeSpan(1, 0, 0);
            Respuesta respuesta = ws.ReservarEquipoAnwo(nroserie);
            if (respuesta.Mensaje != "") Util.MostrarMensaje(respuesta.Mensaje, respuesta.HayErrores);

            var equipo = equiposAnwo.FirstOrDefault(e => e.nroserie == nroserie);
            if (equipo != null)
            {
                equipo.reservado = (equipo.reservado == "No") ? "Si" : "No";
                dgvEquiposAnwo.Refresh();
            }
        }

        private void btnVolver_Click(object sender, EventArgs e)
        {
            var ventana = new VentanaPrincipal();
            ventana.Show();
            this.Hide();
        }
    }
}