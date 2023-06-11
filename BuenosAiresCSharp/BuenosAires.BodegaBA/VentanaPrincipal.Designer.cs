
namespace BuenosAires.BodegaBA
{
    partial class VentanaPrincipal
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.label4 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.panel1 = new System.Windows.Forms.Panel();
            this.btnSalir = new System.Windows.Forms.Button();
            this.btnAnwo = new System.Windows.Forms.Button();
            this.btnGuias = new System.Windows.Forms.Button();
            this.btnBodega = new System.Windows.Forms.Button();
            this.panel1.SuspendLayout();
            this.SuspendLayout();
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.BackColor = System.Drawing.Color.Salmon;
            this.label4.Font = new System.Drawing.Font("Ode to Idle Gaming", 16F);
            this.label4.Location = new System.Drawing.Point(435, 11);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(280, 47);
            this.label4.TabIndex = 9;
            this.label4.Text = "Buenos Aires";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.BackColor = System.Drawing.Color.Salmon;
            this.label3.Font = new System.Drawing.Font("Ode to Idle Gaming", 20F);
            this.label3.Location = new System.Drawing.Point(118, 68);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(925, 60);
            this.label3.TabIndex = 8;
            this.label3.Text = "Sistema de Bodega - Menú Principal";
            // 
            // panel1
            // 
            this.panel1.BackColor = System.Drawing.Color.Salmon;
            this.panel1.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D;
            this.panel1.Controls.Add(this.btnSalir);
            this.panel1.Controls.Add(this.btnAnwo);
            this.panel1.Controls.Add(this.btnGuias);
            this.panel1.Controls.Add(this.btnBodega);
            this.panel1.Location = new System.Drawing.Point(296, 244);
            this.panel1.Margin = new System.Windows.Forms.Padding(3, 2, 3, 2);
            this.panel1.Name = "panel1";
            this.panel1.Size = new System.Drawing.Size(562, 399);
            this.panel1.TabIndex = 10;
            // 
            // btnSalir
            // 
            this.btnSalir.BackColor = System.Drawing.SystemColors.GradientActiveCaption;
            this.btnSalir.FlatAppearance.MouseDownBackColor = System.Drawing.Color.Salmon;
            this.btnSalir.FlatAppearance.MouseOverBackColor = System.Drawing.Color.Tomato;
            this.btnSalir.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.btnSalir.Font = new System.Drawing.Font("Ode to Idle Gaming", 10F);
            this.btnSalir.Location = new System.Drawing.Point(172, 299);
            this.btnSalir.Margin = new System.Windows.Forms.Padding(3, 2, 3, 2);
            this.btnSalir.Name = "btnSalir";
            this.btnSalir.Size = new System.Drawing.Size(221, 60);
            this.btnSalir.TabIndex = 14;
            this.btnSalir.Text = "Salir";
            this.btnSalir.UseVisualStyleBackColor = false;
            this.btnSalir.Click += new System.EventHandler(this.btnSalir_Click);
            // 
            // btnAnwo
            // 
            this.btnAnwo.BackColor = System.Drawing.SystemColors.GradientActiveCaption;
            this.btnAnwo.FlatAppearance.MouseDownBackColor = System.Drawing.Color.DodgerBlue;
            this.btnAnwo.FlatAppearance.MouseOverBackColor = System.Drawing.Color.LightSkyBlue;
            this.btnAnwo.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.btnAnwo.Font = new System.Drawing.Font("Ode to Idle Gaming", 10F);
            this.btnAnwo.Location = new System.Drawing.Point(61, 205);
            this.btnAnwo.Margin = new System.Windows.Forms.Padding(3, 2, 3, 2);
            this.btnAnwo.Name = "btnAnwo";
            this.btnAnwo.Size = new System.Drawing.Size(442, 60);
            this.btnAnwo.TabIndex = 13;
            this.btnAnwo.Text = "Reservar Equipos ANWO";
            this.btnAnwo.UseVisualStyleBackColor = false;
            this.btnAnwo.Click += new System.EventHandler(this.btnAnwo_Click);
            // 
            // btnGuias
            // 
            this.btnGuias.BackColor = System.Drawing.SystemColors.GradientActiveCaption;
            this.btnGuias.FlatAppearance.MouseDownBackColor = System.Drawing.Color.DodgerBlue;
            this.btnGuias.FlatAppearance.MouseOverBackColor = System.Drawing.Color.LightSkyBlue;
            this.btnGuias.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.btnGuias.Font = new System.Drawing.Font("Ode to Idle Gaming", 10F);
            this.btnGuias.Location = new System.Drawing.Point(61, 48);
            this.btnGuias.Margin = new System.Windows.Forms.Padding(3, 2, 3, 2);
            this.btnGuias.Name = "btnGuias";
            this.btnGuias.Size = new System.Drawing.Size(442, 60);
            this.btnGuias.TabIndex = 11;
            this.btnGuias.Text = "Administrar Guías de Despacho";
            this.btnGuias.UseVisualStyleBackColor = false;
            this.btnGuias.Click += new System.EventHandler(this.btnGuias_Click);
            // 
            // btnBodega
            // 
            this.btnBodega.BackColor = System.Drawing.SystemColors.GradientActiveCaption;
            this.btnBodega.FlatAppearance.MouseDownBackColor = System.Drawing.Color.DodgerBlue;
            this.btnBodega.FlatAppearance.MouseOverBackColor = System.Drawing.Color.LightSkyBlue;
            this.btnBodega.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.btnBodega.Font = new System.Drawing.Font("Ode to Idle Gaming", 10F);
            this.btnBodega.Location = new System.Drawing.Point(61, 126);
            this.btnBodega.Margin = new System.Windows.Forms.Padding(3, 2, 3, 2);
            this.btnBodega.Name = "btnBodega";
            this.btnBodega.Size = new System.Drawing.Size(442, 60);
            this.btnBodega.TabIndex = 12;
            this.btnBodega.Text = "Administrar Bodega";
            this.btnBodega.UseVisualStyleBackColor = false;
            this.btnBodega.Click += new System.EventHandler(this.btnBodega_Click);
            // 
            // VentanaPrincipal
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.SystemColors.GradientActiveCaption;
            this.ClientSize = new System.Drawing.Size(1181, 753);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.panel1);
            this.Margin = new System.Windows.Forms.Padding(4);
            this.Name = "VentanaPrincipal";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "VentanaPrincipal";
            this.panel1.ResumeLayout(false);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Panel panel1;
        private System.Windows.Forms.Button btnAnwo;
        private System.Windows.Forms.Button btnGuias;
        private System.Windows.Forms.Button btnBodega;
        private System.Windows.Forms.Button btnSalir;
    }
}