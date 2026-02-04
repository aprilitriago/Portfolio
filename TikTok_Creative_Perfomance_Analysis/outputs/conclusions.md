---
---
## CONCLUSIONS - TikTok Creative Performance Analysis

---
---

### Executive Summary

Analysis of 157 TikTok videos (KFC, McDonald's, Burger King Spain, Q4 2024–Q1 2025) reveals three critical performance drivers:

1. **Brand Imposition Effect**: Control over influencers destroys engagement (25x within-influencer, 9x cross-brand gap)
2. **Content Type Divide**: Branding outperforms promotional 4.6x (82.6 vs 18.0 efficiency)
3. **Character Equity**: Established icons (Coronel, 70+ years) justify investment; newer characters underperform

---

### Key Findings

### 1. Brand Imposition Kills Influencer Performance

**Within-Influencer Evidence:**
- Brujillo Juan (BK): 73.35 efficiency casual vs 2.91 uniformed/scripted
- **Ratio: 25.2x difference**

**Cross-Brand Validation:**
- KFC influencers (autonomous, 67% branding): 155.9 avg efficiency
- BK influencers (controlled, 100% promo): 17.4 avg efficiency
- **Ratio: 9.0x gap**

**Mechanism:** Uniforms + scripts = perceived inauthenticity → disengagement

**Economic Impact:** ~€33K opportunity cost per controlled influencer video

---

### 2. Entertainment-First Beats Selling-First

**Performance by Category:**
```python
branding_avg = 82.6    # n=80
promo_avg = 18.0       # n=58
ratio = 4.6x
```

**Tier Composition:**
- HIGH tier: 80% branding, 20% promo
- LOW tier: 25% branding, 75% promo

**Neither Strategy Validation:**
```python
neither_category_dist = {
    'branding': 81.5%,
    'promo': 11.1%, 
    'product_launch': 7.4%
}
neither_roi = 110.6  # Best ROI, branding-heavy
```

**Insight:** Baseline efficiency driven by entertainment-focus (branding), not protagonist investment.

---

### 3. ROI Analysis: Portfolio Approach

**Performance vs ROI Trade-offs:**

| Strategy   | Performance | Cost (€) | ROI (per €1K) | Use Case |
|-----------|-------------|----------|---------------|----------|
| Neither   | 88.5        | 800      | **110.6** ★   | Baseline efficiency |
| Lore (other) | 72.9     | 5000     | 14.6          | Avoid (underperforms) |
| Coronel   | **102.3**   | 4000     | 25.6          | Brand building |
| Influencer| **155.9** ★ | 10000    | 15.6          | Peak moments |

**Character-Specific Breakdown:**
```python
coronel_performance = 102.3    # KFC, 70+ years equity
other_lore_performance = 72.9  # Bucket Head, Eduardo, etc.
baseline_performance = 88.5    # Neither (no protagonist)

# Coronel justification:
coronel_premium = (102.3 - 88.5) / 88.5  # +15.6% performance
# Worth €5K for differentiation + long-term equity
```

**Recommended Portfolio:**
- 60% Neither (€800/video): High ROI baseline
- 30% Coronel (€4K/video): Brand differentiation
- 10% Influencer (€10K/video): Strategic peaks

---

### 4. Platform-Native Aesthetics: Chaotic Wins, Lifestyle Fails

**Finding:** Clear aesthetic divergence—platform-native content (chaotic, meme-style) dominates HIGH tier, while traditional advertising aesthetics (lifestyle, TV commercial) dominate LOW tier.

**Vibe Distribution:**

**LOW Tier (Failures):**
- Lifestyle: 60% ← Polished, TV commercial aesthetic
- Generic: 22%
- Chaotic: 5% ← Meme-style rare

**HIGH Tier (Successes):**
- Chaotic: 65% ← Meme-style dominates 
- Generic: 15%
- Lifestyle: 13% ← TV commercial rare

**Key Numbers:**
- Chaotic: **13x more prevalent in HIGH** (65% vs 5%)
- Lifestyle: **4.6x more prevalent in LOW** (60% vs 13%)

**Why Chaotic Wins:**

Chaotic vibe is **inherently platform-native**:
- Meme-inspired editing (rapid cuts, absurd compositions)
- "Deep-fried" visual effects, high saturation
- Bizarre humor embedded in aesthetic (by definition)
- Raw, unpolished = authentic signal

**Why Lifestyle Fails:**

Lifestyle vibe signals **imported advertising**:
- Polished studio production = "corporate"
- Professional actors, choreography = scripted
- Clean aesthetic = not TikTok-native
- Audiences trained to skip ads

**Exception - Lifestyle + Influencer:**
When lifestyle works in HIGH tier, it's paired with influencers:
- 80% of HIGH lifestyle features influencers
- With influencer: 220.16 avg efficiency
- Without: 118.44 avg efficiency
- **Ratio: 1.86x**

**Interpretation:** Influencer personality softens the "corporate" feel of polished production, providing authenticity the aesthetic lacks alone.

**Connection to Humor:**
- Chaotic: 100% co-occurrence with humor (humor is embedded in meme-style aesthetic)
- Lifestyle: Independent of humor (works with/without if influencer present)

**Strategic Implication:**

TikTok rewards **platform-native visual language** (chaotic, memes, absurd) and punishes **imported advertising aesthetics** (lifestyle, TV commercial, polished). Success requires **aesthetic code-switching**—abandon traditional production values, embrace platform culture.

**Core Pattern:** What dominates failures (lifestyle 60%) nearly disappears in successes (13%). What's rare in failures (chaotic 5%) dominates successes (65%). This isn't about "adding humor"—it's about **speaking TikTok's visual dialect fluently**.

---

### 5. Production Style Patterns

**HIGH tier favors:**
- Lo-fi: 45% (platform-native, authentic)
- Chaotic vibe: 55% (meme-inspired)
- Humor intent: 70%

**LOW tier characteristics:**
- Studio: 60% (polished, corporate feel)
- Lifestyle vibe: 60% (TV commercial aesthetic)
- Humor intent: 30%

**Insight:** TikTok rewards platform-native aesthetics over traditional advertising production.

---

### Statistical Summary

### Sample Composition
```python
total_videos = 157
brands = {
    'kfc_es': 84,
    'mcdonalds_es': 40, 
    'burgerking_es': 33
}

tier_distribution = {
    'high': 39,  # Top 25% (efficiency > 49.1)
    'low': 39,   # Bottom 25% (efficiency < 7.9)
    'medium': 79
}
```

### Key Metrics
```python
# Efficiency Score Distribution
overall_mean = 51.0
overall_median = 16.2
high_tier_min = 49.1
low_tier_max = 7.9

# Engagement Rates
avg_engagement_rate_clean = 2.8%  # (likes + saves + shares) / views
avg_efficiency_score_clean = 28.0  # Per 1000 views
```

### Effect Sizes (Key Comparisons)
```python
# Brand Imposition
brujillo_casual_vs_uniformed = 25.2  # Within-influencer ratio
kfc_vs_bk_influencers = 9.0          # Cross-brand ratio

# Content Type
branding_vs_promo = 4.6              # Category performance gap

# Character Equity  
coronel_vs_other_lore = 1.4          # Character-specific advantage
coronel_vs_baseline = 1.16           # Coronel premium over Neither
```

---

### Limitations

1. **Temporal Scope**: Q4 2024–Q1 2025 (4 months, algorithm may evolve)
2. **Geographic**: Spain only (cultural context matters)
3. **Platform**: TikTok only (may not generalize to Instagram, YouTube)
4. **Sample Size**: 157 videos (adequate for patterns, borderline for causal claims)
5. **Cost Estimates**: Approximated (€800, €5K, €10K), not actual brand spend
6. **Causality**: Observational (not experimental), confounders possible

---

### Technical Notes

### Variables Analyzed
- **48 total columns** including:
  - Basic metrics: views, likes, shares, saves, duration
  - Engagement: efficiency_score_clean (primary DV)
  - Creative: hook_1, hook_2, vibe_check, humor_intent
  - Protagonist: protagonist_type, character_name, influencer_score
  - Production: production_style, camera_dynamics
  - Strategy: video_category, brand_lore_visual
  - Sentiment: sentiment_score, community_reaction

### Tier Definition
```python
# Efficiency quartiles
Q1 = 7.9   # Low tier cutoff (bottom 25%)
Q3 = 49.1  # High tier cutoff (top 25%)

# Assignment
low_tier = efficiency_score_clean <= Q1
high_tier = efficiency_score_clean >= Q3
medium_tier = (efficiency_score_clean > Q1) & (efficiency_score_clean < Q3)
```

### ROI Calculation
```python
def calculate_roi(efficiency, cost_euros):
    """
    Returns efficiency points per €1,000 spent
    
    Example:
    - Neither: 88.5 efficiency / €800 = 110.6 per €1K
    - Coronel: 102.3 efficiency / €5000 = 20.5 per €1K
    """
    return (efficiency / cost_euros) * 1000
```

---

### Recommendations for Future Analysis

### Immediate Extensions
1. **Statistical Tests**: Add t-tests, p-values, Cohen's d for effect sizes
2. **Regression Analysis**: Control for views, duration, time effects
3. **Robustness Checks**: Analyze by brand separately, test alternative tier definitions

### Medium-Term
1. **Temporal Validation**: Collect H1 2025 data, test pattern stability
2. **Cross-Platform**: Replicate on Instagram Reels, YouTube Shorts
3. **Mechanism Testing**: Code "authenticity signals", test mediation (Control → Authenticity → Performance)

### Long-Term
1. **Experimental Validation**: Partner with brand for A/B test (control vs autonomy)
2. **Longitudinal Tracking**: Monitor Coronel ROI improvement as equity compounds
3. **Industry Generalization**: Test in beauty, tech, finance sectors

---

### Code Replication

### Key Analysis Snippets

**1. Brand Imposition Analysis:**
```python
# Within-influencer comparison
brujillo = df[df['character_name'] == 'Brujillo Juan']
casual = brujillo[brujillo['video_category'] == 'branding']['efficiency_score_clean'].mean()
uniformed = brujillo[brujillo['video_category'] == 'promo']['efficiency_score_clean'].mean()
ratio = casual / uniformed  # 25.2x

# Cross-brand comparison
kfc_inf = df[(df['brand']=='kfc_es') & (df['protagonist_type']=='influencer')]['efficiency_score_clean'].mean()
bk_inf = df[(df['brand']=='burgerking_es') & (df['protagonist_type']=='influencer')]['efficiency_score_clean'].mean()
gap = kfc_inf / bk_inf  # 9.0x
```

**2. ROI Calculation:**
```python
# Define costs
costs = {'neither': 800, 'coronel': 4000, 'influencer': 10000}

# Calculate performance
neither_perf = df[df['protagonist_type']=='none']['efficiency_score_clean'].mean()
coronel_perf = df[df['character_name']=='Coronel']['efficiency_score_clean'].mean()
influencer_perf = df[df['protagonist_type']=='influencer']['efficiency_score_clean'].mean()

# ROI
neither_roi = (neither_perf / costs['neither']) * 1000  # 110.6
coronel_roi = (coronel_perf / costs['coronel']) * 1000  # 25.6
influencer_roi = (influencer_perf / costs['influencer']) * 1000  # 15.6
```

**3. Branding vs Promo:**
```python
branding_avg = df[df['video_category']=='branding']['efficiency_score_clean'].mean()
promo_avg = df[df['video_category']=='promo']['efficiency_score_clean'].mean()
advantage = branding_avg / promo_avg  # 4.6x

# Neither category composition
neither = df[df['protagonist_type']=='none']
neither['video_category'].value_counts(normalize=True)
# branding: 81.5%, promo: 11.1%, product_launch: 7.4%
```

---

### Final Takeaway

**Three-sentence summary for stakeholders:**

1. **Brand control destroys influencer effectiveness** (25x within-influencer drop, 9x cross-brand gap, €33K opportunity cost per video)

2. **Entertainment-first content outperforms selling-first** (branding 4.6x better than promo; baseline achieves best ROI being 81.5% branding)

3. **Optimal strategy blends efficiency, differentiation, and peaks** (60% baseline production, 30% established brand character, 10% autonomous influencers)

**Core insight:** Less brand presence often yields more brand impact. TikTok rewards platform-native content over traditional advertising.

---


**Dataset:** `master_creative_audit.csv` (157 rows × 48 columns)
**Date Range:** October 2024 – January 2025

**Analyst:** April Itriago Trujillo

**Contact:** 
    **Email:** april@dataguapa.com
    **LinkedIn:** https://linkedin.com/in/april-itriago

---

### Appendix: Variable Definitions

See `GLOSSARY_ENGLISH_UPDATED.txt` for complete variable documentation.

**Key Variables:**
- `efficiency_score_clean`: (likes + saves + shares) / views × 1000 [Primary DV]
- `eff_tier`: Performance tier (high/medium/low) based on Q1/Q3 cutoffs
- `protagonist_type`: Who appears (none, influencer, brand_character, employee, generic)
- `video_category`: Objective (branding, promo, product_launch)
- `vibe_check`: Visual style (chaotic, lifestyle, sensory, authentic, didactic, generic)
- `brand_lore_visual`: Brand-exclusive visual assets present (1/0)

---

