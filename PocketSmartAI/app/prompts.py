SYSTEM_PROMPT = '''
You are PocketSmart AI, a practical budget planning assistant.
Return ONLY valid JSON. Do not invent exact live prices, stock, ratings, URLs, vendor contracts,
or product IDs. Use estimated prices and broad search links. Keep recommendations within budget.
'''

HOME_PROMPT = '''
Create budget-aware home interior recommendations for this input:
{payload}
Return JSON with summary, allocation, and recommendations. Each recommendation needs
name, category, estimated_price, platform, and reason. Use Amazon, IKEA or Flipkart.
Provide 6-10 useful options and keep total estimated spend within the budget.
'''

PARTY_PROMPT = '''
Create a party budget plan for India for this input:
{payload}
Return JSON with summary, allocation, and recommendations. Each recommendation needs
name, category, estimated_price, platform, and reason. Use Swiggy, Zomato, OYO or Amazon.
Provide 6-10 useful options and keep total estimated spend within the budget.
'''

JEWELRY_PROMPT = '''
Recommend jewelry for this input:
{payload}
If an outfit image is attached, use broad visual cues such as dominant color, neckline,
formality and style; do not identify the person.
Return JSON with summary, allocation, and recommendations. Each recommendation needs
name, category, estimated_price, platform, and reason. Use Amazon or Flipkart.
Provide 6-8 useful options and keep total estimated spend within the budget.
'''
