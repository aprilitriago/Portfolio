📊 COLUMN GLOSSARY - ENGLISH VERSION (UPDATED)

📈 BASIC METRICS
id - Unique TikTok video identifier
date - Publication date (format: YYYYMMDD)
brand - Brand name (burgerking_es, mcdonalds_es, kfc_es)
url - Complete TikTok video URL
views - Total number of views
likes - Number of likes
comments - Number of comments
saves - Times saved
shares - Times shared
duration - Duration in seconds

📊 ENGAGEMENT METRICS
engagement_rate_total - (likes + comments + saves + shares) / views × 100
engagement_rate_clean - (likes + saves + shares) / views × 100
efficiency_score_clean - (likes + saves + shares) / views × 1000
likes_rate - (likes / views) × 100
shares_rate - (shares / views) × 100
saves_rate - (saves / views) × 100

🎣 HOOK ANALYSIS
hook_1 - Dominant signal in first 1.5s:
  - text_direct: standalone persuasive text (promotion, question, intriguing phrase)
  - text_contextual: text that only labels/describes (product name, subtitle)
  - action: dominant physical action (biting, pouring, hands doing something)
  - visual: visual impact without text (extreme close-up, unexpected object)
  - unknown: no clear signal

hook_2 - Hook rhythm:
  - punch: immediate impact, everything visible from frame 1
  - build: builds tension, doesn't resolve in the hook
  - reveal: setup + payoff within the hook (resolution in 1.5s)
  - flat: no clear rhythm, neutral, plain
  - unknown: not determinable

hook_evidence - Visual justification for hook classification
hook_confidence - Classification confidence (0.0-1.0)

📝 TEXT DENSITY
text_density - Amount of text: high, medium, low, unknown
text_evidence - Description of observed text

🎨 VISUAL STYLE (VIBE)
vibe_check - Dominant visual style:
  - sensory: food porn, macro, extreme close-ups, textures
  - chaotic: meme, frenetic editing, absurd, bizarre humor
  - authentic: real UGC, handheld mobile, imperfect, real environments
  - didactic: app, steps, tutorial, data
  - lifestyle: TV commercial, actors, studio, clean choreography
  - generic: only if doesn't fit any other

vibe_evidence - 2-3 concrete visual signals
vibe_confidence - Confidence (0.0-1.0)

😂 HUMOR
humor_intent - Humor intention:
  - yes: video attempts to be funny (jokes, absurd, memes, punchlines)
  - no: informative, direct promotional, emotional, serious
  - unknown: not determinable

👥 CHARACTERS
gender - Visible gender: male, female, both, none, unknown
humanity_level - Human presence level: face, hands, body, none, unknown

protagonist_type - Protagonist type:
  - brand_character: fictional brand character (Colonel, BK King, Ronald, Eduardo)
  - influencer: real person who could work for any brand
  - employee: brand employee
  - generic: unidentified generic person
  - none: no human protagonist
  - unknown: not determinable

character_name - Character or influencer name (e.g., "Coronel", "Brujillo Juan", "Don Pollo", "none")
influencer_score - Influencer likelihood (0.0-1.0)
baby_presence - Baby presence: 1 (yes), 0 (no)
animal_presence - Animal presence: 1 (yes), 0 (no)

🎬 PRODUCTION
production_style - Production style:
  - ugc: REAL user content, not the brand
  - false_ugc: brand imitates casual style but with GOOD technical quality
  - studio: professional POLISHED production (includes quality animation)
  - lo-fi: brand production with POOR technical quality (includes crude animation)
  - unknown: not determinable

camera_dynamics - Camera movement:
  - static: fixed camera
  - zoom_transition: close-up to wide or vice versa
  - handheld: mobile phone, organic movement
  - fast_cuts: rapid cuts <2s
  - unknown: not determinable

🎨 COLORS
brand_colors - JSON list 0-3 HEX colors from product/packaging/logo
bg_colors - JSON list 0-3 HEX colors from environment/background

🏆 BRAND LORE
brand_lore_visual - ICONIC brand-exclusive visual assets: 1/0
  - 1: official characters (Colonel, Eduardo, BK King), iconic props
  - 0: only logo, colors, or product without iconic character

brand_lore_visual_evidence - Detected asset description or "none"

brand_lore_text - Lore in description/comments: 1/0
  - 1: brand history mentions, secret recipe, campaign references
  - 0: only product or promotion mentions

brand_lore_text_evidence - 1-2 textual examples or "none"

KEY RULE LORE vs INFLUENCER:
- brand_character/lore: CANNOT work for another brand (Colonel → only KFC)
- influencer: COULD work for any brand (Brujillo Juan → could go to KFC)

📂 CATEGORIZATION
video_category - Category:
  - promo: offers, discounts, prices (2x1, coupons, "only X€")
  - product_launch: NEW product ("new", "now available", "arrived")
  - branding: entertainment/image without selling anything specific
  - unknown: not determinable

product_visible_early - Product visible in first 1.5s: 1/0
cta_visible - Visible call-to-action: 1/0
main_topic - Main topic in 3-8 words

💬 SENTIMENT
sentiment_score - Score (-1.0 to 1.0):
  - 1.0 to 0.6: enthusiastic
  - 0.5 to -0.5: indifferent
  - -0.6 to -1.0: critical

community_reaction - Reaction: entusiasta, indiferente, crítica

🎵 AUDIO
music - Music track name
