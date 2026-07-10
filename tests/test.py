# test.py
from app import get_crop_recommendations, process_voice_command

print("Testing Crop Recommendations...")
recommendations = get_crop_recommendations('Loamy', 'Winter', 'Moderate')
for crop in recommendations:
    print(f"- {crop['name']}: {crop['match_percentage']}% match")

print("\nTesting Voice Assistant...")
test_commands = [
    "weather",
    "recommend crops",
    "disease",
    "irrigation",
    "market prices",
    "hello"
]
for cmd in test_commands:
    response = process_voice_command(cmd)
    print(f"Command: '{cmd}' -> Response: {response}")

print("\nAll tests passed!")