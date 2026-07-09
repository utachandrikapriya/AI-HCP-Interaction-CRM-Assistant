import sys
import os
# Add parent directory to path so we can import app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import reset_current_interaction, get_current_interaction
from app.agent import (
    run_log_interaction,
    run_edit_interaction,
    run_generate_summary,
    run_validate_interaction,
    run_suggest_follow_up
)

def run_tests():
    print("--------------------------------------------------")
    print("Running HCP CRM Backend Unit Tests...")
    print("--------------------------------------------------")

    # Reset DB to initial clean state
    print("Step 1: Resetting database...")
    initial_state = reset_current_interaction()
    assert initial_state["hcpName"] == "", "Database reset failed: hcpName not empty"
    print("✅ Database reset successful.")

    # Test Tool 1: Log Interaction
    print("\nStep 2: Testing Tool 1 (Log Interaction)...")
    res1 = run_log_interaction(
        hcpName="Dr. Sarah Jenkins",
        interactionDate="2026-07-09",
        productsDiscussed=["OncoBoost", "CardioLife"],
        sentiment="Positive",
        interactionType="Meeting",
        materialsShared=["Clinical Study A"]
    )
    assert res1["status"] == "success", "Log interaction tool execution failed"
    data1 = res1["data"]
    assert data1["hcpName"] == "Dr. Sarah Jenkins", f"Expected 'Dr. Sarah Jenkins', got '{data1['hcpName']}'"
    assert "OncoBoost" in data1["productsDiscussed"], "Products discussed did not update"
    assert data1["sentiment"] == "Positive", "Sentiment did not update"
    print("✅ Log Interaction tool updates verified successfully.")

    # Test Tool 2: Edit Interaction
    print("\nStep 3: Testing Tool 2 (Edit Interaction)...")
    res2 = run_edit_interaction(
        sentiment="Neutral",
        productsDiscussed=["CardioMax"]
    )
    assert res2["status"] == "success", "Edit interaction tool execution failed"
    data2 = res2["data"]
    # Check that sentiment and products updated
    assert data2["sentiment"] == "Neutral", f"Expected sentiment 'Neutral', got '{data2['sentiment']}'"
    assert data2["productsDiscussed"] == ["CardioMax"], "Products discussed did not edit correctly"
    # Check that hcpName was preserved
    assert data2["hcpName"] == "Dr. Sarah Jenkins", f"HCP Name was overwritten! Got '{data2['hcpName']}'"
    print("✅ Edit Interaction tool verified. Requested fields updated, other fields preserved.")

    # Test Tool 3: Generate Summary
    print("\nStep 4: Testing Tool 3 (Generate Summary)...")
    res3 = run_generate_summary()
    assert res3["status"] == "success", "Generate summary tool execution failed"
    assert "summary" in res3 and len(res3["summary"]) > 0, "Summary text was not generated"
    print(f"✅ Generate Summary tool verified. Generated summary: \"{res3['summary']}\"")

    # Test Tool 4: Validate Interaction
    print("\nStep 5: Testing Tool 4 (Validate Interaction)...")
    res4 = run_validate_interaction()
    assert res4["status"] == "success", "Validate interaction tool execution failed"
    assert "missingFields" in res4, "Validation response missing missingFields key"
    assert len(res4["missingFields"]) > 0, "Validation did not find missing fields"
    # Verify specialty is missing (we haven't set it)
    assert "Specialty" in res4["missingFields"], "Specialty should be listed as missing"
    print("✅ Validate Interaction tool verified. Correctly identified missing fields:")
    for field in res4["missingFields"][:3]:
        print(f" - Missing: {field}")
    print(" ...")

    # Test Tool 5: Suggest Follow-up
    print("\nStep 6: Testing Tool 5 (Suggest Follow-up)...")
    res5 = run_suggest_follow_up()
    assert res5["status"] == "success", "Suggest follow-up tool execution failed"
    assert "suggestions" in res5 and len(res5["suggestions"]) > 0, "Follow-up suggestions not generated"
    print("✅ Suggest Follow-up tool verified. Generated suggestions:")
    print(res5["suggestions"])

    print("\n--------------------------------------------------")
    print("ALL TESTS PASSED SUCCESSFULLY!")
    print("--------------------------------------------------")

if __name__ == "__main__":
    run_tests()
