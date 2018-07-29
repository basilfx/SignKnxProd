using CommandLine;
using System;

namespace KnxSign.Cli
{
    class Program
    {
        /// <summary>
        /// The application entry point.
        /// </summary>
        /// <param name="args">Application arguments.</param>
        /// <returns>Zero on success, non-zero error code on failure.</returns>
        public static int Main(string[] args)
        {
            return Parser.Default
                .ParseArguments<Options>(args)
                .MapResult(
                    options => Run(options),
                    errors => 1);
        }

        /// <summary>
        /// Runs the signer with the specified options.
        /// </summary>
        /// <param name="options">The options.</param>
        /// <returns>An <see cref="int"/> status code.</returns>
        public static int Run(Options options)
        {
            try
            {
                Signer.Sign(options.EtsDirectory, options.InputDirectory, options.OutputFile);

                if (options.Convert)
                {
                    Signer.Convert(options.EtsDirectory, options.OutputFile);
                }

                // All went well.
                return 0;
            }
            catch (Exception e)
            {
                Console.Write(e);

                // Return error code.
                return 1;
            }
        }
    }
}
