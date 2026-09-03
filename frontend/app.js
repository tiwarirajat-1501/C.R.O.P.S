/**
 * C.R.O.P.S. — Modern 3D Frontend Application Logic
 * Implements 3D Parallax Tilt physics, real-time prediction orchestration,
 * commercial fertilizer calculations, economics, and printable Soil Health Card export.
 */

// Exhibition Presets Dictionary
const PRESETS = {
    gangetic: {
        N: 85, P: 50, K: 40, ph: 6.6, temp: 26.0, humidity: 82, rain: 210,
        region: "West Bengal (Hooghly / Burdwan)"
    },
    deccan: {
        N: 120, P: 45, K: 20, ph: 6.8, temp: 24.5, humidity: 80, rain: 80,
        region: "Maharashtra (Nashik / Vidarbha)"
    },
    semiarid: {
        N: 20, P: 55, K: 20, ph: 6.2, temp: 28.0, humidity: 55, rain: 50,
        region: "Gujarat (Anand / Saurashtra)"
    },
    coastal: {
        N: 22, P: 18, K: 32, ph: 6.0, temp: 27.5, humidity: 95, rain: 175,
        region: "Kerala (Wayanad / Palakkad)"
    },
    orchard: {
        N: 22, P: 138, K: 198, ph: 5.9, temp: 22.0, humidity: 92, rain: 112,
        region: "Punjab (Ludhiana)"
    },
    coffee: {
        N: 100, P: 30, K: 30, ph: 6.8, temp: 25.5, humidity: 68, rain: 160,
        region: "Karnataka (Bengaluru / Mandya)"
    }
};

let currentPredictionData = null;

document.addEventListener("DOMContentLoaded", () => {
    init3DParallaxTilt();
    initSliders();
    initPresets();
    initTabs();
    initWeatherRegions();
    initPredictAction();
    initDownloadCard();
    loadModelMetrics();

    // Trigger initial prediction for immediate live exhibition showcase
    runPrediction();
});

/* ==========================================================================
   1. 3D PARALLAX TILT PHYSICS
   ========================================================================== */
function init3DParallaxTilt() {
    const tiltCards = document.querySelectorAll(".tilt-card");

    tiltCards.forEach(card => {
        card.addEventListener("mousemove", (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            // Maximum tilt angle (degrees)
            const maxTilt = 8;
            const rotateX = ((y - centerY) / centerY) * -maxTilt;
            const rotateY = ((x - centerX) / centerX) * maxTilt;

            card.style.transform = `perspective(1000px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) translateY(-4px)`;

            // Card Glare Effect
            const glare = card.querySelector(".card-glare");
            if (glare) {
                const glareX = (x / rect.width) * 100;
                const glareY = (y / rect.height) * 100;
                glare.style.background = `radial-gradient(circle at ${glareX}% ${glareY}%, rgba(255, 255, 255, 0.18) 0%, transparent 60%)`;
            }
        });

        card.addEventListener("mouseleave", () => {
            card.style.transform = "perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0)";
            const glare = card.querySelector(".card-glare");
            if (glare) {
                glare.style.background = "radial-gradient(circle at 50% 0%, rgba(255, 255, 255, 0.12) 0%, transparent 70%)";
            }
        });
    });
}

/* ==========================================================================
   2. SLIDERS, VALUE BUBBLES & DYNAMIC CARD PUSH/TILT
   ========================================================================== */
function initSliders() {
    const consoleCard = document.getElementById("inputConsole");
    let tiltResetTimer = null;

    const sliders = [
        { id: "sliderN", bubble: "valN", unit: " kg/ha" },
        { id: "sliderP", bubble: "valP", unit: " kg/ha" },
        { id: "sliderK", bubble: "valK", unit: " kg/ha" },
        { id: "sliderPh", bubble: "valPh", unit: " pH" },
        { id: "sliderTemp", bubble: "valTemp", unit: " °C" },
        { id: "sliderHumidity", bubble: "valHumidity", unit: " %" },
        { id: "sliderRain", bubble: "valRain", unit: " mm" }
    ];

    sliders.forEach(s => {
        const input = document.getElementById(s.id);
        const bubble = document.getElementById(s.bubble);
        if (!input || !bubble) return;

        let lastVal = parseFloat(input.value);

        input.addEventListener("input", () => {
            const currentVal = parseFloat(input.value);
            bubble.textContent = input.value + s.unit;

            // Push and tilt the console card toward the side being dragged
            if (consoleCard) {
                if (currentVal > lastVal) {
                    // Dragging to the right -> push & tilt right
                    consoleCard.style.transform = "perspective(1000px) rotateY(4deg) translateX(8px)";
                } else if (currentVal < lastVal) {
                    // Dragging to the left -> push & tilt left
                    consoleCard.style.transform = "perspective(1000px) rotateY(-4deg) translateX(-8px)";
                }

                // Reset smoothly back to static rest position 250ms after dragging stops
                clearTimeout(tiltResetTimer);
                tiltResetTimer = setTimeout(() => {
                    consoleCard.style.transform = "perspective(1000px) rotateY(0deg) translateX(0px)";
                }, 250);
            }

            lastVal = currentVal;
        });

        // Reset immediately when mouse/touch is released
        const resetCard = () => {
            if (consoleCard) {
                clearTimeout(tiltResetTimer);
                consoleCard.style.transform = "perspective(1000px) rotateY(0deg) translateX(0px)";
            }
        };

        input.addEventListener("mouseup", resetCard);
        input.addEventListener("touchend", resetCard);
        input.addEventListener("change", resetCard);
    });
}

/* ==========================================================================
   3. EXHIBITION PRESETS
   ========================================================================== */
function initPresets() {
    const buttons = document.querySelectorAll(".preset-chip");
    buttons.forEach(btn => {
        btn.addEventListener("click", () => {
            buttons.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");

            const presetKey = btn.getAttribute("data-preset");
            const data = PRESETS[presetKey];
            if (data) {
                applyPreset(data);
                runPrediction();
            }
        });
    });
}

function applyPreset(p) {
    document.getElementById("sliderN").value = p.N;
    document.getElementById("valN").textContent = p.N + " kg/ha";

    document.getElementById("sliderP").value = p.P;
    document.getElementById("valP").textContent = p.P + " kg/ha";

    document.getElementById("sliderK").value = p.K;
    document.getElementById("valK").textContent = p.K + " kg/ha";

    document.getElementById("sliderPh").value = p.ph;
    document.getElementById("valPh").textContent = p.ph + " pH";

    document.getElementById("sliderTemp").value = p.temp;
    document.getElementById("valTemp").textContent = p.temp + " °C";

    document.getElementById("sliderHumidity").value = p.humidity;
    document.getElementById("valHumidity").textContent = p.humidity + " %";

    document.getElementById("sliderRain").value = p.rain;
    document.getElementById("valRain").textContent = p.rain + " mm";

    const select = document.getElementById("regionSelect");
    for (let opt of select.options) {
        if (opt.value === p.region) {
            select.value = p.region;
            break;
        }
    }
}

/* ==========================================================================
   4. WEATHER & REGIONS
   ========================================================================== */
async function initWeatherRegions() {
    try {
        const res = await fetch("/api/regions");
        const data = await res.json();
        const select = document.getElementById("regionSelect");
        select.innerHTML = "";
        data.regions.forEach(r => {
            const opt = document.createElement("option");
            opt.value = r;
            opt.textContent = r;
            select.appendChild(opt);
        });

        // Set default to Gangetic Alluvial region
        select.value = "West Bengal (Hooghly / Burdwan)";
    } catch (e) {
        console.warn("Could not load regions:", e);
    }

    // Sync button listener
    document.getElementById("syncWeatherBtn").addEventListener("click", async () => {
        const region = document.getElementById("regionSelect").value;
        const pill = document.getElementById("weatherStatus");
        pill.textContent = "Syncing...";
        try {
            const res = await fetch(`/api/weather?region=${encodeURIComponent(region)}`);
            const w = await res.json();

            document.getElementById("sliderTemp").value = w.temperature;
            document.getElementById("valTemp").textContent = w.temperature + " °C";

            document.getElementById("sliderHumidity").value = w.humidity;
            document.getElementById("valHumidity").textContent = w.humidity + " %";

            document.getElementById("sliderRain").value = w.rainfall;
            document.getElementById("valRain").textContent = w.rainfall + " mm";

            pill.textContent = w.is_live ? "Live Sync" : "Cached Preset";
            pill.style.background = w.is_live ? "rgba(0, 245, 155, 0.2)" : "rgba(56, 189, 248, 0.2)";

            runPrediction();
        } catch (e) {
            pill.textContent = "Error";
        }
    });
}

/* ==========================================================================
   5. TABS NAVIGATION
   ========================================================================== */
function initTabs() {
    const tabs = document.querySelectorAll(".tab-btn-3d");
    const panels = document.querySelectorAll(".tab-panel");

    tabs.forEach(tab => {
        tab.addEventListener("click", () => {
            tabs.forEach(t => t.classList.remove("active"));
            panels.forEach(p => p.classList.remove("active"));

            tab.classList.add("active");
            const targetId = tab.getAttribute("data-tab");
            const targetPanel = document.getElementById(targetId);
            if (targetPanel) {
                targetPanel.classList.add("active");
            }
        });
    });
}

/* ==========================================================================
   6. CORE PREDICTION ORCHESTRATION
   ========================================================================== */
function initPredictAction() {
    document.getElementById("runPredictBtn").addEventListener("click", () => {
        runPrediction();
    });
}

async function runPrediction() {
    const btn = document.getElementById("runPredictBtn");
    btn.style.opacity = "0.7";
    btn.querySelector(".btn-text").textContent = "Computing AI Inference...";

    const payload = {
        N: parseFloat(document.getElementById("sliderN").value),
        P: parseFloat(document.getElementById("sliderP").value),
        K: parseFloat(document.getElementById("sliderK").value),
        ph: parseFloat(document.getElementById("sliderPh").value),
        temperature: parseFloat(document.getElementById("sliderTemp").value),
        humidity: parseFloat(document.getElementById("sliderHumidity").value),
        rainfall: parseFloat(document.getElementById("sliderRain").value),
        farm_area: parseFloat(document.getElementById("farmArea").value),
        unit: document.getElementById("areaUnit").value,
        farmer_name: document.getElementById("farmerName").value,
        field_id: document.getElementById("fieldId").value,
        region: document.getElementById("regionSelect").value
    };

    try {
        const res = await fetch("/api/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await res.json();
        currentPredictionData = data;
        renderResults(data);
        renderSoilHealthCardPreview(data, payload);
    } catch (e) {
        console.error("Prediction failed:", e);
    } finally {
        btn.style.opacity = "1";
        btn.querySelector(".btn-text").textContent = "Compute Precision Recommendation";
    }
}

function renderResults(data) {
    const pred = data.prediction;
    const econ = data.economics;
    const fert = data.fertilizer_bags;
    const irrig = data.irrigation;
    const land = data.land;

    // 1. Hero Recommendation Stage
    document.getElementById("resCropIcon").textContent = pred.icon;
    document.getElementById("resCropName").textContent = pred.primary_crop;
    document.getElementById("resCropCategory").textContent = `${pred.category} • Soil Harmony Optimal`;
    document.getElementById("resConfidence").textContent = `${pred.confidence.toFixed(1)}%`;

    // Top-3 Visualizer Bars
    const top3Container = document.getElementById("top3Bars");
    top3Container.innerHTML = "";
    pred.top3_crops.forEach((crop, i) => {
        const prob = pred.top3_probs[i];
        const icon = pred.top3_icons[i];

        const item = document.createElement("div");
        item.className = "top3-item";
        item.innerHTML = `
            <div class="top3-top">
                <span>${icon} ${crop.charAt(0).toUpperCase() + crop.slice(1)}</span>
                <span style="color:#00f0ff; font-weight:800;">${prob.toFixed(1)}%</span>
            </div>
            <div class="top3-bar-bg">
                <div class="top3-bar-fill" style="width: ${prob}%;"></div>
            </div>
        `;
        top3Container.appendChild(item);
    });

    // 2. Tab 1: Fertilizer Bags & Schedule
    document.getElementById("fertSubtitle").textContent = `Scaled for ${land.total_acres.toFixed(2)} Acres (${land.total_hectares.toFixed(2)} Hectares)`;
    document.getElementById("ureaBags").textContent = `${fert.urea_bags} Bags`;
    document.getElementById("ureaKg").textContent = `Total: ${fert.total_urea_kg} kg`;

    document.getElementById("dapBags").textContent = `${fert.dap_bags} Bags`;
    document.getElementById("dapKg").textContent = `Total: ${fert.total_dap_kg} kg`;

    document.getElementById("mopBags").textContent = `${fert.mop_bags} Bags`;
    document.getElementById("mopKg").textContent = `Total: ${fert.total_mop_kg} kg`;

    const phStatus = data.nutrient_gap.ph.status;
    document.getElementById("phStatusText").textContent = phStatus;
    document.getElementById("phRemedyText").textContent = phStatus === "Optimal" ? "Optimal Balance" : (phStatus === "Acidic" ? "Apply Lime" : "Apply Gypsum");

    // Fertilizer Schedule Table
    const scheduleTbody = document.getElementById("scheduleTableBody");
    scheduleTbody.innerHTML = "";
    fert.schedule.forEach(row => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td><strong>${row.stage}</strong></td>
            <td>${row.urea}</td>
            <td>${row.dap}</td>
            <td>${row.mop}</td>
        `;
        scheduleTbody.appendChild(tr);
    });

    // 3. Tab 2: Economics
    document.getElementById("econSubtitle").textContent = `Projected yield, market revenue, and net profit for ${land.total_acres.toFixed(2)} Acres`;
    document.getElementById("econYield").textContent = `${econ.yield_total.toLocaleString()} Qtl`;
    document.getElementById("econYieldPerAcre").textContent = `@ ${econ.yield_per_acre} Qtl/Acre`;

    document.getElementById("econRevenue").textContent = `₹${econ.gross_revenue.toLocaleString()}`;
    document.getElementById("econMsp").textContent = `@ ₹${econ.market_price.toLocaleString()}/Qtl`;

    document.getElementById("econCost").textContent = `₹${econ.total_cost.toLocaleString()}`;
    document.getElementById("econCostPerAcre").textContent = "Total Seed, Fertilizer & Labor";

    document.getElementById("econProfit").textContent = `₹${econ.net_profit.toLocaleString()}`;
    document.getElementById("econRoi").textContent = `ROI: +${econ.roi}%`;

    // Top-3 Economics Table
    const top3EconTbody = document.getElementById("top3EconTableBody");
    top3EconTbody.innerHTML = "";
    econ.top3_comparison.forEach(c => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td><strong>${c.icon} ${c.name}</strong> (${c.confidence}%)</td>
            <td>${c.yield_total.toLocaleString()} Qtl</td>
            <td>₹${c.market_price.toLocaleString()}</td>
            <td>₹${c.cost_total.toLocaleString()}</td>
            <td>₹${c.gross_revenue.toLocaleString()}</td>
            <td style="color:#fbbf24; font-weight:800;">₹${c.net_profit.toLocaleString()}</td>
            <td style="color:#38bdf8; font-weight:800;">+${c.roi}%</td>
        `;
        top3EconTbody.appendChild(tr);
    });

    // 4. Tab 3: Irrigation
    document.getElementById("irrigSeason").textContent = irrig.season;
    document.getElementById("irrigDuration").textContent = irrig.duration_days;
    document.getElementById("irrigWaterNeed").textContent = irrig.water_need;
    document.getElementById("irrigType").textContent = irrig.irrigation_type;
    document.getElementById("irrigTip").textContent = `💡 Agronomic Pro-Tip: ${irrig.water_saving_tip}`;

    document.getElementById("rainCurrent").textContent = `${irrig.rainfall_current.toFixed(1)} mm`;
    document.getElementById("rainIdeal").textContent = `${irrig.rainfall_ideal.toFixed(1)} mm`;

    const rainStatus = document.getElementById("rainStatusBox");
    const rainAdvisory = document.getElementById("rainAdvisoryText");
    if (irrig.rainfall_diff < -20) {
        rainStatus.textContent = `⚠️ Moisture Deficit (${Math.abs(irrig.rainfall_diff)} mm)`;
        rainStatus.style.background = "rgba(244, 63, 94, 0.2)";
        rainStatus.style.border = "1px solid rgba(244, 63, 94, 0.4)";
        rainStatus.style.color = "#fb7185";
        rainAdvisory.textContent = `Provide approximately ${irrig.supplemental_cycles} supplemental irrigations (45-50 mm depth each) during vegetative and flowering stages. Deploy ${irrig.irrigation_type}.`;
    } else if (irrig.rainfall_diff > 40) {
        rainStatus.textContent = `🌧️ Ample Rainfall (+${irrig.rainfall_diff} mm)`;
        rainStatus.style.background = "rgba(56, 189, 248, 0.2)";
        rainStatus.style.border = "1px solid rgba(56, 189, 248, 0.4)";
        rainStatus.style.color = "#38bdf8";
        rainAdvisory.textContent = "Natural precipitation is ample. Prioritize perimeter drainage channels and raised bed furrowing to prevent root waterlogging.";
    } else {
        rainStatus.textContent = "✔ Optimum Moisture Regime";
        rainStatus.style.background = "rgba(16, 185, 129, 0.2)";
        rainStatus.style.border = "1px solid rgba(16, 185, 129, 0.4)";
        rainStatus.style.color = "#34d399";
        rainAdvisory.textContent = "Ambient rainfall is in near-perfect equilibrium with the target crop's ecological requirements.";
    }
}

/* ==========================================================================
   7. OFFICIAL SOIL HEALTH CARD PREVIEW & DOWNLOAD
   ========================================================================== */
async function renderSoilHealthCardPreview(data, payload) {
    const reportPayload = {
        farmer_name: payload.farmer_name,
        field_id: payload.field_id,
        region: payload.region,
        total_acres: data.land.total_acres,
        total_hectares: data.land.total_hectares,
        primary_crop: data.prediction.primary_crop,
        primary_prob: data.prediction.confidence,
        primary_category: data.prediction.category,
        top3_crops: data.prediction.top3_crops,
        top3_probs: data.prediction.top3_probs,
        soil_inputs: {
            N: payload.N, P: payload.P, K: payload.K, ph: payload.ph,
            temp: payload.temperature, humidity: payload.humidity, rain: payload.rainfall
        },
        fertilizer_plan: {
            urea_kg: data.fertilizer_bags.total_urea_kg,
            urea_bags: data.fertilizer_bags.urea_bags,
            dap_kg: data.fertilizer_bags.total_dap_kg,
            dap_bags: data.fertilizer_bags.dap_bags,
            mop_kg: data.fertilizer_bags.total_mop_kg,
            mop_bags: data.fertilizer_bags.mop_bags
        },
        irrigation_plan: data.irrigation,
        economics: data.economics
    };

    try {
        const res = await fetch("/api/report", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(reportPayload)
        });
        const html = await res.text();
        const iframe = document.getElementById("cardPreviewIframe");
        iframe.srcdoc = html;
        iframe.dataset.rawHtml = html;
    } catch (e) {
        console.warn("Could not generate card preview:", e);
    }
}

function initDownloadCard() {
    document.getElementById("downloadCardBtn").addEventListener("click", () => {
        const iframe = document.getElementById("cardPreviewIframe");
        const html = iframe.dataset.rawHtml;
        if (!html) return;

        const blob = new Blob([html], { type: "text/html" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        const crop = currentPredictionData?.prediction?.primary_crop || "Crop";
        const farmer = document.getElementById("farmerName").value.replace(/\s+/g, "_");
        a.href = url;
        a.download = `Soil_Health_Card_${farmer}_${crop}.html`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    });
}

/* ==========================================================================
   8. EXPLAINABLE AI (XAI) METRICS
   ========================================================================== */
async function loadModelMetrics() {
    try {
        const res = await fetch("/api/metrics");
        const data = await res.json();
        const container = document.getElementById("featureImportanceBars");
        container.innerHTML = "";

        const fi = data.feature_importances;
        const sorted = Object.entries(fi).sort((a, b) => b[1] - a[1]);

        sorted.forEach(([feat, score]) => {
            const pct = (score * 100).toFixed(1);
            const row = document.createElement("div");
            row.className = "feat-row";
            row.innerHTML = `
                <div class="feat-label-row">
                    <span>${feat.toUpperCase()}</span>
                    <span style="color:#00f0ff; font-weight:800;">${pct}%</span>
                </div>
                <div class="feat-bar-bg">
                    <div class="feat-bar-fill" style="width: ${pct}%;"></div>
                </div>
            `;
            container.appendChild(row);
        });
    } catch (e) {
        console.warn("Could not load metrics:", e);
    }
}
