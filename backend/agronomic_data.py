"""
Agronomic and Economic Knowledge Base for C.R.O.P.S.
Contains validated agro-ecological parameters, cropping seasons, irrigation guidelines,
and economic benchmarks (yield, MSP/market prices, cultivation costs) for 22 crops.
"""

# Economic and Market Parameters (per Acre basis)
# Based on ICAR (Indian Council of Agricultural Research) & Ministry of Agriculture CACP benchmarks
CROP_ECONOMICS = {
    "rice": {
        "yield_per_acre_qtl": 22.0,      # Quintals (1 Qtl = 100 kg)
        "market_price_per_qtl": 2300,    # MSP / Mandi average (INR)
        "cost_per_acre": 18500,          # Seed, fertilizer, land prep, labor
        "season": "Kharif (Monsoon)",
        "duration_days": "115 - 135",
        "water_need": "High",
        "irrigation_type": "Alternate Wetting & Drying (AWD) / Controlled Flooding",
        "water_saving_tip": "Adopt AWD technique to save 25-30% water and reduce methane emissions."
    },
    "maize": {
        "yield_per_acre_qtl": 25.0,
        "market_price_per_qtl": 2090,
        "cost_per_acre": 16000,
        "season": "Kharif / Rabi",
        "duration_days": "95 - 110",
        "water_need": "Moderate",
        "irrigation_type": "Furrow / Overhead Sprinkler",
        "water_saving_tip": "Avoid waterlogging during knee-high and tasseling stages."
    },
    "chickpea": {
        "yield_per_acre_qtl": 9.5,
        "market_price_per_qtl": 5440,
        "cost_per_acre": 12500,
        "season": "Rabi (Winter)",
        "duration_days": "100 - 115",
        "water_need": "Low",
        "irrigation_type": "Micro-Sprinkler / Raingun",
        "water_saving_tip": "Highly responsive to 2 life-saving irrigations at branching and pod development."
    },
    "kidneybeans": {
        "yield_per_acre_qtl": 8.0,
        "market_price_per_qtl": 7500,
        "cost_per_acre": 15000,
        "season": "Rabi / Kharif (Hills)",
        "duration_days": "100 - 120",
        "water_need": "Moderate",
        "irrigation_type": "Drip / Sprinkler",
        "water_saving_tip": "Sensitive to moisture stress at flowering and pod filling."
    },
    "pigeonpeas": {
        "yield_per_acre_qtl": 8.5,
        "market_price_per_qtl": 7000,
        "cost_per_acre": 14000,
        "season": "Kharif (Monsoon)",
        "duration_days": "150 - 180",
        "water_need": "Moderate to Low",
        "irrigation_type": "Drip Irrigation / Rainfed",
        "water_saving_tip": "Deep taproot system tolerates dry spells; 1 irrigation at pod-fill boosts yield by 35%."
    },
    "mothbeans": {
        "yield_per_acre_qtl": 5.0,
        "market_price_per_qtl": 6500,
        "cost_per_acre": 8500,
        "season": "Kharif (Arid)",
        "duration_days": "75 - 90",
        "water_need": "Very Low (Drought Hardy)",
        "irrigation_type": "Rainfed / Protective Drip",
        "water_saving_tip": "Extremely drought-hardy legume suitable for low-rainfall sandy soil zones."
    },
    "mungbean": {
        "yield_per_acre_qtl": 6.5,
        "market_price_per_qtl": 8558,
        "cost_per_acre": 10500,
        "season": "Zaid (Summer) / Kharif",
        "duration_days": "65 - 75",
        "water_need": "Low",
        "irrigation_type": "Sprinkler Irrigation",
        "water_saving_tip": "Short duration catch crop requiring only 3-4 light irrigations."
    },
    "blackgram": {
        "yield_per_acre_qtl": 6.0,
        "market_price_per_qtl": 6950,
        "cost_per_acre": 11000,
        "season": "Kharif / Rabi",
        "duration_days": "75 - 90",
        "water_need": "Low to Moderate",
        "irrigation_type": "Sprinkler / Ridge & Furrow",
        "water_saving_tip": "Ensure adequate drainage; stagnant water causes root rot."
    },
    "lentil": {
        "yield_per_acre_qtl": 7.0,
        "market_price_per_qtl": 6425,
        "cost_per_acre": 11500,
        "season": "Rabi (Winter)",
        "duration_days": "110 - 130",
        "water_need": "Low",
        "irrigation_type": "Sprinkler / Border Strip",
        "water_saving_tip": "Requires minimal water; avoid excess irrigation post flowering."
    },
    "pomegranate": {
        "yield_per_acre_qtl": 55.0,
        "market_price_per_qtl": 6000,
        "cost_per_acre": 65000,
        "season": "Perennial (Bahar treatment)",
        "duration_days": "Perennial (Harvest in 150-180 days after flowering)",
        "water_need": "Moderate",
        "irrigation_type": "Precision Drip with Inline Emitters",
        "water_saving_tip": "Use water stress during rest period followed by regulated drip irrigation."
    },
    "banana": {
        "yield_per_acre_qtl": 190.0,
        "market_price_per_qtl": 1600,
        "cost_per_acre": 85000,
        "season": "Year-round Planting",
        "duration_days": "330 - 365",
        "water_need": "High",
        "irrigation_type": "Drip Irrigation with Fertigation",
        "water_saving_tip": "Drip fertigation saves 40% water and increases bunch weight by 20%."
    },
    "mango": {
        "yield_per_acre_qtl": 45.0,
        "market_price_per_qtl": 4500,
        "cost_per_acre": 40000,
        "season": "Perennial (Harvest March-July)",
        "duration_days": "Perennial",
        "water_need": "Moderate",
        "irrigation_type": "Drip / Double Basin",
        "water_saving_tip": "Withhold water 2-3 months prior to flowering to stimulate flower bud differentiation."
    },
    "grapes": {
        "yield_per_acre_qtl": 90.0,
        "market_price_per_qtl": 4200,
        "cost_per_acre": 95000,
        "season": "Perennial (Pruning cycles)",
        "duration_days": "Perennial",
        "water_need": "Moderate",
        "irrigation_type": "Sub-surface Drip / Micro-Drip",
        "water_saving_tip": "Regulated deficit irrigation (RDI) improves sugar content (Brix) and berry quality."
    },
    "watermelon": {
        "yield_per_acre_qtl": 140.0,
        "market_price_per_qtl": 1000,
        "cost_per_acre": 35000,
        "season": "Zaid (Summer)",
        "duration_days": "80 - 95",
        "water_need": "Moderate",
        "irrigation_type": "Drip under Silver-Black Mulch",
        "water_saving_tip": "Mulching reduces water evaporation by 50% and prevents fruit soil rot."
    },
    "muskmelon": {
        "yield_per_acre_qtl": 85.0,
        "market_price_per_qtl": 1800,
        "cost_per_acre": 32000,
        "season": "Zaid (Summer)",
        "duration_days": "75 - 90",
        "water_need": "Moderate",
        "irrigation_type": "Drip under Plastic Mulch",
        "water_saving_tip": "Reduce irrigation 10-14 days before harvest to maximize sugar accumulation."
    },
    "apple": {
        "yield_per_acre_qtl": 60.0,
        "market_price_per_qtl": 7000,
        "cost_per_acre": 90000,
        "season": "Temperate Perennial",
        "duration_days": "Perennial (Harvest July-Oct)",
        "water_need": "Moderate",
        "irrigation_type": "Micro-Sprinklers / Drip",
        "water_saving_tip": "Micro-sprinklers also provide frost protection during early bud break."
    },
    "orange": {
        "yield_per_acre_qtl": 65.0,
        "market_price_per_qtl": 3500,
        "cost_per_acre": 45000,
        "season": "Perennial (Citrus)",
        "duration_days": "Perennial (Harvest Nov-Feb)",
        "water_need": "Moderate",
        "irrigation_type": "Drip System with 2-4 emitters/tree",
        "water_saving_tip": "Maintain uniform moisture during fruit set to prevent fruit drop."
    },
    "papaya": {
        "yield_per_acre_qtl": 240.0,
        "market_price_per_qtl": 1200,
        "cost_per_acre": 60000,
        "season": "Year-round",
        "duration_days": "270 - 300",
        "water_need": "Moderate to High",
        "irrigation_type": "Drip Irrigation / Ring Basin",
        "water_saving_tip": "Avoid wetting the tree trunk directly to prevent collar rot (Phytophthora)."
    },
    "coconut": {
        "yield_per_acre_qtl": 45.0,     # ~4,500 mature nuts translated into qtl equivalent
        "market_price_per_qtl": 3800,
        "cost_per_acre": 30000,
        "season": "Perennial Plantation",
        "duration_days": "Perennial (Continuous fruiting)",
        "water_need": "High",
        "irrigation_type": "Drip (40-50 L/palm/day) or Basin",
        "water_saving_tip": "Apply organic mulch around palm basins to conserve root zone moisture."
    },
    "cotton": {
        "yield_per_acre_qtl": 11.0,
        "market_price_per_qtl": 7020,
        "cost_per_acre": 24000,
        "season": "Kharif (Monsoon)",
        "duration_days": "150 - 170",
        "water_need": "Moderate",
        "irrigation_type": "Drip or Alternate Furrow",
        "water_saving_tip": "Alternate furrow irrigation saves 40% water with zero yield loss in black soils."
    },
    "jute": {
        "yield_per_acre_qtl": 14.5,
        "market_price_per_qtl": 5050,
        "cost_per_acre": 18000,
        "season": "Kharif (Pre-monsoon)",
        "duration_days": "110 - 120",
        "water_need": "High",
        "irrigation_type": "Controlled Furrow / Rainfed",
        "water_saving_tip": "Requires high humidity and ample retting water post harvest."
    },
    "coffee": {
        "yield_per_acre_qtl": 6.5,
        "market_price_per_qtl": 18500,
        "cost_per_acre": 38000,
        "season": "Highland Plantation",
        "duration_days": "Perennial (Harvest Nov-Feb)",
        "water_need": "Moderate to High",
        "irrigation_type": "Overhead Sprinkler (Blossom Showers)",
        "water_saving_tip": "Precision sprinkler 'blossom showers' trigger uniform synchronized flowering."
    }
}

def get_crop_economics(crop_name: str) -> dict:
    """Retrieve economic benchmarks for a given crop."""
    return CROP_ECONOMICS.get(crop_name.lower(), {
        "yield_per_acre_qtl": 15.0,
        "market_price_per_qtl": 3000,
        "cost_per_acre": 20000,
        "season": "Seasonal",
        "duration_days": "100 - 120",
        "water_need": "Moderate",
        "irrigation_type": "Drip or Furrow",
        "water_saving_tip": "Maintain regular soil moisture during critical vegetative stages."
    })
