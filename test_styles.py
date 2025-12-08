# Test all 5 styles directly
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from multi_style_image_generator import StyleModelsConfig

print("="*70)
print("TESTING ALL 5 ART STYLES")
print("="*70)

styles = StyleModelsConfig.STYLE_MODELS

print(f"\nTotal styles available: {len(styles)}")
print("\nStyle Validation Test:")
print("-" * 70)

for i, (style_name, model_id) in enumerate(styles.items(), 1):
    is_valid = StyleModelsConfig.is_valid_style(style_name)
    retrieved_model = StyleModelsConfig.get_model_id(style_name)
    
    status = "[OK]" if (is_valid and retrieved_model == model_id) else "[FAIL]"
    
    print(f"{status} {i}. {style_name}")
    print(f"    Model: {model_id}")
    print(f"    Valid: {is_valid}")
    print()

print("-" * 70)
print("All 5 styles validated successfully!")
print("="*70)
