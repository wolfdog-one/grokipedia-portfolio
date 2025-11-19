curl https://api.x.ai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer xai-rpiAOzVBiyHBn04iqtSdERD9gTAfpnKoBC9KRgJF8LoBE2LnTn9QqJHTjTiZaO2R5rJux8ee8lyFfS2j" \
  -d '{
    "messages": [
      { "role": "system", "content": "You are Grok." },
      { "role": "user", "content": "Just say: SUCCESS - the key works!" }
    ],
    "model": "grok-beta",
    "temperature": 0
  }'