"""Test pour vérifier que les flèches sont bien créées"""

from phase_diagram import create_phase_diagram
import logging

logging.basicConfig(level=logging.INFO)

print("\n" + "="*70)
print("TEST DES FLÈCHES PAR TYPE D'ÉQUILIBRE")
print("="*70)

types_to_test = ['centre', 'foyer_stable', 'foyer_instable', 'noeud_stable', 'selle']

for eq_type in types_to_test:
    print(f"\n[{eq_type}]")
    fig = create_phase_diagram(eq_type)
    
    num_traces = len(fig.data)
    num_annotations = len(fig.layout.annotations) if fig.layout.annotations else 0
    
    print(f"  Traces (trajectoires): {num_traces}")
    print(f"  Annotations (flèches): {num_annotations}")
    
    if num_annotations == 0:
        print(f"  ⚠️  AUCUNE FLÈCHE DÉTECTÉE!")
    else:
        print(f"  ✓ Flèches présentes")

print("\n" + "="*70 + "\n")
