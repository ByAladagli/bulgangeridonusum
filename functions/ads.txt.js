export async function onRequestGet(context) {
  const body = "google.com, pub-3325199916968482, DIRECT, f08c47fec0942fa0\n";
  return new Response(body, {
    status: 200,
    headers: {
      "Content-Type": "text/plain; charset=utf-8",
      "Cache-Control": "public, max-age=3600"
    }
  });
}
