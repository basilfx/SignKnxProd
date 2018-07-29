namespace KnxSign.Gui
{
    partial class MainForm
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
            this.detailsGroup = new System.Windows.Forms.GroupBox();
            this.outputButton = new System.Windows.Forms.Button();
            this.inputButton = new System.Windows.Forms.Button();
            this.etsButton = new System.Windows.Forms.Button();
            this.outputFile = new System.Windows.Forms.TextBox();
            this.outputLabel = new System.Windows.Forms.Label();
            this.inputFile = new System.Windows.Forms.TextBox();
            this.inputLabel = new System.Windows.Forms.Label();
            this.etsDirectory = new System.Windows.Forms.TextBox();
            this.etsLabel = new System.Windows.Forms.Label();
            this.signButton = new System.Windows.Forms.Button();
            this.exitButton = new System.Windows.Forms.Button();
            this.convert = new System.Windows.Forms.CheckBox();
            this.openFolderDialog = new System.Windows.Forms.FolderBrowserDialog();
            this.saveFileDialog = new System.Windows.Forms.SaveFileDialog();
            this.detailsGroup.SuspendLayout();
            this.SuspendLayout();
            // 
            // detailsGroup
            // 
            this.detailsGroup.Controls.Add(this.convert);
            this.detailsGroup.Controls.Add(this.outputButton);
            this.detailsGroup.Controls.Add(this.inputButton);
            this.detailsGroup.Controls.Add(this.etsButton);
            this.detailsGroup.Controls.Add(this.outputFile);
            this.detailsGroup.Controls.Add(this.outputLabel);
            this.detailsGroup.Controls.Add(this.inputFile);
            this.detailsGroup.Controls.Add(this.inputLabel);
            this.detailsGroup.Controls.Add(this.etsDirectory);
            this.detailsGroup.Controls.Add(this.etsLabel);
            this.detailsGroup.Location = new System.Drawing.Point(12, 9);
            this.detailsGroup.Name = "detailsGroup";
            this.detailsGroup.Size = new System.Drawing.Size(483, 143);
            this.detailsGroup.TabIndex = 0;
            this.detailsGroup.TabStop = false;
            this.detailsGroup.Text = "Input details";
            // 
            // outputButton
            // 
            this.outputButton.Location = new System.Drawing.Point(442, 79);
            this.outputButton.Name = "outputButton";
            this.outputButton.Size = new System.Drawing.Size(35, 23);
            this.outputButton.TabIndex = 8;
            this.outputButton.Text = "...";
            this.outputButton.UseVisualStyleBackColor = true;
            this.outputButton.Click += new System.EventHandler(this.outputButton_Click);
            // 
            // inputButton
            // 
            this.inputButton.Location = new System.Drawing.Point(442, 53);
            this.inputButton.Name = "inputButton";
            this.inputButton.Size = new System.Drawing.Size(35, 23);
            this.inputButton.TabIndex = 7;
            this.inputButton.Text = "...";
            this.inputButton.UseVisualStyleBackColor = true;
            this.inputButton.Click += new System.EventHandler(this.inputButton_Click);
            // 
            // etsButton
            // 
            this.etsButton.Location = new System.Drawing.Point(442, 27);
            this.etsButton.Name = "etsButton";
            this.etsButton.Size = new System.Drawing.Size(35, 23);
            this.etsButton.TabIndex = 6;
            this.etsButton.Text = "...";
            this.etsButton.UseVisualStyleBackColor = true;
            this.etsButton.Click += new System.EventHandler(this.etsButton_Click);
            // 
            // outputFile
            // 
            this.outputFile.Location = new System.Drawing.Point(165, 81);
            this.outputFile.Name = "outputFile";
            this.outputFile.Size = new System.Drawing.Size(271, 20);
            this.outputFile.TabIndex = 5;
            // 
            // outputLabel
            // 
            this.outputLabel.AutoSize = true;
            this.outputLabel.Location = new System.Drawing.Point(101, 84);
            this.outputLabel.Name = "outputLabel";
            this.outputLabel.Size = new System.Drawing.Size(58, 13);
            this.outputLabel.TabIndex = 4;
            this.outputLabel.Text = "Output file:";
            // 
            // inputFile
            // 
            this.inputFile.Location = new System.Drawing.Point(165, 55);
            this.inputFile.Name = "inputFile";
            this.inputFile.Size = new System.Drawing.Size(271, 20);
            this.inputFile.TabIndex = 3;
            // 
            // inputLabel
            // 
            this.inputLabel.AutoSize = true;
            this.inputLabel.Location = new System.Drawing.Point(82, 58);
            this.inputLabel.Name = "inputLabel";
            this.inputLabel.Size = new System.Drawing.Size(77, 13);
            this.inputLabel.TabIndex = 2;
            this.inputLabel.Text = "Input directory:";
            // 
            // etsDirectory
            // 
            this.etsDirectory.Location = new System.Drawing.Point(165, 27);
            this.etsDirectory.Name = "etsDirectory";
            this.etsDirectory.Size = new System.Drawing.Size(271, 20);
            this.etsDirectory.TabIndex = 1;
            // 
            // etsLabel
            // 
            this.etsLabel.AutoSize = true;
            this.etsLabel.Location = new System.Drawing.Point(30, 30);
            this.etsLabel.Name = "etsLabel";
            this.etsLabel.Size = new System.Drawing.Size(129, 13);
            this.etsLabel.TabIndex = 0;
            this.etsLabel.Text = "ETS Installation Directory:";
            // 
            // signButton
            // 
            this.signButton.Location = new System.Drawing.Point(334, 158);
            this.signButton.Name = "signButton";
            this.signButton.Size = new System.Drawing.Size(75, 23);
            this.signButton.TabIndex = 1;
            this.signButton.Text = "Sign";
            this.signButton.UseVisualStyleBackColor = true;
            this.signButton.Click += new System.EventHandler(this.signButton_Click);
            // 
            // exitButton
            // 
            this.exitButton.Location = new System.Drawing.Point(415, 158);
            this.exitButton.Name = "exitButton";
            this.exitButton.Size = new System.Drawing.Size(75, 23);
            this.exitButton.TabIndex = 2;
            this.exitButton.Text = "Exit";
            this.exitButton.UseVisualStyleBackColor = true;
            this.exitButton.Click += new System.EventHandler(this.exitButton_Click);
            // 
            // convert
            // 
            this.convert.AutoSize = true;
            this.convert.Location = new System.Drawing.Point(165, 108);
            this.convert.Name = "convert";
            this.convert.Size = new System.Drawing.Size(222, 17);
            this.convert.TabIndex = 9;
            this.convert.Text = "Run conversion utility (requires output file)";
            this.convert.UseVisualStyleBackColor = true;
            // 
            // saveFileDialog
            // 
            this.saveFileDialog.RestoreDirectory = true;
            // 
            // MainForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(507, 193);
            this.Controls.Add(this.exitButton);
            this.Controls.Add(this.signButton);
            this.Controls.Add(this.detailsGroup);
            this.MaximizeBox = false;
            this.Name = "MainForm";
            this.Text = "KnxSign";
            this.Load += new System.EventHandler(this.MainForm_Load);
            this.detailsGroup.ResumeLayout(false);
            this.detailsGroup.PerformLayout();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.GroupBox detailsGroup;
        private System.Windows.Forms.Label inputLabel;
        private System.Windows.Forms.TextBox etsDirectory;
        private System.Windows.Forms.Label etsLabel;
        private System.Windows.Forms.TextBox outputFile;
        private System.Windows.Forms.Label outputLabel;
        private System.Windows.Forms.TextBox inputFile;
        private System.Windows.Forms.Button etsButton;
        private System.Windows.Forms.Button outputButton;
        private System.Windows.Forms.Button inputButton;
        private System.Windows.Forms.Button signButton;
        private System.Windows.Forms.Button exitButton;
        private System.Windows.Forms.CheckBox convert;
        private System.Windows.Forms.FolderBrowserDialog openFolderDialog;
        private System.Windows.Forms.SaveFileDialog saveFileDialog;
    }
}