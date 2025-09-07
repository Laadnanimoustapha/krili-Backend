# 🛡️ KRILI Chat Moderation — Unified README

A complete guide that combines the Integration Guide, Full Documentation, and System Summary into one place.

---

## ✨ Overview

A comprehensive, production-ready chat moderation system that detects and blocks:
- Personal Information: emails, phone numbers, addresses
- Payment links: PayPal, Venmo, CashApp, Zelle
- External platforms: WhatsApp, Telegram, Discord, etc.
- Smart bypass attempts: obfuscated content like "zero six one two"
- Intent analysis: context-aware detection

Core features:
- Regex + ML detection with confidence scoring
- Real-time API and dashboard (http://localhost:5000)
- SQLite logging, stats, health checks
- Configurable thresholds, patterns, and warnings

---

## 🚀 Quick Start

1) Install dependencies
```bash
python install_moderation_deps.py
```

2) Run examples
```bash
python chat_moderation_system.py example
```

3) Start API server
```bash
python chat_moderation_system.py api
```

4) Access UI
- Dashboard: http://localhost:5000
- Health: http://localhost:5000/health

5) (Optional) Train models
```bash
python chat_moderation_system.py train
```

---

## 🎯 Integration Options

### Method 1 — JavaScript (Recommended)
Add to your Chat.html (near </body>):
```html
<script src="http://localhost:5000/static/krili_chat_integration.js"></script>
```
Or serve a local copy:
```html
<script src="js/krili_chat_integration.js"></script>
```
Behavior:
- ✅ Intercepts outgoing messages
- 🔍 Moderates in real-time (10–50ms)
- 🚫 Blocks violations with warnings
- ⚠️ Allows but warns for borderline content

### Method 2 — Direct API
```javascript
// Moderate a single message
fetch('http://localhost:5000/moderate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: "User's message here",
    user_id: 'user123',
    context: { channel: 'general', timestamp: new Date().toISOString() }
  })
})
.then(r => r.json())
.then(result => {
  if (result.is_flagged) {
    if (result.action === 'block') {
      showError(result.warning_message);
      // don't send message
    } else {
      showWarning(result.warning_message);
      // optionally send
    }
  } else {
    sendMessage();
  }
});
```

API endpoints:
- POST /moderate — single message
- POST /batch_moderate — multiple messages
- GET /stats — system statistics
- GET /health — system health
- GET /flagged — flagged messages

---

## 📊 Monitoring & Dashboard
Visit http://localhost:5000 to view:
- Real-time stats and message tests
- Violation breakdown and risk scores
- System health and component status

---

## ⚙️ Configuration

Thresholds (in Config class):
```python
REGEX_CONFIDENCE = 0.9
ML_CONFIDENCE_THRESHOLD = 0.7
COMBINED_CONFIDENCE_THRESHOLD = 0.6  # Lower = more sensitive
```

Custom warning messages:
```python
WARNING_MESSAGES = {
  "personal_info": "🚫 Sharing personal info is not allowed...",
  "external_platform": "🚫 Mentions of external platforms are not allowed...",
  "off_platform_transaction": "🚫 Attempting to move transactions is not allowed...",
  "general": "🚫 This message violates our guidelines..."
}
```

Add custom regex patterns:
```python
REGEX_PATTERNS = {
  "custom_pattern": [
    r"your_custom_regex_here",
    r"another_pattern"
  ]
}
```

---

## 🧠 ML Training & Continuous Learning

Train with your data:
```python
training_data = [
  ("Safe message example", 0),
  ("Violation example", 1)
]
engine.ml_detector.train_models(training_data)
```

Feedback-based learning:
```python
engine.train_with_feedback(
  message_id=123,
  is_false_positive=True,
  admin_notes="This was actually safe"
)
```

Export training data:
```python
filename = engine.export_training_data()
print(f"Exported to {filename}")
```

---

## 🧪 Example Usage (Code)

```python
from chat_moderation_system import ModerationEngine
engine = ModerationEngine()
result = engine.moderate_message(
  message="Contact me at john@email.com",
  user_id="user123"
)
if result['is_flagged']:
  print(f"🚫 {result['action']}: {result['warning_message']}")
  print(f"Confidence: {result['confidence']:.2%}")
else:
  print("✅ Message is safe")
```

Batch processing:
```python
messages = [
  ("Hello, how are you?", "user1"),
  ("Contact me at my email", "user2"),
  ("What's the price?", "user3"),
]
results = engine.batch_moderate(messages)
flagged_count = sum(1 for r in results if r['is_flagged'])
print(f"Flagged {flagged_count} / {len(results)}")
```

---

## 📈 Performance
- Single message: ~10–50ms
- Batch of 100: ~500ms–2s
- Memory: ~50–200MB
- Accuracy: 95%+ with training

---

## 🔒 Security Notes
- Runs on localhost by default; use HTTPS and auth in production
- Rate limit the API; monitor false positives
- SQLi protection, input sanitization, audit logging
- Privacy: no sensitive data stored in logs

---

## 🛠️ Troubleshooting

Common issues:
- API not accessible: check http://localhost:5000/health, ensure port 5000 is free
- Messages not moderated: check browser console, ensure script loads, test API directly
- Too many false positives: lower thresholds, add training data, tune regex
- Performance: use batching and caching for repeated patterns

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 📁 File Structure
```
PYTHON/
├── chat_moderation_system.py      # Main system
├── install_moderation_deps.py     # Dependency installer
├── krili_chat_integration.js      # Frontend integration
├── demo_integration.html          # Live demo interface
├── README.md                      # This unified README
├── chat_moderation.db             # SQLite DB (auto-created)
├── models/                        # Trained ML models (auto)
└── training_data_*.json           # Exported training data
```

---

## 🏆 System Highlights
- Multi-layer detection: Regex (fast) + ML (smart) → combined decision
- Smart bypass detection: obfuscation, number words, hints
- Real-time dashboard and health monitoring
- Production-ready with continuous learning

---

## 📞 Support & Next Steps
- Docs and examples are now unified here
- Dashboard: http://localhost:5000
- Health: http://localhost:5000/health
- Quick commands:
```bash
python install_moderation_deps.py
python chat_moderation_system.py example
python chat_moderation_system.py api
python chat_moderation_system.py train
```

---

✅ Your KRILI chat is now protected with ML-powered moderation! If you’d like, I can remove or link the original separate docs and keep this as the single source of truth.