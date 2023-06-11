using System;
using System.Collections.Generic;
using System.Data;
using System.Data.SqlClient;
using System.Windows.Forms;
using BuenosAires.BodegaBA.ServicioStockProducto;
using Newtonsoft.Json;

namespace BuenosAires.BodegaBA
{
    public partial class VentanaGuiasDespacho : Form
    {
        private const string connectionString = "Data Source=DESKTOP-ESOHJKV\\MSSQLSERVERDUOC;Initial Catalog=base_datos;user id=sa;password=123;";
        private List<GuiaDespachoConEstado> guiasDespacho;

        public VentanaGuiasDespacho()
        {
            InitializeComponent();

            dgvGuiasDespacho.AutoGenerateColumns = false;
            dgvGuiasDespacho.Columns.AddRange(new DataGridViewColumn[] {
                new DataGridViewTextBoxColumn() { Name = "nrogd", DataPropertyName = "nrogd", HeaderText = "Nro GD" },
                new DataGridViewTextBoxColumn() { Name = "producto", DataPropertyName = "producto", HeaderText = "Producto" },
                new DataGridViewTextBoxColumn() { Name = "fechagd", DataPropertyName = "fechagd", HeaderText = "Fecha GD" },
                new DataGridViewTextBoxColumn() { Name = "estadogd", DataPropertyName = "estadogd", HeaderText = "Estado GD" },
                new DataGridViewTextBoxColumn() { Name = "nrofac", DataPropertyName = "nrofac", HeaderText = "Nro Factura" },
                new DataGridViewTextBoxColumn() { Name = "cliente", DataPropertyName = "cliente", HeaderText = "Cliente" },
                new DataGridViewTextBoxColumn() { Name = "opciones", HeaderText = "Opciones", ReadOnly = true, AutoSizeMode = DataGridViewAutoSizeColumnMode.AllCells }
            });

            dgvGuiasDespacho.CellFormatting += dgvGuiasDespacho_CellFormatting;
            dgvGuiasDespacho.CellContentClick += dgvGuiasDespacho_CellContentClick;

            MostrarGuiasDespachoApi();
        }

        private void MostrarGuiasDespachoApi()
        {
            var ws = new ServicioStockProductoClient();
            ws.InnerChannel.OperationTimeout = new TimeSpan(1, 0, 0);
            Respuesta respuesta = ws.ObtenerGuiasDespacho();
            guiasDespacho = JsonConvert.DeserializeObject<List<GuiaDespachoConEstado>>(respuesta.ObtenerGuiasDespacho);
            dgvGuiasDespacho.DataSource = guiasDespacho;
        }

        private void dgvGuiasDespacho_CellFormatting(object sender, DataGridViewCellFormattingEventArgs e)
        {
            if (e.ColumnIndex == dgvGuiasDespacho.Columns["opciones"].Index)
            {
                e.Value = "Despachado | Imprimir | Entregado";
            }
        }

        private void dgvGuiasDespacho_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {
            if (e.ColumnIndex == dgvGuiasDespacho.Columns["opciones"].Index)
            {
                var guiaDespacho = (GuiaDespachoConEstado)dgvGuiasDespacho.Rows[e.RowIndex].DataBoundItem;

                var mouseLocation = dgvGuiasDespacho.PointToClient(Cursor.Position);
                var cellRectangle = dgvGuiasDespacho.GetCellDisplayRectangle(e.ColumnIndex, e.RowIndex, false);

                if (mouseLocation.X > cellRectangle.X + 10 && mouseLocation.X < cellRectangle.X + 80)
                {
                    CambiarEstado("SP_ESTADO_DESPACHADO_GUIA_DE_DESPACHO", guiaDespacho.nrogd.ToString(), "Despachado");
                }
                else if (mouseLocation.X > cellRectangle.X + 90 && mouseLocation.X < cellRectangle.X + 150)
                {
                    // no se si se imprime
                }
                else if (mouseLocation.X > cellRectangle.X + 160 && mouseLocation.X < cellRectangle.X + 230)
                {
                    CambiarEstado("SP_ESTADO_ENTREGADO_GUIA_DE_DESPACHO", guiaDespacho.nrogd.ToString(), "Entregado");
                }
            }
        }

        private void CambiarEstado(string storedProcedure, string nro, string estado)
        {
            using (SqlConnection connection = new SqlConnection(connectionString))
            {
                connection.Open();

                using (SqlCommand command = new SqlCommand(storedProcedure, connection))
                {
                    command.CommandType = CommandType.StoredProcedure;
                    command.Parameters.AddWithValue("@nro", nro);
                    command.ExecuteNonQuery();
                }
            }

            // Actualiza la guia de despacho
            var guiaDespacho = guiasDespacho.Find(g => g.nrogd.ToString() == nro);
            if (guiaDespacho != null)
            {
                guiaDespacho.estadogd = estado;
            }

            dgvGuiasDespacho.Refresh();
        }

        private void btnVolver_Click(object sender, EventArgs e)
        {
            var ventana = new VentanaPrincipal();
            ventana.Show();
            this.Hide();
        }
    }
}