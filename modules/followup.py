import pandas as pd


def get_followup_recommendations(df):

    if df.empty:
        return pd.DataFrame()

    recommendations = df.copy()

    # Convert follow-up values into a consistent format
    recommendations["requires_followup"] = (
        recommendations["requires_followup"]
        .fillna(0)
        .astype(int)
    )

    # Identify enquiries that need attention
    followups = recommendations[
        (
            recommendations["requires_followup"] == 1
        )
        |
        (
            (recommendations["priority"] == "High")
            &
            (recommendations["status"] != "Resolved")
        )
    ].copy()

    # Exclude resolved enquiries
    followups = followups[
        followups["status"] != "Resolved"
    ]

    # Add a recommendation for the clinic staff
    def suggest_action(row):

        if row["priority"] == "High":
            return "Contact patient as soon as possible"

        elif row["status"] == "Open":
            return "Review and respond to enquiry"

        else:
            return "Check progress and follow up"

    followups["recommended_action"] = followups.apply(
        suggest_action,
        axis=1
    )

    return followups[
        [
            "enquiry_id",
            "patient_name",
            "category",
            "priority",
            "status",
            "recommended_action"
        ]
    ]