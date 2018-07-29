using System;
using System.Windows.Forms;

namespace KnxSign.Gui
{
    public partial class MainForm: Form
    {
        public MainForm()
        {
            InitializeComponent();
        }

        private void MainForm_Load(object sender, EventArgs e)
        {
            var result = MessageBox.Show(
                string.Concat(
                    "This application is solely built for personal use and not for commercial or other use. Use at " +
                    "your own risk. If you choose to continue, you accept this agreement."),
                "KnxSign", 
                MessageBoxButtons.OKCancel);

            if (result == DialogResult.Cancel)
            {
                Application.Exit();
            }
        }

        private void exitButton_Click(object sender, EventArgs e)
        {
            Application.Exit();
        }

        private void signButton_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrWhiteSpace(etsDirectory.Text))
            {
                MessageBox.Show("Missing ETS directory.");
                return;
            }

            if (string.IsNullOrWhiteSpace(inputFile.Text))
            {
                MessageBox.Show("Missing input file.");
                return;
            }

            if (convert.Checked && string.IsNullOrWhiteSpace(outputFile.Text))
            {
                MessageBox.Show("Convert option requires an output file.");
                return;
            }

            // Run methods.
            try
            {
                if (string.IsNullOrEmpty(outputFile.Text))
                {
                    Signer.Sign(etsDirectory.Text, inputFile.Text);
                }
                else
                {
                    Signer.Sign(etsDirectory.Text, inputFile.Text, outputFile.Text);
                    Signer.Convert(etsDirectory.Text, outputFile.Text);
                }

                MessageBox.Show($"Signing completed!");
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Signing failed: {ex.Message}");
            }
        }

        private void etsButton_Click(object sender, EventArgs e)
        {
            if (openFolderDialog.ShowDialog() == DialogResult.OK)
            {
                etsDirectory.Text = openFolderDialog.SelectedPath;
            }
        }

        private void inputButton_Click(object sender, EventArgs e)
        {
            if (openFolderDialog.ShowDialog() == DialogResult.OK)
            {
                inputFile.Text = openFolderDialog.SelectedPath;
            }
        }

        private void outputButton_Click(object sender, EventArgs e)
        {
            if (saveFileDialog.ShowDialog() == DialogResult.OK)
            {
                outputFile.Text = saveFileDialog.FileName;
            }
        }
    }
}
