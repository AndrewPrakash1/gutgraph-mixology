/* ============================================================================
   AGENT ROOM — grokbot-style parliament chat (grokbot-clone loop.py pattern).

   Live only: GET /agents (roster + mode badge), GET /meals (chips),
   POST /chat/stream (SSE: agent_start, token*, vote, tally, result, error).

   Everything is namespaced under AR / ar*, so it cannot collide with the
   site's own globals in script.js (PRODUCTS, MEALS, currentMeal, ...).
   ========================================================================= */
var AR = {
  agents: [], meals: [], mode: null, states: {}, last: {},
  focused: null, running: false, booted: false
};

/* Served by the backend at :8000, "" is right. Opened straight off disk or on
   another local port, the API still lives at :8000. */
var AR_API = (location.protocol === "file:" ||
              (/^(localhost|127\.0\.0\.1|\[::1\])$/.test(location.hostname) && location.port !== "8000"))
  ? "http://localhost:8000" : "";

function arEl(id) { return document.getElementById(id); }
function arEsc(s) {
  return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
    return ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c];
  });
}
function arAvatar(a) {
  return '<div class="ar-av" style="background:' + (a.color || "#FFD52A") +
         ';color:#170052">' + (a.emoji || "•") + "</div>";
}

function openAgentRoom() {
  arEl("agent-room").setAttribute("data-open", "true");
  arEl("agent-room").setAttribute("aria-hidden", "false");
  document.body.style.overflow = "hidden";
  if (!AR.booted) arBoot();
  setTimeout(function () { var i = arEl("ar-input"); if (i) i.focus(); }, 250);
}
function closeAgentRoom() {
  arEl("agent-room").setAttribute("data-open", "false");
  arEl("agent-room").setAttribute("aria-hidden", "true");
  document.body.style.overflow = "";
}
document.addEventListener("keydown", function (e) {
  if (e.key === "Escape" && arEl("agent-room").getAttribute("data-open") === "true") closeAgentRoom();
});

async function arBoot() {
  AR.booted = true;
  try {
    var a = await (await fetch(AR_API + "/agents")).json();
    AR.agents = a.agents || [];
    AR.mode = a;
    arEl("ar-mode").textContent = a.mode === "live"
      ? "live · " + a.provider + " · " + a.model
      : "engine live · template voice (no api key)";
  } catch (e) { arEl("ar-mode").textContent = "backend unreachable"; }
  try {
    AR.meals = await (await fetch(AR_API + "/meals")).json();
    arEl("ar-meals").innerHTML = AR.meals.map(function (m) {
      return '<button class="ar-chip" type="button" onclick="arChip(' +
             JSON.stringify(m.name).replace(/"/g, "&quot;") + ')">' + arEsc(m.emoji + " " + m.name) + "</button>";
    }).join("");
  } catch (e) {}
  arReset();
}

function arRenderRail() {
  arEl("ar-rail").innerHTML = AR.agents.map(function (a) {
    var st = AR.states[a.handle] || { cls: "idle", label: "idle" };
    var sel = AR.focused === a.handle;
    return '<button class="ar-agent" type="button" aria-pressed="' + sel + '" onclick="arFocus(\'' + a.handle + '\')">' +
      arAvatar(a) +
      '<span style="min-width:0;flex:1">' +
        '<span class="ar-nm">' + arEsc(a.name) + "</span>" +
        '<span class="ar-role">' + arEsc(a.role) + "</span>" +
        '<span class="ar-prev">' + arEsc(AR.last[a.handle] || "listening for the next meal") + "</span>" +
      "</span>" +
      '<span class="ar-st ' + st.cls + '" id="ar-st-' + a.handle + '">' + arEsc(st.label) + "</span>" +
    "</button>";
  }).join("") || '<div class="ar-sys">No agents loaded.</div>';
}
function arState(handle, cls, label) {
  AR.states[handle] = { cls: cls, label: label };   // survives arRenderRail()
  var n = document.getElementById("ar-st-" + handle);
  if (n) { n.className = "ar-st " + cls; n.textContent = label; }
  arRenderRail();
}
function arFocus(handle) {
  AR.focused = handle;
  arRenderRail();
  var b = document.getElementById("ar-bubble-" + handle);
  if (b) b.scrollIntoView({ behavior: "smooth", block: "center" });
}
function arSys(html) {
  var d = document.createElement("div");
  d.className = "ar-sys";
  d.innerHTML = html;
  arEl("ar-inner").appendChild(d);
  arScroll();
}
function arDots(handles) {
  return handles.map(function (h) {
    var a = AR.agents.filter(function (x) { return x.handle === h; })[0] || {};
    return '<i style="background:' + (a.color || "#FFD52A") + '"></i>';
  }).join("");
}
function arUser(text) {
  var d = document.createElement("div");
  d.className = "ar-msg me";
  d.innerHTML = '<div><div class="ar-who" style="text-align:right">You</div>' +
    '<div class="ar-bub">' + arEsc(text) + "</div></div>";
  arEl("ar-inner").appendChild(d);
  arScroll();
}
function arBubble(a) {
  var d = document.createElement("div");
  d.className = "ar-msg";
  d.id = "ar-bubble-" + a.handle;
  d.innerHTML = arAvatar(a) +
    '<div style="min-width:0">' +
      '<div class="ar-who">' + arEsc(a.name) + " · " + arEsc(a.role) + "</div>" +
      '<div class="ar-bub typing" id="ar-text-' + a.handle + '" data-text=""></div>' +
      '<div class="ar-tags" id="ar-tags-' + a.handle + '"></div>' +
    "</div>";
  arEl("ar-inner").appendChild(d);
  return d;
}
function arAppend(handle, delta) {
  var n = document.getElementById("ar-text-" + handle);
  if (!n) return;
  n.dataset.text = (n.dataset.text || "") + delta;   // never read back innerText
  n.textContent = n.dataset.text;
  arScroll();
}
function arScroll() { var t = arEl("ar-thread"); t.scrollTop = t.scrollHeight; }

function arReset() {
  arEl("ar-inner").innerHTML = "";
  AR.states = {}; AR.last = {}; AR.focused = null;
  arRenderRail();
  arSys("Room ready · " + AR.agents.length + " agents on the roster. Tell them what you ate, or pick a meal below.");
}
function arChip(name) { arEl("ar-input").value = name; arSend(null); }

async function arSend(ev) {
  if (ev) ev.preventDefault();
  if (AR.running) return;
  var text = (arEl("ar-input").value || "").trim();
  if (!text) return;
  AR.running = true;
  arEl("ar-send").disabled = true;
  arEl("ar-input").value = "";
  arUser(text);
  AR.agents.forEach(function (a) { arState(a.handle, "idle", "waiting"); });
  var live = {};

  try {
    var res = await fetch(AR_API + "/chat/stream", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text })
    });
    if (!res.ok || !res.body) throw new Error("HTTP " + res.status);
    var reader = res.body.getReader(), dec = new TextDecoder(), buf = "";
    for (;;) {
      var chunk = await reader.read();
      if (chunk.done) break;
      buf += dec.decode(chunk.value, { stream: true });
      var frames = buf.split("\n\n");
      buf = frames.pop();
      for (var i = 0; i < frames.length; i++) {
        var line = frames[i].split("\n").filter(function (l) { return l.indexOf("data:") === 0; })[0];
        if (!line) continue;
        var obj;
        try { obj = JSON.parse(line.slice(5).trim()); } catch (e) { continue; }
        arHandle(obj, live);
      }
    }
  } catch (err) {
    arSys('<span style="color:var(--ar-pink)">Could not reach the backend (' +
          arEsc(err.message) + "). Is the server running on :8000?</span>");
  } finally {
    AR.running = false;
    arEl("ar-send").disabled = false;
    arEl("ar-input").focus();
  }
}

function arHandle(ev, live) {
  switch (ev.event) {
    case "agent_start":
      live[ev.agent.handle] = arBubble(ev.agent);
      arState(ev.agent.handle, "thinking", "thinking");
      break;
    case "token":
      if (ev.agent === "MIXOLOGIST") {
        if (!live.MIXOLOGIST) {
          live.MIXOLOGIST = arBubble({
            handle: "MIXOLOGIST", name: "Mixologist",
            role: "orchestrator", emoji: "🍸", color: "#70B96B"
          });
          arState("MIXOLOGIST", "thinking", "speaking");
        }
        arAppend("MIXOLOGIST", ev.delta);
      } else {
        arAppend(ev.agent, ev.delta);
      }
      break;
    case "vote": {
      var t = arEl("ar-text-" + ev.agent);
      if (t) t.classList.remove("typing");
      var tags = arEl("ar-tags-" + ev.agent);
      if (tags) {
        var warm = ev.vote === "no";
        tags.innerHTML = '<span class="ar-tag ' + (warm ? "no" : "yes") + '">' +
          (warm ? "objects" : "approves") + '</span><span class="ar-tag voice">' +
          arEsc(ev.source === "template" ? "template voice" : ev.source) + "</span>";
      }
      AR.last[ev.agent] = ev.reason;
      arState(ev.agent, ev.vote === "no" ? "no" : "yes", ev.vote === "no" ? "objects" : "approves");
      break;
    }
    case "error": {
      var b = document.getElementById("ar-bubble-" + ev.agent);
      if (b) {
        var line = document.createElement("div");
        line.className = "ar-err";
        line.textContent = "model call failed — " + (ev.provider || "provider") +
          (ev.status ? " " + ev.status : "") + ", fell back to template voice";
        b.lastElementChild.appendChild(line);
      }
      break;
    }
    case "tally": {
      var yes = ev.votes.filter(function (v) { return v.vote === "yes"; });
      var no = ev.votes.filter(function (v) { return v.vote === "no"; });
      arSys("<b>" + ev.yes + " of " + ev.total + "</b> approve " +
            arDots(yes.map(function (v) { return v.agent; })) +
            (no.length ? " · " + no.length + " object " + arDots(no.map(function (v) { return v.agent; })) : ""));
      break;
    }
    case "result": arRx(ev.result); break;
    case "unknown_meal":
      arSys("That meal isn't in the demo set — the Mixologist listed what it knows above.");
      break;
  }
}

function arRx(r) {
  var d = r.drink;
  var card = document.createElement("div");
  card.className = "ar-rx";
  card.innerHTML =
    '<div class="kick">Prescription</div>' +
    "<h3>" + arEsc(d.emoji) + " " + arEsc(d.name) + "</h3>" +
    "<p><b>Gut score " + r.gut_score + "/10</b> · gaps: " + arEsc((r.gaps || []).join(", ") || "none") + "</p>" +
    "<p>" + arEsc(d.prep) + "</p>" +
    '<p style="opacity:.8">' + arEsc(d.explanation) + "</p>" +
    '<div class="ar-kv">' +
      "<div><span>Ingredients</span><b>" + arEsc((d.ingredients || []).join(", ")) + "</b></div>" +
      "<div><span>Shared molecules</span><b>" + d.shared_molecules + "</b></div>" +
      "<div><span>Pairing score</span><b>" + d.similarity_score + "</b></div>" +
      "<div><span>Agents approving</span><b>" + (r.tally ? r.tally.yes + "/" + r.tally.total : "?") + "</b></div>" +
    "</div>" +
    '<p style="opacity:.7;font-size:.76rem">Concept mockup · scores are rule-based heuristics and the votes are simulated — not medical advice.</p>';
  arEl("ar-inner").appendChild(card);
  arScroll();
}
