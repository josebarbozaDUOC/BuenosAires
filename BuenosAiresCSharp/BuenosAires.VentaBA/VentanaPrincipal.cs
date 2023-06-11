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
    public partial class VentanaPrincipal : Form
    {
        public VentanaPrincipal()
        {
            InitializeComponent();

            dgvStockProductos.AutoGenerateColumns = false;
            dgvStockProductos.Columns.AddRange(new DataGridViewColumn[] {
                new DataGridViewTextBoxColumn() { Name = "idstock", DataPropertyName = "idstock", HeaderText = "ID de stock" },
                new DataGridViewTextBoxColumn() { Name = "idprod", DataPropertyName = "idprod", HeaderText = "ID de producto" },
                new DataGridViewTextBoxColumn() { Name = "nomprod", DataPropertyName = "nomprod", HeaderText = "Nombre de producto" },
                new DataGridViewTextBoxColumn() { Name = "nrofac", DataPropertyName = "nrofac", HeaderText = "N° de factura" },
                new DataGridViewTextBoxColumn() { Name = "estado", DataPropertyName = "estado", HeaderText = "Estado" },
            });
            dgvStockProductos.ReadOnly = true;
            dgvStockProductos.SelectionMode = DataGridViewSelectionMode.FullRowSelect;
            dgvStockProductos.MultiSelect = false;
            MostrarProductosEnBodegaApi();
        }

        private void MostrarProductosEnBodegaApi()
        {
            var ws = new ServicioStockProductoClient();
            ws.InnerChannel.OperationTimeout = new TimeSpan(1, 0, 0);
            Respuesta respuesta = ws.LeerTodosEnJson();
            if (respuesta.Mensaje != "") Util.MostrarMensaje(respuesta.Mensaje, respuesta.HayErrores);
            var lista = JsonConvert.DeserializeObject<List<StockProductoConEstado>>(respuesta.JsonListaProducto);
            dgvStockProductos.DataSource = lista;
            dgvStockProductos.Refresh();
            dgvStockProductos.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.AllCells;
        }

        private void btnSalir_Click(object sender, EventArgs e)
        {
            //System.Environment.Exit(1);
            Application.Exit();
            //this.Close();
        }
    }
}
