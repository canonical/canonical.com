"""
Ubuntu Pro Description page constants.

Update EFFECTIVE_DATE when the document is re-issued.
Update PAGE_NAVIGATION when sections are added, renamed, or removed.
The ids here must match the id attributes on the h2/h3 headings in the
_sections/ include files, and the section ids used in the export modal
checkboxes in index.html.
"""

EFFECTIVE_DATE = "26 JUNE 2026"

PAGE_NAVIGATION = [
    {"id": "introduction", "text": "Introduction"},
    {
        "id": "security-compliance",
        "text": "Security and compliance",
        "children": [
            {
                "id": "expanded-security-maintenance",
                "text": "1. Expanded Security Maintenance (ESM)",
            },
            {"id": "legacy-add-on", "text": "2. Legacy add-on"},
            {"id": "other-security-fixes", "text": "3. Other security fixes"},
            {
                "id": "certified-components",
                "text": "4. Certified components for compliance, hardening and audit",
            },
            {"id": "kernel-livepatch", "text": "5. Kernel Livepatch"},
            {
                "id": "access-to-other-services",
                "text": "6. Access to other services",
            },
            {
                "id": "subscription-limitations",
                "text": "7. Subscription limitations",
            },
        ],
    },
    {
        "id": "support",
        "text": "Support",
        "children": [
            {"id": "scope-of-support", "text": "8. Scope of Support"},
            {"id": "supported-products", "text": "9. Supported Products"},
            {"id": "exclusions", "text": "10. Exclusions"},
        ],
    },
    {
        "id": "support-services-process",
        "text": "Support Services Process",
        "children": [
            {"id": "service-initiation", "text": "11. Service initiation"},
            {
                "id": "submitting-support-requests",
                "text": "12. Submitting support requests",
            },
            {
                "id": "support-severity-levels",
                "text": "13. Support severity levels",
            },
            {"id": "customer-assistance", "text": "14. Customer assistance"},
            {"id": "hotfixes", "text": "15. Hotfixes"},
            {"id": "support-language", "text": "16. Support language"},
            {"id": "remote-sessions", "text": "17. Remote sessions"},
            {"id": "ask-for-peer-review", "text": "18. Ask for a Peer Review"},
            {
                "id": "management-escalation",
                "text": "19. Management escalation",
            },
            {"id": "levels-of-support", "text": "20. Levels of Support"},
        ],
    },
    {
        "id": "add-ons",
        "text": "Add-Ons",
        "children": [
            {"id": "managed-services", "text": "21. Managed Services"},
            {"id": "firefighting-support", "text": "22. Firefighting Support"},
            {"id": "ops-consultancy", "text": "23. OpsConsultancy"},
            {
                "id": "professional-support-services",
                "text": "24. Professional Support Services",
            },
            {"id": "embedded-services", "text": "25. Embedded Services"},
        ],
    },
    {"id": "definitions", "text": "Definitions"},
]
