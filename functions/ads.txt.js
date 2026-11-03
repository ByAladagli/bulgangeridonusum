// Cloudflare Pages Function: GET /ads.txt
// mehmethilmiozkan@gmail.com Google AdSense / Ads doğrulaması için dinamik ads.txt sunucusu

export async function onRequestGet(context) {
  const pubId = context.env.ADSENSE_PUB_ID || "pub-0000000000000000";
  const cleanPub = pubId.startsWith("ca-") ? pubId.slice(3) : pubId;
  const body = [
    "# bulgangeridonusum.com.tr - Authorized Digital Sellers (ads.txt)",
    "# Account: mehmethilmiozkan@gmail.com",
    `google.com, ${cleanPub}, DIRECT, f08c47fec0942fa0`
  ].join("\n") + "\n";

  return new Response(body, {
    status: 200,
    headers: {
      "Content-Type": "text/plain; charset=utf-8",
      "Cache-Control": "public, max-age=3600"
    }
  });
}
