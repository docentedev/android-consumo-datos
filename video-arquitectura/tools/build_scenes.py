#!/usr/bin/env python3
"""Genera los archivos HyperFrames del video 'El aviso que cruza las capas'.

Los HTML resultantes son la fuente editable: este script sólo sirve para
regenerar la serie completa con un formato consistente.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
COMP = ROOT / "compositions"
COMP.mkdir(parents=True, exist_ok=True)
NARRATION_META = ROOT / "assets" / "voice" / "meta.json"

COMMON_CSS = r"""
:root {
  --ground: #0D1117;
  --panel: #161B22;
  --line: #30363D;
  --ink: #F0F6FC;
  --dim: #8B949E;
  --green: #3DDC84;
  --blue: #38BDF8;
  --paper: #F6F1E7;
  --accent: var(--green);
}
* { margin: 0; padding: 0; box-sizing: border-box; }
#root {
  position: absolute;
  inset: 0;
  width: 1920px;
  height: 1080px;
  overflow: hidden;
  background: var(--ground);
  color: var(--ink);
  font-family: Inter, Roboto, sans-serif;
}
.clip { position: absolute; }
.clip .in { width: 100%; height: 100%; }
.chapter {
  position: absolute; left: 1460px; top: 142px; width: 260px;
  text-align: right; font-size: 24px; font-weight: 700;
  letter-spacing: .08em; text-transform: uppercase; color: var(--blue);
}
.headline {
  position: absolute; left: 200px; top: 130px; width: 1150px; height: 82px;
  font-size: 64px; font-weight: 800; letter-spacing: -.02em; line-height: 1.05;
}
.sub {
  position: absolute; left: 200px; top: 222px; width: 1200px; height: 48px;
  font-size: 30px; color: var(--dim);
}
.panel {
  position: absolute; left: 200px; top: 300px; width: 900px; height: 600px;
  background: var(--panel); border: 2px solid var(--line); border-radius: 14px;
  overflow: hidden;
}
.panel-bar {
  position: absolute; left: 0; top: 0; width: 100%; height: 52px;
  background: #21262D; border-bottom: 2px solid var(--line);
  padding: 0 24px; display: flex; align-items: center;
  font-family: 'JetBrains Mono', monospace; font-size: 22px; color: var(--dim);
}
.panel-bar .dot { width: 12px; height: 12px; border-radius: 50%; background: var(--green); margin-right: 14px; }
.code {
  position: absolute; left: 26px; height: 38px; width: 840px;
  font-family: 'JetBrains Mono', monospace; font-size: 28px; line-height: 38px;
  color: #E6EDF3; white-space: pre;
}
.code.hl { background: rgba(61,220,132,.12); border-left: 4px solid var(--green); padding-left: 10px; width: 826px; }
.kw { color: #CF8E6D; }
.str { color: #6A8759; }
.fn { color: #56A8F5; }
.cm { color: #7A7E85; }
.ac { color: var(--green); }
.bl { color: var(--blue); }
.visual { position: absolute; left: 1160px; top: 292px; width: 560px; height: 608px; }
.caption {
  position: absolute; left: 200px; top: 920px; width: 1520px; height: 54px;
  font-size: 30px; font-weight: 700; color: var(--ink);
}
.rule { height: 4px; background: var(--blue); border-radius: 2px; }
.ficha-wrap { position: absolute; inset: 0; }
.ficha-paper {
  position: absolute; left: 0; top: 0; width: 420px; min-height: 250px;
  background: var(--paper); color: #101418; border-radius: 10px;
  box-shadow: 0 14px 34px rgba(0,0,0,.5); transform: rotate(-2deg);
  padding: 18px 22px; font-family: 'JetBrains Mono', monospace;
}
.ficha-tab {
  display: inline-block; background: #101418; color: var(--green);
  font-size: 22px; font-weight: 700; padding: 5px 12px; border-radius: 6px;
  margin-bottom: 14px;
}
.ficha-row { font-size: 22px; line-height: 32px; white-space: pre; }
.ficha-row b { color: #1B5E38; font-weight: 700; }
.node {
  position: absolute; background: var(--panel); border: 2px solid var(--blue);
  border-radius: 12px; padding: 14px 20px; font-size: 26px; font-weight: 700;
}
.node small { display: block; font-size: 20px; font-weight: 400; color: var(--dim); margin-top: 4px; font-family: 'JetBrains Mono', monospace; }
.node.green { border-color: var(--green); color: var(--green); }
.tagline { font-family: 'JetBrains Mono', monospace; font-size: 26px; color: var(--dim); }
.bigword { font-size: 76px; font-weight: 800; letter-spacing: -.03em; line-height: 1.1; }
.check { color: var(--green); font-family: 'JetBrains Mono', monospace; font-size: 27px; line-height: 40px; }
"""

TW = {
    "blur": ('{opacity:0,filter:"blur(8px)"}', '{opacity:1,filter:"blur(0px)",duration:0.16,ease:"power4.out"}'),
    "fade": ('{opacity:0}', '{opacity:1,duration:0.3,ease:"power2.out"}'),
    "xr": ('{opacity:0,x:90}', '{opacity:1,x:0,duration:0.5,ease:"power3.out"}'),
    "xl": ('{opacity:0,x:-90}', '{opacity:1,x:0,duration:0.5,ease:"power3.out"}'),
    "scale": ('{opacity:0,scale:0.9}', '{opacity:1,scale:1,duration:0.4,ease:"back.out(1.4)"}'),
    "line": ('{scaleX:0}', '{scaleX:1,duration:0.4,ease:"power2.out",transformOrigin:"left center"}'),
    "dim": ('{opacity:1}', '{opacity:0.22,duration:0.4,ease:"power2.inOut"}'),
    "outR": ('{opacity:1,x:0}', '{opacity:0,x:320,duration:0.5,ease:"power3.in"}'),
    "outL": ('{opacity:1,x:0}', '{opacity:0,x:-320,duration:0.5,ease:"power3.in"}'),
    "drop": ('{opacity:0,y:-80,scale:0.9}', '{opacity:1,y:0,scale:1,duration:0.55,ease:"expo.out"}'),
    "pop": ('{opacity:0,scale:1.6}', '{opacity:1,scale:1,duration:0.45,ease:"back.out(1.4)"}'),
}


def clip(cid, start, inner, style, anim, scene_dur, dur=None, cls="", attrs=""):
    """Devuelve (html, tween) para un clip con id estable y animación en su hijo."""
    d = scene_dur - start if dur is None else dur
    html = (
        f'<div id="{cid}" class="clip {cls}" data-start="{start:.2f}" '
        f'data-duration="{d:.2f}" style="{style}" {attrs}>'
        f'<div id="{cid}-in" class="in">{inner}</div></div>'
    )
    a, b = TW[anim]
    tween = f'tl.fromTo("#{cid}-in", {a}, {b}, {start:.2f});'
    return html, [tween]


def ficha(cid, x, y, tab, rows, start, anim, scene_dur, dur=None):
    rows_html = "".join(f'<div class="ficha-row">{r}</div>' for r in rows)
    inner = (
        '<div class="ficha-wrap">'
        f'<div class="ficha-paper"><span class="ficha-tab">{tab}</span>{rows_html}</div>'
        '</div>'
    )
    return clip(cid, start, inner, f'left:{x}px;top:{y}px;width:440px;height:280px;', anim, scene_dur, dur)


def code_panel(prefix, filename, entries, scene_dur):
    """entries: (tiempo, línea HTML, highlight)"""
    lines, tws = [], []
    for i, (t, line, hl) in enumerate(entries):
        h, tw = clip(
            f"{prefix}-l{i}", t, line,
            f"left:26px;top:{70 + i * 38}px;", "blur", scene_dur,
        )
        lines.append(h.replace('class="clip "', f'class="clip code{" hl" if hl else ""}"'))
        tws.extend(tw)
    bar, tw = clip(f"{prefix}-bar", 0.4,
                   f'<span class="dot"></span>{filename}', "", "fade", scene_dur)
    tws.extend(tw)
    panel = (
        '<div class="panel">'
        + bar
        + "".join(lines)
        + "</div>"
    )
    return panel, tws


def render(scene):
    sid = scene["id"]
    tweens = "\n      ".join(scene["tweens"])
    header = (
        f'    <div class="chapter">{scene["chapter"]}</div>\n'
        f'    <div class="headline">{scene["title"]}</div>\n'
        f'    <div class="sub">{scene["sub"]}</div>'
    )
    html = f"""<!doctype html>
<template>
  <style>
{COMMON_CSS}
{scene.get('css', '')}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="1920" data-height="1080">
{header}
    {scene['body']}
  </div>
  <script>
    window.__timelines = window.__timelines || {{}};
    const tl = gsap.timeline({{ paused: true }});
    {tweens}
    window.__timelines["{sid}"] = tl;
    tl.seek(0);
  </script>
</template>
"""
    (COMP / f"{sid}.html").write_text(html, encoding="utf-8")


def make(id, chapter, title, sub, dur, pieces):
    """pieces: lista de (html, [tweens]) o strings."""
    body, tweens = [], []
    for p in pieces:
        if isinstance(p, str):
            body.append(p)
        else:
            body.append(p[0])
            tweens.extend(p[1])
    return dict(id=id, chapter=chapter, title=title, sub=sub, dur=dur,
                body="\n    ".join(body), tweens=tweens, css="")


scenes = []

# ---------------------------------------------------------------- S1 hook
s = make("s1_hook", "Gancho", "¿Qué lee la pantalla", "cuando no hay red?", 20, [])
h, t = clip("s1-rule", 4, '<div class="rule" style="width:1080px"></div>',
            "left:200px;top:312px;width:1080px;height:4px;", "line", 20)
s["body"] += "\n    " + h; s["tweens"] += t
h, t = clip("s1-path", 4.4,
            '<div class="tagline">HTTPS → DTO → <span class="ac">Room</span> → Flow → UI</div>',
            "left:200px;top:340px;width:1000px;height:44px;", "blur", 20)
s["body"] += "\n    " + h; s["tweens"] += t
h, t = ficha("s1-ficha", 1180, 420, "Notice · notice_1",
             ["<b>text</b> Texto de aviso", "<b>createdAt</b> 2025-01-01T10:00:00Z",
              "<b>email</b> user@test.com"], 0, "drop", 20)
s["body"] += "\n    " + h; s["tweens"] += t
h, t = clip("s1-q", 1.2, '<div class="bigword">¿Qué lee<br>la pantalla<br><span class="ac">sin red?</span></div>',
            "left:200px;top:400px;width:900px;height:300px;", "blur", 20)
s["body"] += "\n    " + h; s["tweens"] += t
h, t = clip("s1-note", 9, '<div class="tagline">Un aviso real del repo · <span class="bl">13 @Test</span></div>',
            "left:200px;top:840px;width:900px;height:40px;", "blur", 20)
s["body"] += "\n    " + h; s["tweens"] += t
h, t = clip("s1-out", 17.2, '<div class="ficha-wrap"><div class="ficha-paper"><span class="ficha-tab">Notice</span><div class="ficha-row">Texto de aviso</div></div></div>',
            "left:1180px;top:420px;width:440px;height:280px;", "outR", 20)
s["body"] += "\n    " + h; s["tweens"] += t
scenes.append(s)

# ---------------------------------------------------------------- S2 Hilt
s = make("s2_bootstrap", "Capítulo 1", "Hilt construye el grafo", "Una app, tres módulos, doce proveedores", 50, [])
p, ts = code_panel("s2-code", "ConsumoDatosApp.kt · MainActivity.kt · di/", [
    (2.0, '<span class="kw">@HiltAndroidApp</span> <span class="kw">class</span> ConsumoDatosApp : Application()', False),
    (7.0, '<span class="kw">@AndroidEntryPoint</span> <span class="kw">class</span> MainActivity', False),
    (12.0, 'ContactScreen(viewModel = <span class="fn">hiltViewModel</span>())', False),
    (18.0, '<span class="ac">DatabaseModule</span>  → provideAppDatabase / Dao / LocalDataSource', True),
    (25.0, '<span class="ac">NetworkModule</span>   → OkHttp / Retrofit / ApiServices / Monitor', True),
    (32.0, '<span class="ac">RepositoryModule</span> → @Binds NoticeRepository / SendEmailRepository', True),
], 50)
s["body"] += "\n    " + p; s["tweens"] += ts
h, t = clip("s2-count", 39, '<div class="bigword" style="font-size:60px"><span class="ac">12</span> proveedores<br><span class="bl">3</span> módulos · <span class="ac">1</span> grafo</div>',
            "left:1180px;top:340px;width:520px;height:220px;", "scale", 50)
s["body"] += "\n    " + h; s["tweens"] += t
h, t = clip("s2-flow", 43, '<div class="rule" style="width:520px"></div>',
            "left:1180px;top:610px;width:520px;height:4px;", "line", 50)
s["body"] += "\n    " + h; s["tweens"] += t
h, t = ficha("s2-ficha", 1220, 660, "Notice", ["<b>id</b> notice_1"], 44, "xr", 50, dur=5)
s["body"] += "\n    " + h; s["tweens"] += t
h, t = clip("s2-out", 47, '<div class="ficha-wrap"><div class="ficha-paper"><span class="ficha-tab">Notice</span></div></div>',
            "left:1220px;top:660px;width:440px;height:280px;", "outR", 50)
s["body"] += "\n    " + h; s["tweens"] += t
scenes.append(s)

# ---------------------------------------------------------------- S3 dominio
s = make("s3_domain", "Capítulo 2", "Dominio: sin Android", "Ni @Entity, ni @SerializedName, ni Context", 40, [])
p, ts = code_panel("s3-code", "domain/model/Notice.kt · domain/repository/", [
    (2.0, '<span class="kw">data class</span> <span class="fn">Notice</span>(<span class="kw">val</span> id: String, userId: String,', False),
    (4.0, '    email: String, text: String, createdAt: String)', False),
    (8.0, '<span class="kw">interface</span> <span class="fn">NoticeRepository</span> {', True),
    (10.0, '  <span class="kw">suspend fun</span> getNotices(): Result&lt;List&lt;Notice&gt;&gt;', False),
    (12.0, '  <span class="kw">fun</span> observeNotices(): Flow&lt;List&lt;Notice&gt;&gt;', True),
    (14.0, '  <span class="kw">suspend fun</span> refreshNotices(): Result&lt;Unit&gt; }', False),
    (16.0, '<span class="kw">interface</span> <span class="fn">SendEmailRepository</span> {', True),
    (18.0, '  <span class="kw">suspend fun</span> sendEmail(to, subject, body): Result&lt;Unit&gt; }', False),
    (24.0, '<span class="cm">// el dominio no sabe si hay red</span>', False),
], 40)
s["body"] += "\n    " + p; s["tweens"] += ts
h, t = clip("s3-tags", 27, '<div class="tagline">DTO · Entity · <span class="ac">Notice</span><br>3 contratos, 1 modelo puro</div>',
            "left:1180px;top:350px;width:520px;height:120px;", "blur", 40)
s["body"] += "\n    " + h; s["tweens"] += t
h, t = ficha("s3-ficha", 1240, 520, "NoticeEntity → Notice", ["<b>text</b> Texto de aviso"], 30, "scale", 40, dur=8)
s["body"] += "\n    " + h; s["tweens"] += t
h, t = clip("s3-out", 36, '<div class="ficha-wrap"><div class="ficha-paper"><span class="ficha-tab">Notice</span></div></div>',
            "left:1240px;top:520px;width:440px;height:280px;", "outR", 40)
s["body"] += "\n    " + h; s["tweens"] += t
scenes.append(s)

# ---------------------------------------------------------------- S4 red
s = make("s4_network", "Capítulo 3", "Del HTTPS al DTO", "Config → OkHttp → Retrofit → NoticeResponseDto", 80, [])
p, ts = code_panel("s4-code", "Config.kt · NetworkModule.kt · NoticeApiService.kt", [
    (2.0, '<span class="kw">enum class</span> <span class="fn">Config</span>(<span class="kw">val</span> url: String, <span class="kw">val</span> key: String)', False),
    (4.0, '  PRODUCTION(', False),
    (5.0, '    <span class="str">"https://app.claudioviajando.com/api/saas"</span>,', False),
    (6.0, '    <span class="str">"********"</span>)', False),
    (8.0, '<span class="kw">object</span> Endpoints {', False),
    (9.0, '  GET_NOTICE = <span class="str">"notices"</span>', False),
    (10.0, '  SEND_EMAIL = <span class="str">"send-email"</span> }', False),
    (13.0, 'OkHttpClient.Builder().<span class="fn">addInterceptor</span> { chain →', True),
    (15.0, '  chain.request().newBuilder()', False),
    (17.0, '    .<span class="fn">addHeader</span>(<span class="str">"authorization"</span>, <span class="str">"ApiKey ********"</span>)', True),
    (19.0, '    .<span class="fn">addHeader</span>(<span class="str">"Content-Type"</span>, <span class="str">"application/json"</span>)', False),
    (21.0, '  chain.proceed(request) }.<span class="fn">addInterceptor</span>(logging BODY)', False),
    (27.0, 'Retrofit.Builder().<span class="fn">baseUrl</span>(baseUrl).<span class="fn">client</span>(okHttp)', False),
    (29.0, '  .<span class="fn">addConverterFactory</span>(GsonConverterFactory.create())', False),
    (33.0, '<span class="kw">@GET</span>(Endpoints.GET_NOTICE)', False),
    (35.0, '<span class="kw">suspend fun</span> <span class="fn">getNotices</span>(): NoticeResponseDto', True),
    (39.0, '<span class="kw">data class</span> <span class="fn">NoticeResponseDto</span>(', False),
    (40.0, '  items, total, page, limit, pages)', False),
    (47.0, '<span class="cm">// paginación recibida, todavía no usada</span>', False),
    (70.0, '<span class="cm">// 1 header · 1 DTO · 0 acoplamiento</span>', False),
], 80)
s["body"] += "\n    " + p; s["tweens"] += ts
for i, (label, t) in enumerate([("Config", 54), ("OkHttp", 57), ("Retrofit", 60), ("API HTTPS", 63), ("DTO", 66)]):
    h, tw = clip(f"s4-pipe{i}", t, f'<div class="node {"green" if i == 4 else ""}">{label}</div>',
                 f"left:{1160 + (i % 2) * 285}px;top:{300 + (i // 2) * 140}px;width:270px;", "scale", 80)
    s["body"] += "\n    " + h; s["tweens"] += tw
h, t = ficha("s4-ficha", 1230, 690, "NoticeDto", ["<b>user_id</b> user_123"], 71, "xr", 80, dur=8)
s["body"] += "\n    " + h; s["tweens"] += t
h, t = clip("s4-out", 77, '<div class="ficha-wrap"><div class="ficha-paper"><span class="ficha-tab">NoticeDto</span></div></div>',
            "left:1230px;top:690px;width:440px;height:280px;", "outR", 80)
s["body"] += "\n    " + h; s["tweens"] += t
scenes.append(s)

# ---------------------------------------------------------------- S5 mapeo
s = make("s5_mapping", "Capítulo 4", "Tres nombres, un dato", "DTO ≠ Entity ≠ Notice", 60, [])
p, ts = code_panel("s5-code", "NoticeDto.kt · NoticeEntity.kt · NoticeRepositoryImpl.kt", [
    (2.0, '<span class="kw">data class</span> <span class="fn">NoticeDto</span>(<span class="kw">val</span> user_id, <span class="kw">val</span> created_at)', False),
    (5.0, '<span class="kw">@SerializedName</span>(<span class="str">"user_id"</span>) <span class="kw">val</span> userId: String?', False),
    (12.0, '<span class="kw">fun</span> NoticeDto.<span class="fn">toEntity</span>(): NoticeEntity', True),
    (16.0, '  = NoticeEntity(id = id ?: <span class="str">""</span>, userId = userId.<span class="fn">orEmpty</span>() …)', False),
    (22.0, '<span class="cm">// los campos nulos del JSON se vuelven ""</span>', False),
    (28.0, '<span class="kw">fun</span> NoticeEntity.<span class="fn">toDomain</span>(): Notice', True),
    (32.0, '  = Notice(id, userId, email, text, createdAt)', False),
    (45.0, 'response.items.<span class="fn">map</span> { it.<span class="fn">toEntity</span>() } → saveNotices(...)', False),
], 60)
s["body"] += "\n    " + p; s["tweens"] += ts
for i, (lab, t) in enumerate([("NoticeDto", 2), ("NoticeEntity", 16), ("Notice", 32)]):
    h, tw = clip(f"s5-tag{i}", t, f'<div class="node {"green" if i == 2 else ""}">{lab}</div>',
                 f"left:1180px;top:{300 + i * 120}px;width:400px;", "xr" if i else "scale", 60)
    s["body"] += "\n    " + h; s["tweens"] += tw
h, t = clip("s5-neq", 39, '<div class="bigword" style="font-size:44px">DTO <span class="ac">≠</span> Entity <span class="ac">≠</span> Notice</div>',
            "left:200px;top:930px;width:1100px;height:60px;", "blur", 60)
s["body"] += "\n    " + h; s["tweens"] += t
h, t = ficha("s5-ficha", 1250, 650, "Notice", ["<b>text</b> Texto de aviso"], 40, "scale", 60, dur=8)
s["body"] += "\n    " + h; s["tweens"] += t
h, t = clip("s5-out", 55, '<div class="ficha-wrap"><div class="ficha-paper"><span class="ficha-tab">Notice</span></div></div>',
            "left:1250px;top:650px;width:440px;height:280px;", "outR", 60)
s["body"] += "\n    " + h; s["tweens"] += t
scenes.append(s)

# ---------------------------------------------------------------- S6 repo
s = make("s6_repository", "Capítulo 5", "Repositorio = SSOT", "Dos caminos, una sola fuente", 70, [])
p, ts = code_panel("s6-code", "data/repository/NoticeRepositoryImpl.kt", [
    (3.0, '<span class="cm">// LEER · la UI observa la BD local</span>', True),
    (5.0, '<span class="kw">override fun</span> <span class="fn">observeNotices</span>(): Flow&lt;List&lt;Notice&gt;&gt;', False),
    (7.0, '  = localDataSource.getNotices().map { entities →', False),
    (9.0, '      entities.map { it.<span class="fn">toDomain</span>() } }', False),
    (16.0, '<span class="cm">// ESCRIBIR · la red sólo actualiza la BD</span>', True),
    (18.0, '<span class="kw">override suspend fun</span> <span class="fn">refreshNotices</span>(): Result&lt;Unit&gt;', False),
    (22.0, '  = <span class="fn">runCatching</span> {', False),
    (26.0, '      val res = remoteDataSource.getNotices()', False),
    (28.0, '      localDataSource.<span class="fn">saveNotices</span>(res.items.map { it.<span class="fn">toEntity</span>() })', True),
    (54.0, '<span class="check">assertEquals("Texto de aviso", notice.text)</span>', True),
], 70)
s["body"] += "\n    " + p; s["tweens"] += ts
for i, (lab, t, color) in enumerate([
    ("LEER · Room → Flow → UI", 10, "green"), ("ESCRIBIR · HTTP → Room", 30, "blue"), ("Room = SSOT", 35, "green")
]):
    h, tw = clip(f"s6-lane{i}", t, f'<div class="node {color}">{lab}</div>',
                 f"left:1180px;top:{320 + i * 140}px;width:490px;", "xr", 70)
    s["body"] += "\n    " + h; s["tweens"] += tw
h, t = clip("s6-claim", 41, '<div class="tagline" style="font-size:28px">La UI lee <span class="ac">Room</span>.<br>La red sólo lo actualiza.</div>',
            "left:1160px;top:770px;width:540px;height:90px;", "blur", 70)
s["body"] += "\n    " + h; s["tweens"] += t
h, t = clip("s6-result", 47, '<div class="node green" style="width:240px">Result&lt;T&gt;</div>',
            "left:1300px;top:700px;width:260px;", "pop", 70)
s["body"] += "\n    " + h; s["tweens"] += t
scenes.append(s)

# ---------------------------------------------------------------- S7 room
s = make("s7_room", "Capítulo 6", "Room: una tabla, un Flow", "consumo_datos.db · version 1", 60, [])
p, ts = code_panel("s7-code", "NoticeEntity.kt · NoticeDao.kt · DatabaseModule.kt", [
    (2.0, '<span class="kw">@Entity</span>(tableName = <span class="str">"notices"</span>)', False),
    (4.0, '<span class="kw">data class</span> <span class="fn">NoticeEntity</span>(<span class="kw">@PrimaryKey val</span> id: String,', False),
    (6.0, '  userId, email, text, createdAt: String? = <span class="kw">null</span>)', False),
    (8.0, '<span class="kw">@Query</span>(', True),
    (9.0, '  <span class="str">"SELECT * FROM notices ORDER BY createdAt DESC"</span>)', False),
    (10.0, '<span class="kw">fun</span> <span class="fn">getNotices</span>(): Flow&lt;List&lt;NoticeEntity&gt;&gt;', False),
    (26.0, '<span class="kw">@Insert</span>(<span class="kw">OnConflictStrategy.REPLACE</span>)', True),
    (28.0, '<span class="kw">suspend fun</span> <span class="fn">insertNotices</span>(notices: List&lt;NoticeEntity&gt;)', False),
    (46.0, 'Room.databaseBuilder(ctx, AppDatabase::class.java, <span class="str">"consumo_datos.db"</span>)', False),
    (51.0, '<span class="cm">// INSERT → el Flow re-emite solo</span>', False),
], 60)
s["body"] += "\n    " + p; s["tweens"] += ts
h, t = clip("s7-table", 16, '<div class="node" style="width:520px">notices · 1 fila<br><small>notice_1 · Texto de aviso · 2025-01-01T10:00:00Z</small></div>',
            "left:1170px;top:310px;width:520px;", "scale", 60)
s["body"] += "\n    " + h; s["tweens"] += t
for i, t0 in enumerate([31, 37, 43]):
    h, tw = clip(f"s7-wave{i}", t0, '<div class="rule" style="width:520px"></div>',
                 f"left:1170px;top:{450 + i * 70}px;width:520px;height:4px;", "line", 60)
    s["body"] += "\n    " + h; s["tweens"] += tw
h, t = clip("s7-label", 33, '<div class="tagline">Flow re-emite <span class="ac">3</span> veces</div>',
            "left:1170px;top:630px;width:520px;height:40px;", "blur", 60)
s["body"] += "\n    " + h; s["tweens"] += t
h, t = clip("s7-v", 49, '<div class="bigword" style="font-size:54px">v<span class="ac">1</span> · 1 entidad<br>1 DAO · 2 métodos</div>',
            "left:1170px;top:680px;width:520px;height:130px;", "blur", 60)
s["body"] += "\n    " + h; s["tweens"] += t
scenes.append(s)

# ---------------------------------------------------------------- S8 UI
s = make("s8_viewmodel_ui", "Capítulo 7", "StateFlow → Compose", "Un estado inmutable, una lista", 60, [])
p, ts = code_panel("s8-code", "NoticeViewModel.kt · NoticeScreen.kt", [
    (2.0, '<span class="kw">private val</span> _uiState = MutableStateFlow(NoticeUiState())', False),
    (4.0, '<span class="kw">val</span> uiState: StateFlow&lt;NoticeUiState&gt;', True),
    (6.0, '  = _uiState.<span class="fn">asStateFlow</span>()', False),
    (8.0, 'repository.observeNotices().<span class="fn">collect</span> { list →', False),
    (10.0, '  _uiState.<span class="fn">update</span> { it.copy(notices = list, isLoading = <span class="kw">false</span>) } }', False),
    (22.0, '<span class="kw">val</span> uiState <span class="kw">by</span> viewModel.uiState', False),
    (24.0, '  .<span class="fn">collectAsStateWithLifecycle</span>()', True),
    (28.0, 'LazyColumn { <span class="fn">items</span>(uiState.notices, key = { it.id }) { … } }', False),
], 60)
s["body"] += "\n    " + p; s["tweens"] += ts
phone = (
    '<div style="position:absolute;left:1290px;top:300px;width:380px;height:560px;'
    'background:#0B1017;border:8px solid #30363D;border-radius:36px;overflow:hidden">'
    '<div style="height:34px;background:#21262D"></div>'
    '<div style="padding:20px;font-family:Inter,sans-serif">'
    '<div style="font-size:24px;font-weight:800;margin-bottom:14px">Avisos</div>'
    '<div style="background:#161B22;border:2px solid #30363D;border-radius:12px;padding:16px">'
    '<div style="font-size:22px">Texto de aviso</div>'
    '<div style="font-size:18px;color:#8B949E">2025-01-01T10:00:00Z</div>'
    '</div></div></div>'
)
h, t = clip("s8-phone", 16, phone, "left:1170px;top:290px;width:380px;height:560px;", "scale", 60)
s["body"] += "\n    " + h; s["tweens"] += t
h, t = clip("s8-state", 5, '<div class="node green" style="width:300px">UiState → StateFlow</div>',
            "left:1190px;top:900px;width:340px;", "xr", 60)
s["body"] += "\n    " + h; s["tweens"] += t
h, t = ficha("s8-ficha", 1300, 480, "Notice", ["<b>text</b> Texto de aviso"], 42, "drop", 60, dur=10)
s["body"] += "\n    " + h; s["tweens"] += t
h, t = clip("s8-out", 56, '<div class="ficha-wrap"><div class="ficha-paper"><span class="ficha-tab">Notice</span></div></div>',
            "left:1300px;top:480px;width:440px;height:280px;", "outR", 60)
s["body"] += "\n    " + h; s["tweens"] += t
scenes.append(s)

# ---------------------------------------------------------------- S9 offline
s = make("s9_offline", "Capítulo 8", "Se cae la red", "La ficha sigue en pantalla", 50, [])
p, ts = code_panel("s9-code", "LiveNetworkMonitor.kt · NoticeViewModel.kt · NoticeScreen.kt", [
    (2.0, '<span class="kw">override fun</span> <span class="fn">onAvailable</span>(network) { <span class="fn">trySend</span>(<span class="kw">true</span>) }', True),
    (10.0, '<span class="kw">override fun</span> <span class="fn">onLost</span>(network) { <span class="fn">trySend</span>(<span class="kw">false</span>) }', True),
    (16.0, 'networkMonitor.isOnline.<span class="fn">collect</span> { isOnline →', False),
    (18.0, '  _uiState.<span class="fn">update</span> { it.copy(isOnline = isOnline) }', False),
    (26.0, '  <span class="cm">if (isOnline) refreshNotices()</span> <span class="cm">// no corre</span>', False),
    (36.0, 'repository.observeNotices().<span class="fn">collect</span> { … } <span class="cm">// sí corre</span>', True),
], 50)
s["body"] += "\n    " + p; s["tweens"] += ts
h, t = clip("s9-online", 0.5, '<div class="node green" style="width:260px">● online</div>',
            "left:1180px;top:310px;width:300px;", "fade", 50, dur=11)
s["body"] += "\n    " + h; s["tweens"] += t
h, t = clip("s9-offline", 12, '<div class="node" style="width:260px;border-color:#8B949E;color:#8B949E">○ offline</div>',
            "left:1180px;top:310px;width:300px;", "pop", 50)
s["body"] += "\n    " + h; s["tweens"] += t
s["tweens"].append('tl.to("#s9-online-in",{opacity:0,duration:0.4,ease:"power2.inOut"},10.5);')
banner = (
    '<div style="background:#3B1D1D;border:2px solid #FF5252;border-radius:10px;'
    'padding:16px;font-size:22px;color:#FFB4B4">⚡ Modo sin conexión:<br>mostrando avisos guardados localmente.</div>'
)
h, t = clip("s9-banner", 18, banner, "left:1170px;top:340px;width:540px;height:130px;", "xr", 50)
s["body"] += "\n    " + h; s["tweens"] += t
for i, t0 in enumerate([36, 41, 46]):
    h, tw = clip(f"s9-wave{i}", t0, '<div class="rule" style="width:520px"></div>',
                 f"left:1170px;top:{920 + i * 18}px;width:520px;height:4px;", "line", 50)
    s["body"] += "\n    " + h; s["tweens"] += tw
h, t = clip("s9-live", 32, '<div class="bigword" style="font-size:52px">La ficha <span class="ac">sigue</span><br>en pantalla</div>',
            "left:1170px;top:790px;width:540px;height:110px;", "blur", 50)
s["body"] += "\n    " + h; s["tweens"] += t
h, t = ficha("s9-ficha", 1280, 500, "Notice", ["<b>text</b> Texto de aviso"], 22, "drop", 50)
s["body"] += "\n    " + h; s["tweens"] += t
scenes.append(s)

# ---------------------------------------------------------------- S10 email + tests
s = make("s10_email_tests", "Capítulo 9", "El segundo viaje", "Enviar correo y probar las capas", 35, [])
p, ts = code_panel("s10-code", "SendEmailApiService.kt · SendEmailRepositoryImpl.kt · tests", [
    (2.0, '<span class="kw">@POST</span>(Endpoints.SEND_EMAIL)', False),
    (4.0, '<span class="kw">suspend fun</span> <span class="fn">sendEmail</span>(<span class="kw">@Body</span> request: SendEmailRequestDto)', False),
    (6.0, '<span class="kw">suspend fun</span> <span class="fn">sendEmail</span>(to, subject, body) = <span class="fn">runCatching</span> {', True),
    (11.0, '  SendEmailRequestDto(to,', False),
    (13.0, '    emailSubject = subject, messageBody = body)', False),
    (16.0, '<span class="cm">// JSON: to · subject · text</span>', False),
    (21.0, '<span class="check">13 @Test en el repo</span>', True),
    (26.0, '<span class="check">BUILD SUCCESSFUL</span> <span class="cm">(guía de tests)</span>', False),
    (30.0, '6 fakes + MainDispatcherRule', False),
], 35)
s["body"] += "\n    " + p; s["tweens"] += ts
h, t = clip("s10-arrow", 8, '<div class="rule" style="width:520px"></div>',
            "left:1170px;top:640px;width:520px;height:4px;", "line", 35)
s["body"] += "\n    " + h; s["tweens"] += t
h, t = clip("s10-post", 12, '<div class="node green" style="width:400px">POST send-email<br><small>ApiKey en el header</small></div>',
            "left:1170px;top:680px;width:440px;", "scale", 35)
s["body"] += "\n    " + h; s["tweens"] += t
h, t = clip("s10-seal", 24, '<div class="node green" style="width:360px;font-size:36px">✓ 13 / 0</div>',
            "left:1180px;top:800px;width:400px;", "pop", 35)
s["body"] += "\n    " + h; s["tweens"] += t
scenes.append(s)

# ---------------------------------------------------------------- S11 cierre
s = make("s11_claim", "Cierre", "La UI lee Room.", "La red sólo lo actualiza", 15, [])
for i, lab in enumerate(["REST", "OkHttp", "Retrofit", "Repo", "Room", "Flow", "VM", "UI"]):
    h, tw = clip(f"s11-n{i}", 0.4 + i * 0.14,
                 f'<div class="node {"green" if lab in ("Room", "Flow") else ""}" style="font-size:24px;padding:10px 14px">{lab}</div>',
                 f"left:{200 + i * 190}px;top:330px;width:170px;", "scale", 15)
    s["body"] += "\n    " + h; s["tweens"] += tw
h, t = clip("s11-monitor", 1.8, '<div class="node" style="font-size:22px">NetworkMonitor</div>',
            "left:700px;top:490px;width:300px;", "xr", 15)
s["body"] += "\n    " + h; s["tweens"] += t
h, t = clip("s11-claim", 2.4, '<div class="bigword" style="font-size:66px">La UI lee <span class="ac">Room</span>.<br>La red sólo lo actualiza.</div>',
            "left:200px;top:620px;width:1520px;height:180px;", "blur", 15)
s["body"] += "\n    " + h; s["tweens"] += t
scenes.append(s)

for sc in scenes:
    render(sc)

INDEX = """<!doctype html>
<html lang="es" data-resolution="landscape"
  data-composition-variables='[{{"id":"accent","type":"color","label":"Color de acento","default":"#3DDC84"}},{{"id":"noticeText","type":"string","label":"Texto del aviso","default":"Texto de aviso"}},{{"id":"claim","type":"string","label":"Claim final","default":"La UI lee Room. La red sólo lo actualiza."}}]'>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>El aviso que cruza las capas — Arquitectura ConsumoDatos</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      :root {{ --ground: #0D1117; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1920px; height: 1080px; overflow: hidden; background: var(--ground); }}
      #root {{ position: relative; width: 1920px; height: 1080px; overflow: hidden; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="540"
         data-width="1920" data-height="1080">
{hosts}
{audios}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
"""
start = 0
hosts = []
for sc in scenes:
    hosts.append(
        f'      <div id="{sc["id"]}" data-composition-id="{sc["id"]}" '
        f'data-composition-src="compositions/{sc["id"]}.html" '
        f'data-start="{start}" data-duration="{sc["dur"]}" '
        f'data-track-index="0" data-track-kind="graphics"></div>'
    )
    start += sc["dur"]
assert start == 540, start
audios = []
if NARRATION_META.exists():
    meta = json.loads(NARRATION_META.read_text(encoding="utf-8"))
    for voice in meta["scenes"]:
        audios.append(
            f'      <audio id="voice-{voice["id"]}" class="clip" '
            f'src="{voice["file"]}" data-start="{voice["start"]}" '
            f'data-duration="{voice["duration"]:.2f}" data-volume="1" '
            f'data-track-index="1"></audio>'
        )
(ROOT / "index.html").write_text(
    INDEX.format(hosts="\n".join(hosts), audios="\n".join(audios)), encoding="utf-8"
)
print(f"Generadas {len(scenes)} escenas, {start} s, {start * 30} frames, "
      f"{len(audios)} pistas de voz")
