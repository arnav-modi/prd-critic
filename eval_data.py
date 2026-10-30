PRDS = [
    {
        "name": "dark_mode",
        "text": """Feature: Dark Mode (notes app)

Goal: Make the app more modern and increase usage.

Requirements:
1. Users can switch between light and dark mode from Settings.
2. Dark mode should look good on all screens.
3. The app must follow the phone's system theme automatically.
4. The app must always stay in the theme the user chose manually, even if the system theme changes.

Success: Increase daily active users.
""",
        "flaws": [
            {"id": "dm1", "dimension": "success_metrics",
             "anchors": ["Increase daily active users"]},
            {"id": "dm2", "dimension": "requirements_quality",
             "anchors": ["look good on all screens"]},
            {"id": "dm3", "dimension": "consistency",
             "anchors": ["follow the phone's system theme automatically",
                         "always stay in the theme the user chose manually"]},
            {"id": "dm4", "dimension": "scope", "anchors": ["(missing)"],
             "keywords": ["non-goal", "out of scope", "not in scope", "scope"]},
        ],
    },
    {
        "name": "sms_password_reset",
        "text": """Feature: Password Reset by SMS

Goal: Reduce support tickets about forgotten passwords.

Requirements:
1. Users can request a reset code by SMS.
2. A reset code is valid for 10 minutes.
3. The reset process must be secure and fast.
4. Users can request as many codes as they want.
5. A reset code stays valid until the user uses it.

Success: Fewer support tickets.
""",
        "flaws": [
            {"id": "sms1", "dimension": "success_metrics",
             "anchors": ["Fewer support tickets"]},
            {"id": "sms2", "dimension": "requirements_quality",
             "anchors": ["secure and fast"]},
            {"id": "sms3", "dimension": "consistency",
             "anchors": ["valid for 10 minutes",
                         "stays valid until the user uses it"]},
            {"id": "sms4", "dimension": "edge_cases",
             "anchors": ["as many codes as they want"]},
        ],
    },
    {
        "name": "weekly_digest",
        "text": """Feature: Weekly Email Digest

Goal: Bring inactive users back to the product.

Requirements:
1. Send a weekly email summarizing recent activity in the user's account.
2. Emails should be personalized and relevant.
3. Send the digest to all users every Monday at 9am.
4. Only send the digest to users who were active in the last 30 days.
5. Users can unsubscribe with one click.

Success: Reactivate 10% of users inactive for 60+ days (baseline: 2%) within 90 days of launch.
""",
        # NOTE: the Success line is well written on purpose (a "control").
        "flaws": [
            {"id": "wd1", "dimension": "requirements_quality",
             "anchors": ["personalized and relevant"]},
            {"id": "wd2", "dimension": "consistency",
             "anchors": ["Bring inactive users back",
                         "Only send the digest to users who were active",
                         "to all users every Monday"]},
            {"id": "wd3", "dimension": "edge_cases", "anchors": ["(missing)"],
             "keywords": ["time zone", "timezone", "no activity", "nothing to",
                          "empty", "bounce"]},
        ],
    },
    {
        "name": "in_app_search",
        "text": """Feature: In-App Search

Goal: Help users find items faster.

Requirements:
1. A search bar appears on the home screen.
2. Results appear instantly.
3. Search covers products, orders, and help articles.
4. Search supports all languages.
5. Launch next month to all users in all regions.

Success: Reduce the average time to find an item from 45 seconds to 20 seconds within 60 days of launch.
""",
        # NOTE: the Success line is well written on purpose (a "control").
        "flaws": [
            {"id": "sr1", "dimension": "requirements_quality",
             "anchors": ["Results appear instantly"]},
            {"id": "sr2", "dimension": "scope",
             "anchors": ["supports all languages", "all users in all regions"]},
            {"id": "sr3", "dimension": "edge_cases", "anchors": ["(missing)"],
             "keywords": ["no results", "typo", "empty", "misspell", "no match"]},
        ],
    },
    {
        "name": "loyalty_points",
        "text": """Feature: Loyalty Points (online store)

Goal: Increase customer retention.

Requirements:
1. Customers earn 1 point for every $1 spent.
2. 100 points can be redeemed for a $5 discount.
3. The points system should be easy to understand.
4. Points never expire.
5. Points expire 12 months after they are earned.

Success: Customers will be happier and stick around longer.
""",
        "flaws": [
            {"id": "lp1", "dimension": "success_metrics",
             "anchors": ["happier and stick around longer"]},
            {"id": "lp2", "dimension": "requirements_quality",
             "anchors": ["easy to understand"]},
            {"id": "lp3", "dimension": "consistency",
             "anchors": ["Points never expire",
                         "expire 12 months after they are earned"]},
            {"id": "lp4", "dimension": "edge_cases", "anchors": ["(missing)"],
             "keywords": ["refund", "return", "cancel"]},
        ],
    },
]
