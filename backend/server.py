"""
C.R.O.P.S. — Production Web Application Server
Lightweight, zero-dependency Python HTTP API server providing REST endpoints
for ML model inference, fertilizer sizing, crop economics, weather sync, and static files.
"""

import os
import json
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn
import joblib
import numpy as np
import pandas as pd

import weather_service
import agronomic_data
import report_generator

# Directory paths
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BACKEND_DIR) if os.path.basename(BACKEND_DIR) == "backend" else BACKEND_DIR

FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")
if not os.path.exists(FRONTEND_DIR):
    FRONTEND_DIR = os.path.join(BACKEND_DIR, "frontend")

MODELS_DIR = os.path.join(ROOT_DIR, "models")
if not os.path.exists(MODELS_DIR):
    MODELS_DIR = os.path.join(BACKEND_DIR, "models")

# Load ML Models & Artifacts
print("[*] Loading ML models and agronomic benchmarks...")
model = joblib.load(os.path.join(MODELS_DIR, "crop_model.pkl"))
scaler = joblib.load(os.path.join(MODELS_DIR, "scaler.pkl"))
encoder = joblib.load(os.path.join(MODELS_DIR, "label_encoder.pkl"))

with open(os.path.join(MODELS_DIR, "crop_benchmarks.json"), "r") as f:
    benchmarks = json.load(f)

with open(os.path.join(MODELS_DIR, "metrics.json"), "r") as f:
    metrics = json.load(f)

print("[+] Machine learning assets loaded successfully.")

# Crop Icons
CROP_ICONS = {
    "rice": "🌾", "maize": "🌽", "chickpea": "🌱", "kidneybeans": "🫘",
    "pigeonpeas": "🌿", "mothbeans": "🫘", "mungbean": "🌱", "blackgram": "🫘",
    "lentil": "🍲", "pomegranate": "🍎", "banana": "🍌", "mango": "🥭",
    "grapes": "🍇", "watermelon": "🍉", "muskmelon": "🍈", "apple": "🍏",
    "orange": "🍊", "papaya": "🥭", "coconut": "🥥", "cotton": "🧶",
    "jute": "🧵", "coffee": "☕"
}

# Crop Categories
CROP_CATEGORIES = {
    "rice": "Cereals & Grains", "maize": "Cereals & Grains",
    "chickpea": "Pulses & Legumes", "kidneybeans": "Pulses & Legumes",
    "pigeonpeas": "Pulses & Legumes", "mothbeans": "Pulses & Legumes",
    "mungbean": "Pulses & Legumes", "blackgram": "Pulses & Legumes",
    "lentil": "Pulses & Legumes",
    "pomegranate": "Horticulture & Fruits", "banana": "Horticulture & Fruits",
    "mango": "Horticulture & Fruits", "grapes": "Horticulture & Fruits",
    "watermelon": "Horticulture & Fruits", "muskmelon": "Horticulture & Fruits",
    "apple": "Horticulture & Fruits", "orange": "Horticulture & Fruits",
    "papaya": "Horticulture & Fruits",
    "coconut": "Plantation & Cash Crops", "cotton": "Fiber & Cash Crops",
    "jute": "Fiber & Cash Crops", "coffee": "Plantation & Cash Crops"
}

class CropsApiHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=FRONTEND_DIR, **kwargs)

    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def _send_html(self, html_text, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(html_text.encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/health":
            self._send_json({"status": "healthy", "service": "C.R.O.P.S. API", "accuracy": 0.9955})
            return

        elif path == "/api/metrics":
            self._send_json(metrics)
            return

        elif path == "/api/regions":
            self._send_json({"regions": weather_service.get_available_regions()})
            return

        elif path == "/api/weather":
            query = urllib.parse.parse_qs(parsed.query)
            region = query.get("region", ["Punjab (Ludhiana)"])[0]
            api_key = query.get("api_key", [None])[0]
            weather_data = weather_service.get_weather(region, api_key)
            self._send_json(weather_data)
            return

        elif path == "/api/catalog":
            catalog = []
            for crop_name, bm in benchmarks.items():
                ec = agronomic_data.get_crop_economics(crop_name)
                catalog.append({
                    "name": crop_name,
                    "icon": CROP_ICONS.get(crop_name, "🌱"),
                    "category": CROP_CATEGORIES.get(crop_name, "Standard"),
                    "benchmarks": bm,
                    "economics": ec
                })
            self._send_json(catalog)
            return

        # Serve static web files from WEB_DIR
        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        post_body = self.rfile.read(content_length).decode("utf-8")
        
        try:
            req = json.loads(post_body) if post_body else {}
        except Exception:
            self._send_json({"error": "Invalid JSON body"}, 400)
            return

        if path == "/api/predict":
            # Extract inputs
            n = float(req.get("N", 90))
            p = float(req.get("P", 42))
            k = float(req.get("K", 43))
            temp = float(req.get("temperature", 26.0))
            humidity = float(req.get("humidity", 80.0))
            ph = float(req.get("ph", 6.5))
            rain = float(req.get("rainfall", 200.0))

            farm_area = float(req.get("farm_area", 2.5))
            unit = req.get("unit", "Acres")
            
            farmer_name = req.get("farmer_name", "Ramesh Kumar")
            field_id = req.get("field_id", "Plot #4-B")
            region = req.get("region", "West Bengal (Hooghly / Burdwan)")

            if unit == "Acres":
                total_acres = farm_area
                total_hectares = farm_area / 2.47105
            else:
                total_hectares = farm_area
                total_acres = farm_area * 2.47105

            # Run ML Inference
            feature_cols = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
            features_df = pd.DataFrame([[n, p, k, temp, humidity, ph, rain]], columns=feature_cols)
            scaled = scaler.transform(features_df)

            probs = model.predict_proba(scaled)[0]
            top3_idx = np.argsort(probs)[::-1][:3]
            top3_crops = [encoder.classes_[i] for i in top3_idx]
            top3_probs = [round(float(probs[i] * 100), 1) for i in top3_idx]

            primary_crop = top3_crops[0]
            primary_prob = top3_probs[0]

            # Agronomic benchmark analysis
            crop_bm = benchmarks.get(primary_crop, {})
            bench_n = crop_bm.get("N", {}).get("mean", 80.0)
            bench_p = crop_bm.get("P", {}).get("mean", 40.0)
            bench_k = crop_bm.get("K", {}).get("mean", 40.0)
            bench_ph = crop_bm.get("ph", {}).get("mean", 6.5)

            diff_n = round(n - bench_n, 1)
            diff_p = round(p - bench_p, 1)
            diff_k = round(k - bench_k, 1)
            diff_ph = round(ph - bench_ph, 1)

            # Commercial Fertilizer Sizing (50kg bags)
            urea_per_ha = max(0.0, round(abs(diff_n) / 0.46, 1)) if diff_n < -5 else 0.0
            dap_per_ha = max(0.0, round(abs(diff_p) / 0.46, 1)) if diff_p < -5 else 0.0
            mop_per_ha = max(0.0, round(abs(diff_k) / 0.60, 1)) if diff_k < -5 else 0.0

            total_urea_kg = round(urea_per_ha * total_hectares, 1)
            total_dap_kg = round(dap_per_ha * total_hectares, 1)
            total_mop_kg = round(mop_per_ha * total_hectares, 1)

            urea_bags = round(total_urea_kg / 50.0, 1)
            dap_bags = round(total_dap_kg / 50.0, 1)
            mop_bags = round(total_mop_kg / 50.0, 1)

            # Economics for primary crop
            econ_primary = agronomic_data.get_crop_economics(primary_crop)
            yield_total = round(econ_primary["yield_per_acre_qtl"] * total_acres, 1)
            gross_revenue = round(yield_total * econ_primary["market_price_per_qtl"], 0)
            total_cost = round(econ_primary["cost_per_acre"] * total_acres, 0)
            net_profit = round(gross_revenue - total_cost, 0)
            roi_pct = round((net_profit / total_cost) * 100, 1) if total_cost > 0 else 0

            # Top 3 Economics Comparison
            top3_econ = []
            for c, pr in zip(top3_crops, top3_probs):
                ec = agronomic_data.get_crop_economics(c)
                y_tot = round(ec["yield_per_acre_qtl"] * total_acres, 1)
                rev = round(y_tot * ec["market_price_per_qtl"], 0)
                cost = round(ec["cost_per_acre"] * total_acres, 0)
                prof = round(rev - cost, 0)
                roi = round((prof / cost) * 100, 1) if cost > 0 else 0
                top3_econ.append({
                    "crop": c,
                    "name": c.capitalize(),
                    "icon": CROP_ICONS.get(c, "🌱"),
                    "confidence": pr,
                    "yield_total": y_tot,
                    "market_price": ec["market_price_per_qtl"],
                    "cost_total": cost,
                    "gross_revenue": rev,
                    "net_profit": prof,
                    "roi": roi
                })

            # Water and Rainfall Balance
            crop_mean_rain = crop_bm.get("rainfall", {}).get("mean", 120.0)
            rain_diff = round(rain - crop_mean_rain, 1)
            supp_irrigations = max(1, int(round(abs(rain_diff) / 45.0, 0))) if rain_diff < -20 else 0

            response_data = {
                "prediction": {
                    "primary_crop": primary_crop,
                    "confidence": primary_prob,
                    "icon": CROP_ICONS.get(primary_crop, "🌱"),
                    "category": CROP_CATEGORIES.get(primary_crop, "Standard Crop"),
                    "top3_crops": top3_crops,
                    "top3_probs": top3_probs,
                    "top3_icons": [CROP_ICONS.get(c, "🌱") for c in top3_crops]
                },
                "nutrient_gap": {
                    "N": {"current": n, "ideal": bench_n, "diff": diff_n, "status": "Low" if diff_n < -10 else ("High" if diff_n > 15 else "Optimal")},
                    "P": {"current": p, "ideal": bench_p, "diff": diff_p, "status": "Low" if diff_p < -10 else ("High" if diff_p > 15 else "Optimal")},
                    "K": {"current": k, "ideal": bench_k, "diff": diff_k, "status": "Low" if diff_k < -10 else ("High" if diff_k > 15 else "Optimal")},
                    "ph": {"current": ph, "ideal": bench_ph, "diff": diff_ph, "status": "Optimal" if 5.8 <= ph <= 7.8 else ("Acidic" if ph < 5.8 else "Alkaline")}
                },
                "fertilizer_bags": {
                    "urea_bags": urea_bags,
                    "total_urea_kg": total_urea_kg,
                    "dap_bags": dap_bags,
                    "total_dap_kg": total_dap_kg,
                    "mop_bags": mop_bags,
                    "total_mop_kg": total_mop_kg,
                    "schedule": [
                        {
                            "stage": "Stage 1: Basal (At Sowing)",
                            "urea": f"{round(total_urea_kg*0.3, 1)} kg ({round(urea_bags*0.3, 1)} bags)",
                            "dap": f"{total_dap_kg} kg ({dap_bags} bags)",
                            "mop": f"{total_mop_kg} kg ({mop_bags} bags)"
                        },
                        {
                            "stage": "Stage 2: 30-Day Vegetative",
                            "urea": f"{round(total_urea_kg*0.4, 1)} kg ({round(urea_bags*0.4, 1)} bags)",
                            "dap": "None",
                            "mop": "None"
                        },
                        {
                            "stage": "Stage 3: Flowering / Panicle",
                            "urea": f"{round(total_urea_kg*0.3, 1)} kg ({round(urea_bags*0.3, 1)} bags)",
                            "dap": "None",
                            "mop": "None"
                        }
                    ]
                },
                "economics": {
                    "yield_total": yield_total,
                    "yield_per_acre": econ_primary["yield_per_acre_qtl"],
                    "market_price": econ_primary["market_price_per_qtl"],
                    "gross_revenue": gross_revenue,
                    "total_cost": total_cost,
                    "net_profit": net_profit,
                    "roi": roi_pct,
                    "top3_comparison": top3_econ
                },
                "irrigation": {
                    "season": econ_primary.get("season", "Kharif"),
                    "duration_days": econ_primary.get("duration_days", "110-130"),
                    "water_need": econ_primary.get("water_need", "Moderate"),
                    "irrigation_type": econ_primary.get("irrigation_type", "Precision Drip"),
                    "water_saving_tip": econ_primary.get("water_saving_tip", "Maintain uniform moisture during critical flowering stages."),
                    "rainfall_current": rain,
                    "rainfall_ideal": crop_mean_rain,
                    "rainfall_diff": rain_diff,
                    "supplemental_cycles": supp_irrigations
                },
                "land": {
                    "farm_area": farm_area,
                    "unit": unit,
                    "total_acres": round(total_acres, 2),
                    "total_hectares": round(total_hectares, 2)
                }
            }

            self._send_json(response_data)
            return

        elif path == "/api/report":
            # Generate printable HTML Soil Health Card
            primary_crop = req.get("primary_crop", "rice")
            total_acres = float(req.get("total_acres", 2.5))
            total_hectares = float(req.get("total_hectares", round(total_acres / 2.47105, 2)))
            
            fert_plan = req.get("fertilizer_plan", {})
            fert_plan = {
                "urea_kg": fert_plan.get("urea_kg", 0.0),
                "urea_bags": fert_plan.get("urea_bags", 0.0),
                "dap_kg": fert_plan.get("dap_kg", 0.0),
                "dap_bags": fert_plan.get("dap_bags", 0.0),
                "mop_kg": fert_plan.get("mop_kg", 0.0),
                "mop_bags": fert_plan.get("mop_bags", 0.0)
            }
            
            irrig_plan = req.get("irrigation_plan", {})
            default_econ = agronomic_data.get_crop_economics(primary_crop)
            if not irrig_plan or "season" not in irrig_plan:
                irrig_plan = {
                    "season": default_econ.get("season", "Kharif"),
                    "duration_days": default_econ.get("duration_days", "110-130"),
                    "water_need": default_econ.get("water_need", "Moderate"),
                    "irrigation_type": default_econ.get("irrigation_type", "Precision Drip"),
                    "water_saving_tip": default_econ.get("water_saving_tip", "Maintain uniform moisture during critical stages.")
                }
            
            econ_plan = req.get("economics", {})
            if not econ_plan or "yield_total" not in econ_plan:
                y_tot = round(default_econ["yield_per_acre_qtl"] * total_acres, 1)
                rev = round(y_tot * default_econ["market_price_per_qtl"], 0)
                cost = round(default_econ["cost_per_acre"] * total_acres, 0)
                econ_plan = {
                    "yield_total": y_tot,
                    "yield_per_acre": default_econ["yield_per_acre_qtl"],
                    "market_price": default_econ["market_price_per_qtl"],
                    "gross_revenue": rev,
                    "total_cost": cost,
                    "net_profit": rev - cost,
                    "roi": round(((rev - cost) / cost) * 100, 1) if cost > 0 else 0
                }

            card_html = report_generator.generate_soil_health_card_html(
                farmer_name=req.get("farmer_name", "Ramesh Kumar"),
                field_id=req.get("field_id", "Plot #4-B"),
                region=req.get("region", "West Bengal"),
                total_acres=total_acres,
                total_hectares=total_hectares,
                primary_crop=primary_crop,
                primary_prob=float(req.get("primary_prob", 95.0)),
                primary_category=req.get("primary_category", "Cereals & Grains"),
                top3_crops=req.get("top3_crops", ["rice", "jute", "cotton"]),
                top3_probs=req.get("top3_probs", [95.0, 5.0, 0.0]),
                soil_inputs=req.get("soil_inputs", {"N": 90, "P": 42, "K": 43, "ph": 6.5, "temp": 26, "humidity": 80, "rain": 200}),
                crop_benchmarks=benchmarks.get(primary_crop, {}),
                fertilizer_plan=fert_plan,
                irrigation_plan=irrig_plan,
                economics=econ_plan
            )
            self._send_html(card_html)
            return

        self._send_json({"error": "Endpoint not found"}, 404)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

def run_server(port=5000):
    os.makedirs(FRONTEND_DIR, exist_ok=True)
    server = ThreadedHTTPServer(("0.0.0.0", port), CropsApiHandler)
    print(f"\n[+] C.R.O.P.S. 3D Web Application running at: http://localhost:{port}\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Server stopped.")
        server.server_close()

if __name__ == "__main__":
    run_server(port=5000)
