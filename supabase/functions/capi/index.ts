// JAWZR Meta Conversions API relay. Lead + Purchase only (AddToCart / InitiateCheckout / PageView stay browser-only).
// The browser fires the Pixel with an eventID and posts the same eventID here; Meta dedups the pair.
// Rules (from CAPI_EVENTS_AND_REPORTING_PLAYBOOK.md): pixel chosen from the page host, no fallback;
// missing token = skip; never throw; outbox row per event (unique pixel+event+id => no double sends).
import { createClient } from "jsr:@supabase/supabase-js@2";

const GRAPH = "https://graph.facebook.com/v21.0";
// host -> pixel + the NAME of its token secret. Unknown host => skipped.
const REGISTRY: Record<string, { pixel: string; tokenEnv: string; testEnv: string }> = {
  "tothemoonastronauts.github.io": { pixel: "28889931507316454", tokenEnv: "META_CAPI_TOKEN_JAWZR", testEnv: "META_TEST_CODE_JAWZR" },
  "jawzr.com": { pixel: "28889931507316454", tokenEnv: "META_CAPI_TOKEN_JAWZR", testEnv: "META_TEST_CODE_JAWZR" },
  "www.jawzr.com": { pixel: "28889931507316454", tokenEnv: "META_CAPI_TOKEN_JAWZR", testEnv: "META_TEST_CODE_JAWZR" },
};
const EVENTS = new Set(["Lead", "Purchase"]);
const cors = (origin: string | null) => ({
  "Access-Control-Allow-Origin": origin && /^(https:\/\/(tothemoonastronauts\.github\.io|(www\.)?jawzr\.com)|http:\/\/localhost(:\d+)?)$/.test(origin) ? origin : "https://tothemoonastronauts.github.io",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "content-type, apikey, authorization",
  "Vary": "Origin",
});
const json = (b: unknown, h: Record<string, string>, s = 200) => new Response(JSON.stringify(b), { status: s, headers: { ...h, "Content-Type": "application/json" } });

async function sha(v?: string | null) {
  if (!v) return undefined;
  const d = new TextEncoder().encode(v);
  return Array.from(new Uint8Array(await crypto.subtle.digest("SHA-256", d))).map((x) => x.toString(16).padStart(2, "0")).join("");
}
const norm = (v?: string | null) => (v ?? "").toString().trim().toLowerCase();
const s = (v: unknown, n: number) => (typeof v === "string" ? v.slice(0, n) : undefined);

// fb.<idx>.<creationTime_ms>.<id>: seconds -> ms, future -> clamp to event time, malformed -> drop
function normFb(v: unknown, eventMs: number): string | undefined {
  if (typeof v !== "string") return undefined;
  const m = v.match(/^fb\.(\d)\.(\d{9,13})\.(.+)$/);
  if (!m) return undefined;
  let t = Number(m[2]);
  if (t < 1e12) t *= 1000;
  if (t > eventMs) t = eventMs;
  return `fb.${m[1]}.${t}.${m[3]}`.slice(0, 300);
}

// ISO-3166 alpha-2 for the countries the checkout offers
const CC: Record<string, string> = { "Austria":"at","Belgium":"be","Bulgaria":"bg","Croatia":"hr","Cyprus":"cy","Czechia":"cz","Denmark":"dk","Estonia":"ee","Finland":"fi","France":"fr","Germany":"de","Greece":"gr","Hungary":"hu","Ireland":"ie","Italy":"it","Latvia":"lv","Lithuania":"lt","Luxembourg":"lu","Malta":"mt","Netherlands":"nl","Poland":"pl","Portugal":"pt","Romania":"ro","Slovakia":"sk","Slovenia":"si","Spain":"es","Sweden":"se","United States":"us" };

Deno.serve(async (req) => {
  const h = cors(req.headers.get("origin"));
  if (req.method === "OPTIONS") return new Response("ok", { headers: h });
  if (req.method !== "POST") return json({ ok: false, error: "method" }, h, 405);
  let b: any;
  try { b = await req.json(); } catch { return json({ ok: false, error: "json" }, h, 400); }
  try {
    const name = String(b.event_name || "");
    const eventId = s(b.event_id, 80);
    if (!EVENTS.has(name) || !eventId) return json({ ok: false, error: "event" }, h, 400);
    if (b.consent !== true) return json({ ok: true, status: "skipped", reason: "no consent" }, h);
    let host = "";
    try { host = new URL(String(b.event_source_url)).host; } catch { /* */ }
    const reg = REGISTRY[host];
    if (!reg) return json({ ok: true, status: "skipped", reason: "unknown host" }, h);

    const now = Date.now();
    const eventTime = Math.floor(Math.min(Number(b.event_time_ms) || now, now) / 1000);
    const u = b.user || {};
    const ip = (req.headers.get("cf-connecting-ip") || req.headers.get("x-forwarded-for") || "").split(",")[0].trim() || undefined;
    const ua = req.headers.get("user-agent") || undefined;
    const phone = norm(u.phone).replace(/[^0-9]/g, "");
    const user_data: Record<string, unknown> = {
      em: [await sha(norm(u.email))].filter(Boolean),
      fn: u.first_name ? [await sha(norm(u.first_name))] : undefined,
      ln: u.last_name ? [await sha(norm(u.last_name))] : undefined,
      ph: phone.length >= 7 ? [await sha(phone)] : undefined,
      ct: u.city ? [await sha(norm(u.city).replace(/[^a-z]/g, ""))] : undefined,
      zp: u.zip ? [await sha(norm(u.zip).replace(/\s/g, ""))] : undefined,
      st: u.state ? [await sha(norm(u.state).replace(/[^a-z]/g, ""))] : undefined,
      country: u.country && CC[u.country] ? [await sha(CC[u.country])] : undefined,
      external_id: b.session_id ? [await sha(String(b.session_id))] : undefined,
      client_ip_address: ip,
      client_user_agent: ua,
      fbc: normFb(b.fbc, now),
      fbp: normFb(b.fbp, now),
    };
    Object.keys(user_data).forEach((k) => (user_data[k] === undefined || (Array.isArray(user_data[k]) && !(user_data[k] as unknown[]).length)) && delete user_data[k]);

    const cd = b.custom_data || {};
    const custom_data: Record<string, unknown> = {};
    if (typeof cd.value === "number" && cd.value >= 0 && cd.value < 10000) custom_data.value = Math.round(cd.value * 100) / 100;
    if (["EUR", "USD"].includes(String(cd.currency).toUpperCase())) custom_data.currency = String(cd.currency).toUpperCase();
    if (Array.isArray(cd.contents)) {
      custom_data.contents = cd.contents.slice(0, 20).map((c: any) => ({ id: s(c.id, 60), quantity: Math.max(1, Math.min(99, Number(c.quantity) || 1)), item_price: Number(c.item_price) || undefined }));
      custom_data.content_ids = (custom_data.contents as any[]).map((c) => c.id);
      custom_data.content_type = "product";
      custom_data.num_items = (custom_data.contents as any[]).reduce((a, c) => a + c.quantity, 0);
    }
    const event = { event_name: name, event_time: eventTime, event_id: eventId, action_source: "website", event_source_url: s(b.event_source_url, 500), user_data, custom_data };
    const token = Deno.env.get(reg.tokenEnv);
    // a TEST code from Events Manager can come from the env (all events) or from one request (manual checks)
    const test = Deno.env.get(reg.testEnv) || (typeof b.test_event_code === "string" && /^TEST[0-9A-Z]{2,12}$/.test(b.test_event_code) ? b.test_event_code : undefined);

    const db = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });
    const safePayload = { ...event, user_data: { ...user_data, client_ip_address: ip ? "set" : undefined } };
    const ins = await db.from("capi_outbox").insert({ event_name: name, event_id: eventId, pixel_id: reg.pixel, event_time: new Date(eventTime * 1000).toISOString(), event_source_url: event.event_source_url, session_id: s(b.session_id, 64), payload: safePayload, status: token ? "queued" : "skipped", last_error: token ? null : "missing token" }).select("id").single();
    if (ins.error) {
      if (ins.error.code === "23505") return json({ ok: true, status: "duplicate" }, h);
      console.error("outbox insert", ins.error.message);
    }
    if (!token) return json({ ok: true, status: "skipped", reason: "missing token" }, h);

    const body: Record<string, unknown> = { data: [event] };
    if (test) body.test_event_code = test;
    let st = 0, txt = "";
    try {
      const r = await fetch(`${GRAPH}/${reg.pixel}/events?access_token=${encodeURIComponent(token)}`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
      st = r.status; txt = await r.text();
    } catch (e) { txt = String(e); }
    let resp: any = {}; try { resp = JSON.parse(txt); } catch { /* */ }
    const sent = st >= 200 && st < 300;
    if (ins.data?.id) await db.from("capi_outbox").update({ status: sent ? "sent" : "failed", attempts: 1, last_status: st, last_error: sent ? null : txt.slice(0, 1000), fbtrace_id: resp.fbtrace_id ?? resp.error?.fbtrace_id ?? null, events_received: resp.events_received ?? null, sent_at: sent ? new Date().toISOString() : null }).eq("id", ins.data.id);
    console.log(name, eventId, sent ? "sent" : `failed ${st} ${txt.slice(0, 300)}`);
    return json({ ok: true, status: sent ? "sent" : "failed", test: !!test }, h);
  } catch (e) {
    console.error("capi error", String(e));
    return json({ ok: true, status: "failed" }, h);
  }
});
