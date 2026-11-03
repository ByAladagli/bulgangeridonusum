// Cloudflare Pages Function: POST /api/contact
// Sunucu taraflı form doğrulama ve Gmail SMTP (cloudflare:sockets TLS 465) ile anlık bildirim

import { connect } from "cloudflare:sockets";

function toBase64Utf8(str) {
  const bytes = new TextEncoder().encode(str);
  let binary = "";
  for (let i = 0; i < bytes.byteLength; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return btoa(binary);
}

async function sendGmailSmtp({ user, pass, subject, htmlBody, replyTo }) {
  const socket = connect({ hostname: "smtp.gmail.com", port: 465 }, { secureTransport: "on" });
  const writer = socket.writable.getWriter();
  const reader = socket.readable.getReader();
  const decoder = new TextDecoder();
  const encoder = new TextEncoder();

  async function readLine() {
    const { value, done } = await reader.read();
    if (done) return "";
    return decoder.decode(value);
  }

  async function writeCmd(cmd) {
    await writer.write(encoder.encode(cmd + "\r\n"));
    return await readLine();
  }

  try {
    await readLine(); // 220 banner
    await writeCmd("EHLO bulgangeridonusum.com.tr");
    await writeCmd("AUTH LOGIN");
    await writeCmd(toBase64Utf8(user));
    const authResp = await writeCmd(toBase64Utf8(pass));
    if (!authResp.includes("235")) {
      throw new Error("SMTP Auth error: " + authResp);
    }
    await writeCmd(`MAIL FROM:<${user}>`);
    await writeCmd(`RCPT TO:<${user}>`);
    await writeCmd("DATA");

    const mimeMessage = [
      `From: "Bulgan Hurdacilik Web Formu" <${user}>`,
      `To: <${user}>`,
      replyTo ? `Reply-To: ${replyTo}` : null,
      `Subject: =?UTF-8?B?${toBase64Utf8(subject)}?=`,
      "MIME-Version: 1.0",
      'Content-Type: text/html; charset="UTF-8"',
      "Content-Transfer-Encoding: base64",
      "",
      toBase64Utf8(htmlBody),
      "."
    ]
      .filter(Boolean)
      .join("\r\n");

    const sendResp = await writeCmd(mimeMessage);
    await writeCmd("QUIT");
    writer.releaseLock();
    reader.releaseLock();
    socket.close();
    return sendResp.includes("250");
  } catch (err) {
    try {
      socket.close();
    } catch (_) {}
    throw err;
  }
}

export async function onRequestPost(context) {
  const { request, env } = context;
  const headers = {
    "Content-Type": "application/json; charset=utf-8",
    "Access-Control-Allow-Origin": "https://bulgangeridonusum.com.tr"
  };

  try {
    const body = await request.json();
    const name = String(body.name || "").trim();
    const phone = String(body.phone || "").trim();
    const city = String(body.city || "Mardin / Kızıltepe").trim();
    const material = String(body.material || "Genel Hurda").trim();
    const weight = String(body.weight || "Belirtilmedi").trim();
    const note = String(body.note || "").trim();

    const digits = phone.replace(/\D/g, "");
    if (name.length < 2) {
      return new Response(
        JSON.stringify({ ok: false, error: "Lütfen adınızı ve soyadınızı (en az 2 karakter) girin." }),
        { status: 400, headers }
      );
    }
    if (digits.length < 10) {
      return new Response(
        JSON.stringify({ ok: false, error: "Lütfen geçerli bir 10 veya 11 haneli telefon numarası girin." }),
        { status: 400, headers }
      );
    }

    const smtpUser = env.GMAIL_USER || "bulganorhan19@gmail.com";
    const smtpPass = (env.GMAIL_APP_PASSWORD || "").replace(/\s+/g, "");

    let emailSent = false;
    if (smtpPass) {
      const subject = `Yeni Hurda Alım / Kantar Talebi: ${name} (${city} - ${material})`;
      const htmlBody = `
        <div style="font-family:Segoe UI,Arial,sans-serif;max-width:620px;border:1px solid #cbd5e1;border-radius:8px;overflow:hidden">
          <div style="background:#11151c;color:#ffffff;padding:18px 22px;border-bottom:3px solid #d4a52a">
            <h2 style="margin:0;font-size:18px">BULGAN HURDACILIK — YENİ SAHA / KANTAR TALEBİ</h2>
            <p style="margin:4px 0 0;color:#cbd5e1;font-size:12px">bulgangeridonusum.com.tr iletişim ve teklif formundan gönderildi</p>
          </div>
          <div style="padding:20px 22px;background:#ffffff;color:#0f172a;font-size:14px;line-height:1.6">
            <p><strong>Müşteri / Firma Adı:</strong> ${name}</p>
            <p><strong>Telefon Numarası:</strong> <a href="tel:${digits}">${phone}</a> &nbsp;|&nbsp; <a href="https://wa.me/90${digits.slice(-10)}">WhatsApp ile Yanıtla</a></p>
            <p><strong>İl / İlçe Konumu:</strong> ${city}</p>
            <p><strong>Hurda Cinsi:</strong> ${material}</p>
            <p><strong>Tahmini Miktar / Tonaj:</strong> ${weight}</p>
            <p><strong>Ek Not / Açıklama:</strong> ${note || "Belirtilmedi"}</p>
          </div>
        </div>
      `;
      try {
        emailSent = await sendGmailSmtp({
          user: smtpUser,
          pass: smtpPass,
          subject,
          htmlBody
        });
      } catch (smtpErr) {
        console.error("SMTP send failed:", smtpErr);
      }
    }

    return new Response(
      JSON.stringify({
        ok: true,
        emailSent,
        message: "Talebiniz kantar merkezimize başarıyla kaydedildi."
      }),
      { status: 200, headers }
    );
  } catch (err) {
    return new Response(
      JSON.stringify({ ok: false, error: "İstek işlenirken bir hata oluştu. Lütfen 0545 904 38 34 hattımızdan ulaşın." }),
      { status: 500, headers }
    );
  }
}
