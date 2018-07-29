using CommandLine;

namespace KnxSign.Cli
{
    /// <summary>
    /// Command line options.
    /// </summary>
    public class Options
    {
        /// <summary>
        /// Gets or sets the location of ETS.
        /// </summary>
        /// <value>
        /// The location of ETS.
        /// </value>
        [Option('e', "ets", Required = true, HelpText = "ETS installation directory.")]
        public string EtsDirectory { get; set; }

        /// <summary>
        /// Gets or sets the input directory.
        /// </summary>
        /// <value>
        /// The input directory.
        /// </value>
        [Option('d', "directory", Required = true, HelpText = "Input directory.")]
        public string InputDirectory { get; set; }

        /// <summary>
        /// Gets or sets the output file (optional).
        /// </summary>
        /// <value>
        /// The optional file (optional).
        /// </value>
        [Option('o', "output", Required = false, HelpText = "Output file.")]
        public string OutputFile { get; set; }

        /// <summary>
        /// Gets or sets whether the convert should be applied.
        /// </summary>
        /// <value>
        /// True if converter should be applied.
        /// </value>
        [Option('c', "convert", Required = false, Default = false, HelpText = "Run converter.")]
        public bool Convert { get; set; }
    }
}
