// ============ Mode switching ============
const modeBtns = document.querySelectorAll(".mode-btn");
const messagePanel = document.getElementById("message-mode");
const callPanel = document.getElementById("call-mode");

modeBtns.forEach(btn => {
  btn.addEventListener("click", () => {
    modeBtns.forEach(b => { b.classList.remove("active"); b.setAttribute("aria-selected", "false"); });
    btn.classList.add("active");
    btn.setAttribute("aria-selected", "true");
    if (btn.dataset.mode === "message") {
      messagePanel.classList.remove("hidden");
      callPanel.classList.add("hidden");
    } else {
      messagePanel.classList.add("hidden");
      callPanel.classList.remove("hidden");
    }
  });
});

// ============ Sample loader ============
const SAMPLES = [
  `Congratulations! You have been selected for a WORK FROM HOME internship with Global Career Solutions. Registration fee of Rs 999 is required to activate your account. Pay immediately via UPI to confirm your seat, limited slots available!!!`,
  `Dear Meena, thank you for applying for the Web Development internship at Zoho. We would like to invite you for a technical interview on 3rd October via our official Google Meet link sent from careers@zoho.com. Please bring your resume and a valid college ID. No payment is required at any stage.`
];
let sampleIdx = 0;
document.getElementById("sample-btn").addEventListener("click", () => {
  document.getElementById("input-text").value = SAMPLES[sampleIdx % SAMPLES.length];
  sampleIdx++;
});

// ============ Analyze ============
const analyzeBtn = document.getElementById("analyze-btn");
const inputText = document.getElementById("input-text");
const resultEmpty = document.getElementById("result-empty");
const resultContent = document.getElementById("result-content");

analyzeBtn.addEventListener("click", async () => {
  const text = inputText.value.trim();
  if (!text) {
    inputText.focus();
    return;
  }
  const channel = document.querySelector('input[name="channel"]:checked').value;

  analyzeBtn.disabled = true;
  analyzeBtn.textContent = "Analyzing...";

  try {
    const res = await fetch("/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text, channel })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Something went wrong");
    renderResult(text, data);
  } catch (err) {
    alert(err.message);
  } finally {
    analyzeBtn.disabled = false;
    analyzeBtn.textContent = "Analyze Message";
  }
});

function renderResult(text, data) {
  resultEmpty.classList.add("hidden");
  resultContent.classList.remove("hidden");

  // Stamp
  const stamp = document.getElementById("stamp");
  stamp.classList.remove("safe", "mid");
  if (data.verdict === "HIGH RISK") {
    stamp.textContent = "SCAM LIKELY";
  } else if (data.verdict === "SUSPICIOUS") {
    stamp.textContent = "SUSPICIOUS";
    stamp.classList.add("mid");
  } else {
    stamp.textContent = "LIKELY GENUINE";
    stamp.classList.add("safe");
  }
  // retrigger animation
  stamp.style.animation = "none";
  void stamp.offsetWidth;
  stamp.style.animation = "";

  // Dial
  const dialFill = document.getElementById("dial-fill");
  const circumference = 173;
  const offset = circumference - (circumference * data.combined_score) / 100;
  dialFill.style.strokeDashoffset = offset;
  dialFill.style.stroke = data.combined_score >= 65 ? "#a3302a" : data.combined_score >= 35 ? "#9c6b12" : "#2f6f4e";
  document.getElementById("score-number").textContent = Math.round(data.combined_score);

  document.getElementById("rule-score-txt").textContent = data.rule_score + " / 100";
  document.getElementById("ml-score-txt").textContent = data.ml_score !== null ? data.ml_score + " / 100" : "n/a";
  document.getElementById("advice-txt").textContent = data.advice;

  // Annotated text
  renderAnnotated(text, data.findings);

  // Findings list
  const findingsList = document.getElementById("findings-list");
  findingsList.innerHTML = "";
  if (data.findings.length === 0) {
    findingsList.innerHTML = `<li style="border-left-color:#2f6f4e;background:rgba(47,111,78,0.08);">No rule-based red flags matched this text.</li>`;
  } else {
    data.findings.forEach(f => {
      const li = document.createElement("li");
      li.innerHTML = `<span class="f-cat">${f.category} · severity ${f.severity}/5</span>
        <span class="f-match">"${escapeHtml(f.match)}"</span><br>${escapeHtml(f.why)}`;
      findingsList.appendChild(li);
    });
  }

  // Positive findings
  const posList = document.getElementById("positive-list");
  const posWrap = document.getElementById("positive-wrap");
  posList.innerHTML = "";
  if (data.positive_findings.length === 0) {
    posWrap.classList.add("hidden");
  } else {
    posWrap.classList.remove("hidden");
    data.positive_findings.forEach(f => {
      const li = document.createElement("li");
      li.innerHTML = `<span class="f-match">"${escapeHtml(f.match)}"</span><br>${escapeHtml(f.why)}`;
      posList.appendChild(li);
    });
  }
}

function renderAnnotated(text, findings) {
  const container = document.getElementById("annotated-text");
  if (findings.length === 0) {
    container.textContent = text;
    return;
  }
  let html = "";
  let cursor = 0;
  findings.forEach(f => {
    html += escapeHtml(text.slice(cursor, f.start));
    html += `<mark class="flag sev-${f.severity}" title="${escapeHtml(f.why)}">${escapeHtml(text.slice(f.start, f.end))}</mark>`;
    cursor = f.end;
  });
  html += escapeHtml(text.slice(cursor));
  container.innerHTML = html;
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

// ============ Call checklist ============
const callList = document.getElementById("call-checklist");
const flagCountEl = document.getElementById("call-flag-count");
const callVerdictEl = document.getElementById("call-verdict");
let callAnswers = {};

async function loadChecklist() {
  const res = await fetch("/call-checklist");
  const items = await res.json();
  document.getElementById("call-flag-total").textContent = items.length;
  callList.innerHTML = "";
  items.forEach((item, i) => {
    const li = document.createElement("li");
    li.innerHTML = `
      <div>
        <span class="q-text">${i + 1}. ${escapeHtml(item.q)}</span>
        <span class="q-flag">${escapeHtml(item.flag)}</span>
      </div>
      <div class="yn-toggle">
        <button class="yn-btn" data-idx="${i}" data-val="yes">Yes</button>
        <button class="yn-btn" data-idx="${i}" data-val="no">No</button>
      </div>
    `;
    callList.appendChild(li);
  });

  callList.querySelectorAll(".yn-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const idx = btn.dataset.idx;
      const val = btn.dataset.val;
      callAnswers[idx] = val;
      callList.querySelectorAll(`.yn-btn[data-idx="${idx}"]`).forEach(b => {
        b.classList.remove("selected-yes", "selected-no");
      });
      btn.classList.add(val === "yes" ? "selected-yes" : "selected-no");
      updateCallScore(items.length);
    });
  });
}

function updateCallScore(total) {
  const yesCount = Object.values(callAnswers).filter(v => v === "yes").length;
  flagCountEl.textContent = yesCount;
  callVerdictEl.classList.remove("high", "mid", "low");
  if (yesCount >= 3) {
    callVerdictEl.textContent = "HIGH RISK — multiple scam indicators confirmed. Do not pay or share details.";
    callVerdictEl.classList.add("high");
  } else if (yesCount >= 1) {
    callVerdictEl.textContent = "PROCEED WITH CAUTION — verify the company independently before continuing.";
    callVerdictEl.classList.add("mid");
  } else if (Object.keys(callAnswers).length === total) {
    callVerdictEl.textContent = "No red flags confirmed — still verify official channels before sharing sensitive info.";
    callVerdictEl.classList.add("low");
  } else {
    callVerdictEl.textContent = "";
  }
}

loadChecklist();
