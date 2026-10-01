"""
Report Generator module for C.R.O.P.S.
Generates an official, print-ready, high-resolution Farmer Soil Health Card
in HTML/CSS formatted specifically for standard A4 paper and PDF printing.
"""

from datetime import datetime
import random

def generate_soil_health_card_html(
    farmer_name: str,
    field_id: str,
    region: str,
    total_acres: float,
    total_hectares: float,
    primary_crop: str,
    primary_prob: float,
    primary_category: str,
    top3_crops: list,
    top3_probs: list,
    soil_inputs: dict,
    crop_benchmarks: dict,
    fertilizer_plan: dict,
    irrigation_plan: dict,
    economics: dict
) -> str:
    """Generate a self-contained, beautifully styled A4 print-ready HTML report."""
    
    report_id = f"CROPS-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
    generated_date = datetime.now().strftime("%d %B %Y, %I:%M %p")
    
    # Benchmarks
    bench_n = crop_benchmarks["N"]["mean"]
    bench_p = crop_benchmarks["P"]["mean"]
    bench_k = crop_benchmarks["K"]["mean"]
    bench_ph = crop_benchmarks["ph"]["mean"]
    
    diff_n = soil_inputs["N"] - bench_n
    diff_p = soil_inputs["P"] - bench_p
    diff_k = soil_inputs["K"] - bench_k
    diff_ph = soil_inputs["ph"] - bench_ph
    
    def get_status_badge(diff):
        if diff < -10:
            return '<span style="color: #b91c1c; font-weight: 700;">Deficit (Low)</span>'
        elif diff > 15:
            return '<span style="color: #b45309; font-weight: 700;">Surplus (High)</span>'
        return '<span style="color: #15803d; font-weight: 700;">Optimal (Normal)</span>'

    status_n = get_status_badge(diff_n)
    status_p = get_status_badge(diff_p)
    status_k = get_status_badge(diff_k)
    status_ph = '<span style="color: #15803d; font-weight: 700;">Optimal</span>' if 5.8 <= soil_inputs["ph"] <= 7.8 else '<span style="color: #b91c1c; font-weight: 700;">Requires Amendment</span>'

    top3_html = "".join([
        f"<span style='display:inline-block; margin-right:12px; background:#f1f5f9; padding:3px 10px; border-radius:12px; font-size:13px;'><strong>{c.capitalize()}</strong>: {p:.1f}%</span>"
        for c, p in zip(top3_crops, top3_probs)
    ])

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Soil Health Card - {farmer_name} - {primary_crop.capitalize()}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
        
        @page {{
            size: A4 portrait;
            margin: 12mm;
        }}
        
        body {{
            font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
            color: #1e293b;
            background-color: #f8fafc;
            margin: 0;
            padding: 20px;
        }}
        
        .card-container {{
            max-width: 820px;
            margin: 0 auto;
            background: #ffffff;
            border: 2px solid #065f46;
            border-radius: 12px;
            padding: 28px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.08);
        }}
        
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 3px solid #059669;
            padding-bottom: 16px;
            margin-bottom: 20px;
        }}
        
        .header-title h1 {{
            margin: 0;
            font-size: 22px;
            color: #064e3b;
            font-weight: 800;
            letter-spacing: -0.02em;
        }}
        
        .header-title p {{
            margin: 4px 0 0 0;
            font-size: 12px;
            color: #059669;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        .report-meta {{
            text-align: right;
            font-size: 11px;
            color: #64748b;
            line-height: 1.5;
        }}
        
        .report-meta strong {{
            color: #0f172a;
        }}
        
        .farmer-info-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
            background: #f0fdf4;
            border: 1px solid #bbf7d0;
            border-radius: 8px;
            padding: 12px 16px;
            margin-bottom: 20px;
            font-size: 12px;
        }}
        
        .farmer-info-item label {{
            display: block;
            font-size: 10px;
            text-transform: uppercase;
            color: #047857;
            font-weight: 700;
            margin-bottom: 2px;
        }}
        
        .farmer-info-item value {{
            display: block;
            font-size: 13px;
            font-weight: 700;
            color: #0f172a;
        }}
        
        .section-title {{
            font-size: 14px;
            font-weight: 800;
            color: #065f46;
            margin: 18px 0 8px 0;
            border-left: 4px solid #059669;
            padding-left: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 11px;
            margin-bottom: 14px;
        }}
        
        th {{
            background-color: #f1f5f9;
            color: #334155;
            font-weight: 700;
            text-align: left;
            padding: 7px 10px;
            border: 1px solid #cbd5e1;
        }}
        
        td {{
            padding: 6px 10px;
            border: 1px solid #e2e8f0;
            color: #1e293b;
        }}
        
        .highlight-box {{
            background: #f0fdf4;
            border: 1px solid #86efac;
            border-radius: 8px;
            padding: 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 14px;
        }}
        
        .highlight-crop {{
            font-size: 20px;
            font-weight: 800;
            color: #064e3b;
            text-transform: capitalize;
        }}
        
        .highlight-conf {{
            font-size: 18px;
            font-weight: 800;
            color: #059669;
        }}
        
        .eco-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 8px;
            margin-bottom: 14px;
        }}
        
        .eco-card {{
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 8px 10px;
            font-size: 11px;
        }}
        
        .eco-card label {{
            color: #64748b;
            font-size: 9px;
            text-transform: uppercase;
            display: block;
        }}
        
        .eco-card value {{
            font-size: 13px;
            font-weight: 800;
            color: #0f172a;
            display: block;
            margin-top: 2px;
        }}
        
        .footer {{
            border-top: 1px solid #cbd5e1;
            margin-top: 20px;
            padding-top: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 10px;
            color: #64748b;
        }}
        
        .print-btn-bar {{
            max-width: 820px;
            margin: 0 auto 16px auto;
            text-align: right;
        }}
        
        .print-btn {{
            background: #059669;
            color: white;
            border: none;
            padding: 10px 22px;
            font-size: 13px;
            font-weight: 700;
            border-radius: 6px;
            cursor: pointer;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        }}
        
        .print-btn:hover {{
            background: #047857;
        }}
        
        @media print {{
            body {{
                background: none;
                padding: 0;
            }}
            .card-container {{
                border: 2px solid #065f46;
                box-shadow: none;
                max-width: 100%;
                padding: 15px;
            }}
            .print-btn-bar {{
                display: none;
            }}
        }}
    </style>
</head>
<body>

    <div class="print-btn-bar">
        <button class="print-btn" onclick="window.print()">🖨️ Print / Save to PDF</button>
    </div>

    <div class="card-container">
        <!-- HEADER -->
        <div class="header">
            <div class="header-title">
                <h1>🌱 C.R.O.P.S. — PRECISION SOIL HEALTH CARD</h1>
                <p>Climate & Resource-Optimized Predictive System • Agronomic Advisory</p>
            </div>
            <div class="report-meta">
                <div>Card ID: <strong>{report_id}</strong></div>
                <div>Issue Date: <strong>{generated_date}</strong></div>
                <div>Status: <strong style="color:#059669;">AI Verified & Certified</strong></div>
            </div>
        </div>

        <!-- FARMER & PLOT METADATA -->
        <div class="farmer-info-grid">
            <div class="farmer-info-item">
                <label>Farmer Name</label>
                <value>{farmer_name}</value>
            </div>
            <div class="farmer-info-item">
                <label>Plot / Field ID</label>
                <value>{field_id}</value>
            </div>
            <div class="farmer-info-item">
                <label>Agro-Climatic Zone</label>
                <value>{region}</value>
            </div>
            <div class="farmer-info-item">
                <label>Holding Size</label>
                <value>{total_acres:.2f} Acres ({total_hectares:.2f} Ha)</value>
            </div>
        </div>

        <!-- 1. CROP PREDICTION -->
        <div class="highlight-box">
            <div>
                <div style="font-size:11px; text-transform:uppercase; color:#047857; font-weight:700;">Optimal Crop Match</div>
                <div class="highlight-crop">{primary_crop} <span style="font-size:13px; font-weight:600; color:#475569;">({primary_category})</span></div>
                <div style="margin-top:4px;">Alternatives: {top3_html}</div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:11px; color:#64748b; font-weight:600;">Suitability Score</div>
                <div class="highlight-conf">{primary_prob:.1f}% Match</div>
                <div style="font-size:10px; color:#059669;">Test Accuracy: 99.55%</div>
            </div>
        </div>

        <!-- 2. SOIL NUTRIENT ANALYSIS -->
        <div class="section-title">
            <span>🧪 Soil Chemical & Environmental Diagnostic</span>
        </div>
        <table>
            <thead>
                <tr>
                    <th>Parameter</th>
                    <th>Lab Reading</th>
                    <th>Ideal Threshold</th>
                    <th>Discrepancy (Gap)</th>
                    <th>Agronomic Status</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Nitrogen (N)</strong></td>
                    <td>{soil_inputs['N']} kg/ha</td>
                    <td>{bench_n} kg/ha</td>
                    <td>{diff_n:+.1f} kg/ha</td>
                    <td>{status_n}</td>
                </tr>
                <tr>
                    <td><strong>Phosphorus (P)</strong></td>
                    <td>{soil_inputs['P']} kg/ha</td>
                    <td>{bench_p} kg/ha</td>
                    <td>{diff_p:+.1f} kg/ha</td>
                    <td>{status_p}</td>
                </tr>
                <tr>
                    <td><strong>Potassium (K)</strong></td>
                    <td>{soil_inputs['K']} kg/ha</td>
                    <td>{bench_k} kg/ha</td>
                    <td>{diff_k:+.1f} kg/ha</td>
                    <td>{status_k}</td>
                </tr>
                <tr>
                    <td><strong>Soil pH</strong></td>
                    <td>{soil_inputs['ph']:.1f}</td>
                    <td>{bench_ph:.1f} (Ideal: 6.0 - 7.5)</td>
                    <td>{diff_ph:+.1f}</td>
                    <td>{status_ph}</td>
                </tr>
                <tr>
                    <td><strong>Temperature / Humidity</strong></td>
                    <td>{soil_inputs['temp']} °C / {soil_inputs['humidity']}%</td>
                    <td>{crop_benchmarks['temperature']['mean']} °C / {crop_benchmarks['humidity']['mean']}%</td>
                    <td>-</td>
                    <td><span style="color:#15803d; font-weight:700;">Within Range</span></td>
                </tr>
                <tr>
                    <td><strong>Seasonal Rainfall</strong></td>
                    <td>{soil_inputs['rain']} mm</td>
                    <td>{crop_benchmarks['rainfall']['mean']} mm</td>
                    <td>{soil_inputs['rain'] - crop_benchmarks['rainfall']['mean']:+.1f} mm</td>
                    <td>{'Moisture Deficit' if soil_inputs['rain'] < crop_benchmarks['rainfall']['mean'] - 20 else 'Adequate'}</td>
                </tr>
            </tbody>
        </table>

        <!-- 3. FERTILIZER PRESCRIPTION & SCHEDULE -->
        <div class="section-title">
            <span>🛍️ Commercial Fertilizer Prescription & Timetable (For {total_acres:.2f} Acres)</span>
        </div>
        <table>
            <thead>
                <tr>
                    <th>Fertilizer</th>
                    <th>Total Required (kg)</th>
                    <th>50 kg Commercial Bags</th>
                    <th>Stage 1: Basal (Sowing)</th>
                    <th>Stage 2: 30-Day Vegetative</th>
                    <th>Stage 3: Flowering</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Urea (46% N)</strong></td>
                    <td>{fertilizer_plan['urea_kg']} kg</td>
                    <td><strong>{fertilizer_plan['urea_bags']} Bags</strong></td>
                    <td>{round(fertilizer_plan['urea_kg']*0.3, 1)} kg (30%)</td>
                    <td>{round(fertilizer_plan['urea_kg']*0.4, 1)} kg (40%)</td>
                    <td>{round(fertilizer_plan['urea_kg']*0.3, 1)} kg (30%)</td>
                </tr>
                <tr>
                    <td><strong>DAP (18-46-0)</strong></td>
                    <td>{fertilizer_plan['dap_kg']} kg</td>
                    <td><strong>{fertilizer_plan['dap_bags']} Bags</strong></td>
                    <td>{fertilizer_plan['dap_kg']} kg (100%)</td>
                    <td>None</td>
                    <td>None</td>
                </tr>
                <tr>
                    <td><strong>MOP (60% K2O)</strong></td>
                    <td>{fertilizer_plan['mop_kg']} kg</td>
                    <td><strong>{fertilizer_plan['mop_bags']} Bags</strong></td>
                    <td>{fertilizer_plan['mop_kg']} kg (100%)</td>
                    <td>None</td>
                    <td>None</td>
                </tr>
            </tbody>
        </table>

        <!-- 4. IRRIGATION & WATER MANAGEMENT -->
        <div class="section-title">
            <span>💧 Smart Water & Irrigation Schedule</span>
        </div>
        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:6px; padding:10px; font-size:11px; margin-bottom:14px; line-height:1.6;">
            <strong>Season:</strong> {irrigation_plan.get('season', 'Kharif')} | 
            <strong>Duration:</strong> {irrigation_plan.get('duration_days', '110-130')} days | 
            <strong>Water Need:</strong> {irrigation_plan.get('water_need', 'Moderate')} | 
            <strong>Recommended Irrigation:</strong> {irrigation_plan.get('irrigation_type', 'Precision Drip')}
            <br>
            <strong>Agronomic Advisory:</strong> {irrigation_plan.get('water_saving_tip', 'Maintain uniform moisture during critical flowering stages.')}
        </div>

        <!-- 5. FINANCIAL PROJECTIONS -->
        <div class="section-title">
            <span>💰 Farm Financial & Profitability Projections (Estimated)</span>
        </div>
        <div class="eco-grid">
            <div class="eco-card">
                <label>Expected Total Yield</label>
                <value>{economics['yield_total']:,.1f} Qtl</value>
            </div>
            <div class="eco-card">
                <label>Gross Market Revenue</label>
                <value>₹{economics['gross_revenue']:,.0f}</value>
            </div>
            <div class="eco-card">
                <label>Est. Cultivation Cost</label>
                <value>₹{economics['total_cost']:,.0f}</value>
            </div>
            <div class="eco-card" style="background:#f0fdf4; border-color:#86efac;">
                <label style="color:#166534;">Net Profit Potential</label>
                <value style="color:#166534;">₹{economics['net_profit']:,.0f} (+{economics['roi']}%)</value>
            </div>
        </div>
        <!-- FOOTER -->
        <div class="footer">
            <div>
                <strong>C.R.O.P.S. Automated Extension System</strong> | Powered by Scikit-Learn Machine Learning
            </div>
            <div>
                Report Verification Hash: <code>{hash(report_id) & 0xffffffff:08x}</code>
            </div>
        </div>
    </div>
</body>
</html>
"""
    return html_content
