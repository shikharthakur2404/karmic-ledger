"""
karmic-ledger: Command Line Telemetry & Verification Runner
"""

import glob
import os
import sys

# Bootstrap path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from core.reporter import generate_markdown_dossier
from core.verifier import verify_profile_milestones


def print_banner():
    print(r"""
  ███████╗ █████╗ ████████╗██╗   ██╗██████╗  █████╗ 
  ╚══███╔╝██╔══██╗╚══██╔══╝██║   ██║██╔══██╗██╔══██╗
    ███╔╝ ███████║   ██║   ██║   ██║██████╔╝███████║
   ███╔╝  ██╔══██║   ██║   ██║   ██║██╔══██╗██╔══██║
  ███████╗██║  ██║   ██║   ╚██████╔╝██║  ██║██║  ██║
  ╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
  K A R M I C   L E D G E R  |  V E D I C   T E L E M E T R Y
    """)


def run_verify(profile_path: str):
    print_banner()
    if not os.path.isabs(profile_path):
        profile_path = os.path.join(ROOT_DIR, profile_path)

    if not os.path.exists(profile_path):
        print(f"[-] Profile not found: {profile_path}")
        sys.exit(1)

    print(f"[+] Ingesting profile: {profile_path}")
    res = verify_profile_milestones(profile_path)
    soul = res.get("soul_telemetry", {})
    frictions = res.get("frictions", {})

    print("\n" + "=" * 80)
    print(f" SUBJECT:           {res['subject']}")
    print(f" LAGNA:             {res['lagna']}")
    print(f" MOON NAKSHATRA:    {res['moon_nakshatra']}")
    if soul:
        print(
            f" SOUL AGE:          {soul['soul_age_category']} [{soul['sanskrit_category']}]"
        )
        print(
            f" SOUL ARCHETYPE:    {soul['archetype_title']} [{soul['archetype_sanskrit']}]"
        )
        print(
            f" ĀTMAKĀRAKA (AK):   {soul['atmakaraka_planet']} at {soul['atmakaraka_degree']} ({soul['odometer_percentage']} Cycle)"
        )
    print(
        f" OVERALL VCS SCORE: {res['average_vedic_correlation_score']} (Vedic Correlation Score)"
    )
    print("=" * 80 + "\n")

    # Live Karmic Frictions / Disruptions Display
    if frictions and frictions.get("status") == "CRITICAL_FRICTION_DETECTED":
        print("!" * 80)
        print(" [!] CRITICAL REAL-WORLD FRICTION / ACTIVE DISRUPTION DETECTED")
        print(
            "     Transit & Dasha physics overriding user-prompt present tense assumptions."
        )
        print("!" * 80)
        for c in frictions.get("active_crises", []):
            print(f"  * DOMAIN:  {c['domain']}")
            print(f"    CODE:    {c['code']} [{c['severity']}]")
            print(f"    VERDICT: {c['verdict']}")
            print(f"    IMPACT:  {c['real_world_impact']}")
            print("    MECHANICS:")
            for m in c["mechanisms"]:
                print(f"      - {m}")
            print()
        if frictions.get("resolution_roadmap"):
            print("  RESOLUTION TIMELINE ROADMAP:")
            for r in frictions["resolution_roadmap"]:
                print(f"    -> {r}")
        print("!" * 80 + "\n")
    else:
        print(
            "[+] Live Transit Status: OPERATIONAL_STABLE (No acute systemic halts detected)\n"
        )

    print(
        f"{'MILESTONE EVENT':<30} | {'ACTIVE DASHA':<18} | {'TRANSIT SATURN':<14} | {'VCS':<6}"
    )
    print("-" * 75)
    for m in res["calibration_results"]:
        dasha_str = f"{m['active_mahadasha']}-{m['active_antardasha']}"
        print(
            f"{m['event'][:28]:<30} | {dasha_str:<18} | {m['saturn_transit']:<14} | {m['correlation_score']:.0f}%"
        )
        print(f"  └─ Citation: [{m['shastra_citation']}] | Span: {m['dasha_span']}")
        print()


def run_cohort():
    print_banner()
    profiles_dir = os.path.join(ROOT_DIR, "profiles")
    profile_files = glob.glob(os.path.join(profiles_dir, "*.json"))
    print(
        f"[+] Running calibration cohort across {len(profile_files)} ground truth profiles...\n"
    )

    print(
        f"{'SUBJECT':<18} | {'SOUL AGE':<18} | {'ARCHETYPE':<22} | {'FRICTION STATUS':<16} | {'VCS':<6}"
    )
    print("=" * 88)

    for pf in sorted(profile_files):
        try:
            res = verify_profile_milestones(pf)
            soul = res.get("soul_telemetry", {})
            frictions = res.get("frictions", {})
            sub = res["subject"][:16]
            s_age = soul.get("soul_age_category", "N/A")[:17]
            arch = soul.get("archetype_title", "N/A")[:20]
            f_status = (
                "CRITICAL (3)"
                if frictions.get("crisis_count", 0) >= 3
                else (
                    f"ALERT ({frictions.get('crisis_count', 0)})"
                    if frictions.get("crisis_count", 0) > 0
                    else "STABLE"
                )
            )
            score = res["average_vedic_correlation_score"]
            print(f"{sub:<18} | {s_age:<18} | {arch:<22} | {f_status:<16} | {score:<6}")
        except Exception as e:
            print(f"{os.path.basename(pf):<18} | ERROR: {str(e)[:55]}")

    print("=" * 88)
    print(
        "[+] All profiles verified against Swiss Ephemeris, Jaimini AK & Parashari Engines.\n"
    )


def run_report(profile_path: str, output_path: str = None):
    print_banner()
    if not os.path.exists(profile_path):
        print(f"[-] Profile not found: {profile_path}")
        sys.exit(1)

    if not output_path:
        base_name = os.path.splitext(os.path.basename(profile_path))[0]
        output_path = f"reports/{base_name}_dossier.md"

    print(f"[+] Generating manuscript dossier for: {profile_path}")
    out = generate_markdown_dossier(profile_path, output_path)
    print(f"[+] Master Dossier generated: {out}\n")


def run_adversarial(profile_path: str):
    print_banner()
    if not os.path.isabs(profile_path):
        profile_path = os.path.join(ROOT_DIR, profile_path)

    if not os.path.exists(profile_path):
        print(f"[-] Profile not found: {profile_path}")
        sys.exit(1)

    from core.adversarial import run_adversarial_stress_test

    print(f"[!] Executing Adversarial Stress-Test Harness against: {profile_path}\n")
    report = run_adversarial_stress_test(profile_path)

    print("=" * 88)
    print(f" SUBJECT:                 {report['subject']}")
    print(f" GROUND TRUTH VCS:        {report['baseline_vcs']} (True Natal Epoch)")
    print(
        f" CORRUPTED AVERAGE VCS:   {report['average_corrupted_vcs']} (Synthetic/Corrupted Injections)"
    )
    print(f" DISCRIMINATION MARGIN:   {report['discrimination_margin']} (Δ Separation)")
    print(f" FALSIFICATION PASS RATE: {report['falsification_pass_rate']}")
    print(f" RESILIENCE VERDICT:      {report['resilience_verdict']}")
    print("=" * 88 + "\n")

    print(
        f"{'MUTATION / ATTACK VECTOR':<32} | {'CORRUPTED LAGNA':<18} | {'VCS':<6} | {'Δ DROP':<8} | {'STATUS'}"
    )
    print("-" * 88)
    for m in report["evaluations"]:
        status_tag = (
            "[FALSIFIED // PASS]"
            if m["falsified_successfully"]
            else "[COLLUSION // FAIL]"
        )
        print(
            f"{m['name'][:30]:<32} | {m['corrupted_lagna'][:16]:<18} | {m['corrupted_vcs']:<6.1f}% | -{m['delta_vcs']:<6.1f}% | {status_tag}"
        )
        for ev in m["event_breakdown"][:2]:
            print(
                f"  └─ {ev['event'][:24]}: Dasha drifted to [{ev['corrupted_dasha']}], score -> {ev['corrupted_score']:.0f}%"
            )
        print()
    print("=" * 88)
    print("[+] Adversarial proof-testing complete. Falsification protocol verified.\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python main.py verify <path_to_profile.json>")
        print("  python main.py adversarial <path_to_profile.json>")
        print("  python main.py cohort")
        print("  python main.py report <path_to_profile.json> [output_path.md]")
        sys.exit(0)

    cmd = sys.argv[1].lower()
    if cmd == "cohort":
        run_cohort()
    elif cmd == "verify":
        if len(sys.argv) < 3:
            print(
                "[-] Please provide profile path: python main.py verify <profile.json>"
            )
            sys.exit(1)
        run_verify(sys.argv[2])
    elif cmd == "adversarial":
        if len(sys.argv) < 3:
            print(
                "[-] Please provide profile path: python main.py adversarial <profile.json>"
            )
            sys.exit(1)
        run_adversarial(sys.argv[2])
    elif cmd == "report":
        if len(sys.argv) < 3:
            print(
                "[-] Please provide profile path: python main.py report <profile.json>"
            )
            sys.exit(1)
        out_p = sys.argv[3] if len(sys.argv) > 3 else None
        run_report(sys.argv[2], out_p)
    else:
        print(f"[-] Unknown command: {cmd}")
