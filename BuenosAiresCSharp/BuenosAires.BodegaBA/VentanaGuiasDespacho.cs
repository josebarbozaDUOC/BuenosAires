using System;
using System.Collections.Generic;
using System.Data;
using System.Data.SqlClient;
using System.Windows.Forms;
using BuenosAires.BodegaBA.ServicioStockProducto;
using Newtonsoft.Json;
using System.Drawing;
using System.Drawing.Printing;

namespace BuenosAires.BodegaBA
{
    public partial class VentanaGuiasDespacho : Form
    {
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
                var nroguia = guiaDespacho.nrogd.ToString();
                var mouseLocation = dgvGuiasDespacho.PointToClient(Cursor.Position);
                var cellRectangle = dgvGuiasDespacho.GetCellDisplayRectangle(e.ColumnIndex, e.RowIndex, false);

                if (mouseLocation.X > cellRectangle.X + 1 && mouseLocation.X < cellRectangle.X + 99)
                {
                    CambiarEstado(nroguia, "Despachado");
                }
                else if (mouseLocation.X > cellRectangle.X + 100 && mouseLocation.X < cellRectangle.X + 179)
                {
                    string texto = string.Format("GUÍA DE DESPACHO "+ "\n\r" + "\n\r" +
                        "Nro GD:      "+ guiaDespacho.nrogd.ToString()       + "\n\r" +
                        "Producto:    "+ guiaDespacho.producto.ToString()    + "\n\r" +
                        "Fecha:       "+ guiaDespacho.fechagd.ToString()     + "\n\r" +
                        "Estado:      "+ guiaDespacho.estadogd.ToString()    + "\n\r" +
                        "Nro Factura: "+ guiaDespacho.nrofac.ToString()      + "\n\r" +
                        "Cliente:     "+ guiaDespacho.cliente.ToString());

                    ImprimirTexto(texto);
                }
                else if (mouseLocation.X > cellRectangle.X + 180 && mouseLocation.X < cellRectangle.X + 270)
                {
                    CambiarEstado(guiaDespacho.nrogd.ToString(), "Entregado");
                }
            }
        }

        private void CambiarEstado(string nro, string estado)
        {
            var ws = new ServicioStockProductoClient();
            ws.InnerChannel.OperationTimeout = new TimeSpan(1, 0, 0);
            ws.ModificarEstadoGuiaDespacho(nro, estado);

            var guiaDespacho = guiasDespacho.Find(g => g.nrogd.ToString() == nro);
            if (guiaDespacho != null)
            {
                guiaDespacho.estadogd = estado;
            }
            dgvGuiasDespacho.Refresh();
        }

        private void ImprimirTexto(string texto)
        {
            PrintDocument pd = new PrintDocument();
            pd.PrintPage += (sender, e) => ImprimirPagina(sender, e, texto);

            // Configurar los márgenes
            pd.DefaultPageSettings.Margins = new Margins(50, 50, 50, 50); // Márgenes de 50 unidades en todos los lados

            // Mostrar la vista previa del documento
            PrintPreviewDialog printPreviewDialog = new PrintPreviewDialog();
            printPreviewDialog.Document = pd;

            // Ajustar el tamaño de la ventana de la vista previa
            printPreviewDialog.ClientSize = new Size(600, 1000); // Tamaño deseado para el visualizador del documento
            printPreviewDialog.StartPosition = FormStartPosition.CenterScreen;
            printPreviewDialog.ShowDialog();
        }
        private void ImprimirPagina(object sender, PrintPageEventArgs e, string texto)
        {
            // Definir la fuente y el formato
            Font fuente = new Font("Arial", 12);
            StringFormat formato = new StringFormat();

            // Obtener los márgenes de la página
            Margins margenes = ((PrintDocument)sender).DefaultPageSettings.Margins;
            float x = margenes.Left;
            float y = margenes.Top;

            // Dibujar el texto en la página con los márgenes aplicados
            e.Graphics.DrawString(texto, fuente, Brushes.Black, new PointF(x, y), formato);
        }

        private void btnVolver_Click(object sender, EventArgs e)
        {
            var ventana = new VentanaPrincipal();
            ventana.Show();
            this.Hide();
        }
    }
}