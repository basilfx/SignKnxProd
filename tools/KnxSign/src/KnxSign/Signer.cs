using McMaster.Extensions.CommandLineUtils;
using System;
using System.Diagnostics;
using System.IO;
using System.Reflection;

namespace KnxSign
{
    /// <summary>
    /// The class that contains the signing method.
    /// </summary>
    public class Signer
    {
        /// <summary>
        /// Sign a giving directory. Optionally, an output file can be specified to directly generate a zipped file.
        /// 
        /// This will need a reference to ETS directory, as it uses reflection to load the required assemblies.
        /// </summary>
        /// <param name="etsDir">ETS directory.</param>
        /// <param name="signDir">Input directory to sign.</param>
        /// <param name="outputFile">Optional output file.</param>
        public static void Sign(string etsDir, string signDir, string outputFile = null)
        {
            // Ensure the input directory exists.
            if (!Directory.Exists(signDir))
            {
                throw new Exception($"Directory to be signed does not exist: {signDir}");
            }

            // Load the assembly.
            string dllFile = Path.Combine(etsDir, "Knx.Ets.Converter.ConverterEngine.dll");

            if (!File.Exists(dllFile))
            {
                throw new Exception($"Cannot load Knx.Ets.Converter.ConverterEngine.dll: {dllFile}");
            }

            var assembly = Assembly.LoadFrom(dllFile);
            var type = assembly.GetType("Knx.Ets.Converter.ConverterEngine.ConverterEngine");

            // Sign the directory.
            var signMethod = type.GetMethod("SignOutputFiles", BindingFlags.Static | BindingFlags.NonPublic);
            signMethod.Invoke(null, new object[] { signDir });

            // Optionally, pack the signed directory.
            if (outputFile != null)
            {
                var zipMethod = type.GetMethod("CreateZipFileFromDir", BindingFlags.Static | BindingFlags.Public);
                zipMethod.Invoke(null, new object[] { outputFile, signDir, false });
            }
        }

        /// <summary>
        /// Run the convert utility over the signed file, to pre-validate it.
        /// </summary>
        /// <param name="etsDir">ETS directory.</param>
        /// <param name="signedFile">The signed file.</param>
        public static void Convert(string etsDir, string signedFile)
        {
            // Ensure the signed file exists.
            if (!File.Exists(signedFile))
            {
                throw new Exception($"Input file does not exist: {signedFile}");
            }

            // Find path to the process.
            var processFile = Path.Combine(etsDir, "knxconv.exe");

            if (!File.Exists(processFile))
            {
                throw new Exception($"Cannot find knxconv.exe: {processFile}");
            }

            // Run the command, retrieve the response.
            using (var process = new Process())
            {
                ProcessStartInfo info = new ProcessStartInfo(processFile);

                info.Arguments = ArgumentEscaper.EscapeAndConcatenate(new string[] { signedFile, signedFile });
                info.RedirectStandardInput = true;
                info.RedirectStandardOutput = true;
                info.UseShellExecute = false;

                process.StartInfo = info;
                process.Start();
                process.StandardOutput.ReadToEnd();

                if (process.ExitCode != 0)
                {
                    throw new Exception("Unable to convert signed file.");
                }
            }
        }
    }
}
