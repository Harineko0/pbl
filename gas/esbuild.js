const esbuild = require("esbuild");
const plugin = require("esbuild-gas-plugin");
const { GasPlugin } = plugin;

esbuild
    .build({
        entryPoints: ["./src/index.ts"],
        bundle: true,
        minify: true,
        outfile: "./dist/index.js",
        plugins: [GasPlugin],
    })
    .catch((e) => {
        console.error(e);
        process.exit(1);
    });
