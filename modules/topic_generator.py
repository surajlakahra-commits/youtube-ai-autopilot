"""
Topic Generator Module
Groq AI से नए-नए trading topics generate करता है
"""

import random
from groq import Groq

class TopicGenerator:
    def __init__(self, config):
        """Initialize topic generator with Groq API"""
        self.config = config
        self.client = Groq(api_key=config.get('groq_api_key'))
        
        self.default_topics = [
            "Stock Market के लिए Best Trading Strategies",
            "Cryptocurrency Trading में Profit कैसे करें",
            "Forex Trading के Basic Rules और Tips",
            "Day Trading vs Swing Trading - क्या अंतर है",
            "Technical Analysis सीखें - Complete Guide",
            "Risk Management in Trading - सही तरीका",
            "Stock Market में Investment के लिए पैसे कैसे लगाएं",
            "Options Trading - Beginners के लिए",
            "Trading Psychology - मानसिक मजबूती",
            "Crypto Market में सही समय पर Entry कैसे लें",
        ]
    
    def generate_topic(self):
        """
        Groq AI से नया topic generate करो
        अगर API fail हो तो default से select करो
        """
        try:
            prompt = """
You are a financial content expert. Generate ONE new, unique and engaging trading topic in Hindi for YouTube.
The topic should be:
- Educational and valuable for beginners
- Specific and actionable (not too general)
- Related to trading, stocks, crypto, forex, or investing
- Suitable for a 5-15 minute video

Return ONLY the topic title, nothing else. No numbering, no extra text.
            """
            
            message = self.client.messages.create(
                model="mixtral-8b-7b-32768",
                max_tokens=100,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            topic = message.content[0].text.strip()
            return topic
        
        except Exception as e:
            print(f"⚠️  Groq API error: {str(e)}")
            print("📚 Using default topic instead...")
            return random.choice(self.default_topics)
    
    def generate_multiple_topics(self, count=5):
        """Multiple topics एक साथ generate करो"""
        topics = []
        for i in range(count):
            topic = self.generate_topic()
            topics.append(topic)
        return topics
