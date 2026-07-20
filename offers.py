# offers.py

MOBILE_OFFERS = [
    {
        "id": 1,
        "name": "Starter Line",
        "category": "Mobile Line",

        "price": 7,
        "currency": "JOD",
        "billing": "month",

        "description": "Affordable mobile plan for light users.",

        "benefits": [
            "10 GB Internet",
            "300 Local Minutes",
            "300 SMS",
            "No Contract"
        ],

        "tags": [
            "student",
            "cheap",
            "low_budget",
            "light_usage",
            "single_person",
            "basic_calls"
        ]
    },

    {
        "id": 2,
        "name": "Smart Line",
        "category": "Mobile Line",

        "price": 12,
        "currency": "JOD",
        "billing": "month",

        "description": "Balanced plan for everyday users.",

        "benefits": [
            "35 GB Internet",
            "Unlimited On-Net Calls",
            "500 Local Minutes",
            "Free Caller ID"
        ],

        "tags": [
            "employee",
            "family",
            "average_usage",
            "social_media",
            "daily_use",
            "medium_budget"
        ]
    },

    {
        "id": 3,
        "name": "Unlimited Max",
        "category": "Mobile Line",

        "price": 22,
        "currency": "JOD",
        "billing": "month",

        "description": "Premium unlimited mobile experience.",

        "benefits": [
            "Unlimited Internet",
            "Unlimited Calls",
            "Unlimited SMS",
            "5G Included"
        ],

        "tags": [
            "business",
            "heavy_usage",
            "gaming",
            "streaming",
            "remote_work",
            "high_budget",
            "unlimited"
        ]
    }
]


INTERNET_OFFERS = [
    {
        "id": 101,
        "name": "Fiber 100",
        "category": "Internet",

        "price": 20,
        "currency": "JOD",
        "billing": "month",

        "description": "Reliable internet for everyday home use.",

        "benefits": [
            "100 Mbps",
            "Unlimited Usage",
            "Free Router",
            "24/7 Technical Support"
        ],

        "tags": [
            "student",
            "small_family",
            "youtube",
            "browsing",
            "low_budget"
        ]
    },

    {
        "id": 102,
        "name": "Fiber 300",
        "category": "Internet",

        "price": 30,
        "currency": "JOD",
        "billing": "month",

        "description": "High-speed internet for families and gamers.",

        "benefits": [
            "300 Mbps",
            "Unlimited Usage",
            "Wi-Fi 6 Router",
            "Priority Technical Support"
        ],

        "tags": [
            "family",
            "gaming",
            "streaming",
            "netflix",
            "work_from_home",
            "medium_budget"
        ]
    },

    {
        "id": 103,
        "name": "Fiber 600",
        "category": "Internet",

        "price": 45,
        "currency": "JOD",
        "billing": "month",

        "description": "Ultra-fast fiber for professionals and heavy users.",

        "benefits": [
            "600 Mbps",
            "Unlimited Usage",
            "Premium Router",
            "Priority Installation",
            "Premium Technical Support"
        ],

        "tags": [
            "business",
            "office",
            "remote_work",
            "content_creator",
            "heavy_usage",
            "high_budget"
        ]
    }
]


ALL_OFFERS = {
    "mobile": MOBILE_OFFERS,
    "internet": INTERNET_OFFERS
}


def get_offers_prompt():
    """
    Convert all available offers into a clean text format
    that will be appended to the system prompt.
    """

    prompt = "\n========== AVAILABLE OFFERS ==========\n\n"

    # Mobile Offers
    prompt += "MOBILE OFFERS:\n\n"

    for offer in MOBILE_OFFERS:
        prompt += f"Offer ID: {offer['id']}\n"
        prompt += f"Name: {offer['name']}\n"
        prompt += f"Category: {offer['category']}\n"
        prompt += (
            f"Price: {offer['price']} "
            f"{offer['currency']} / {offer['billing']}\n"
        )
        prompt += f"Description: {offer['description']}\n"

        prompt += "Benefits:\n"
        for benefit in offer["benefits"]:
            prompt += f"  - {benefit}\n"

        prompt += "Tags: "
        prompt += ", ".join(offer["tags"])
        prompt += "\n\n"

    # Internet Offers
    prompt += "INTERNET OFFERS:\n\n"

    for offer in INTERNET_OFFERS:
        prompt += f"Offer ID: {offer['id']}\n"
        prompt += f"Name: {offer['name']}\n"
        prompt += f"Category: {offer['category']}\n"
        prompt += (
            f"Price: {offer['price']} "
            f"{offer['currency']} / {offer['billing']}\n"
        )
        prompt += f"Description: {offer['description']}\n"

        prompt += "Benefits:\n"
        for benefit in offer["benefits"]:
            prompt += f"  - {benefit}\n"

        prompt += "Tags: "
        prompt += ", ".join(offer["tags"])
        prompt += "\n\n"

    return prompt