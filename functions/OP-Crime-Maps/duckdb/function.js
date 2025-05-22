export async function onRequest(context) {
  const { env, params } = context;          // env.ASSET_BUCKET, params.path[]
  const key = params.path.join('/');        // e.g. "duckdb-eh.wasm"

  const object = await env.ASSET_BUCKET.get(key, { httpMetadata: true });
  if (!object) return new Response('Not found', { status: 404 });

  const hdr = new Headers();
  object.writeHttpMetadata(hdr);            // copies content‑type, cache‑control
  return new Response(object.body, { headers: hdr });
}
