// Tests never load local .env files or pass host credentials to the application.
const allowedNames = new Set(['PATH', 'PATHEXT', 'SYSTEMROOT', 'WINDIR', 'TEMP', 'TMP', 'COMSPEC'])
for (const name of Object.keys(process.env)) {
  if (!allowedNames.has(name.toUpperCase())) delete process.env[name]
}
const { build, preview } = await import('vite')
const options = {
  envDir: false,
  define: { 'import.meta.env.VITE_API_BASE_URL': JSON.stringify(process.argv[3] || '') },
  build: { outDir: `.test-builds/${process.argv[2]}`, emptyOutDir: true },
  preview: { host: '127.0.0.1', port: Number(process.argv[2]), strictPort: true },
}
await build(options)
await preview(options)
