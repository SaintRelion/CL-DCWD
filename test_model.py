from ai.predictive_model import PredictiveModel
from database.db_locations import locations


def run_test():
    try:
        pm = PredictiveModel()
        print("\n" + "=" * 40)
        print("  AI INDEPENDENT RISK TEST (CLI)")
        print("=" * 40)

        # Test a few specific locations
        test_ids = [1, 5, 10, 20]

        for loc_id in test_ids:
            loc_data = next((l for l in locations if l[0] == loc_id), None)
            name = f"{loc_data[1]} - {loc_data[2]}" if loc_data else f"ID {loc_id}"

            report = pm.get_daily_risk_report(loc_id)

            print(f"\n📍 {name}")
            print(f"  🚰 No Water:    {report[1]:>6.2f}%")
            print(f"  💧 Leak:        {report[2]:>6.2f}%")
            print(f"  🟫 Dirty Water: {report[3]:>6.2f}%")

        print("\n" + "=" * 40)

    except Exception as e:
        print(f"\n[FATAL ERROR] {e}")


if __name__ == "__main__":
    run_test()
