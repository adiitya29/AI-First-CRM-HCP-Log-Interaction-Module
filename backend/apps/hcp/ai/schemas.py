"""
Pydantic schemas for LangChain structured output parsing.

Design principle:
  Fields use Optional/None as default wherever possible so the frontend can
  distinguish "AI explicitly extracted this value" from "AI left this as default".
  Only fields that are explicitly mentioned in the user's message should be non-null,
  allowing the frontend to do a selective merge (update only mentioned fields).
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class InteractionExtraction(BaseModel):
    """
    Extracted data from a natural language interaction log provided by a field rep.
    ALL fields default to None/empty — only populate a field if it is EXPLICITLY
    mentioned in the user's message. Do not guess or infer values that aren't stated.
    """

    hcp_name: Optional[str] = Field(
        default=None,
        description=(
            "The name of the Healthcare Professional mentioned (e.g., 'Dr. Sharma'). "
            "Set to null if not explicitly mentioned."
        )
    )

    interaction_type: Optional[str] = Field(
        default=None,
        description=(
            "The type of interaction — one of: 'in_person', 'phone', 'email', 'virtual', 'event'. "
            "Set to null if the user did NOT explicitly mention the interaction type."
        )
    )

    date: Optional[str] = Field(
        default=None,
        description=(
            "The date of the interaction in YYYY-MM-DD format. "
            "Set to null if not explicitly mentioned."
        )
    )

    time: Optional[str] = Field(
        default=None,
        description=(
            "The time of the interaction in HH:MM 24-hour format. "
            "Convert naturally: '3pm' → '15:00', '10:30am' → '10:30'. "
            "Set to null if not explicitly mentioned."
        )
    )

    attendees: Optional[List[str]] = Field(
        default=None,
        description=(
            "A list of attendee names (people other than the HCP) present at the interaction. "
            "Set to null if no attendees are mentioned. "
            "Do NOT include the HCP's name here."
        )
    )

    notes: Optional[str] = Field(
        default=None,
        description=(
            "ONLY discussion topics, product information shared, HCP observations, and key talking points. "
            "Do NOT include attendee names, outcomes, samples distributed, or follow-up info here. "
            "Set to null if no discussion topics are mentioned."
        )
    )

    outcomes: Optional[str] = Field(
        default=None,
        description=(
            "Key results, agreements, or commitments made DURING the interaction "
            "(e.g., 'HCP agreed to prescribe OncoBoost', 'Rep will send Phase III data PDF'). "
            "Do NOT put samples or materials here. "
            "Set to null if no specific outcomes are mentioned."
        )
    )

    products_discussed: Optional[List[str]] = Field(
        default=None,
        description=(
            "A list of specific medical product, drug, or device NAMES that were discussed. "
            "Set to null if none are mentioned."
        )
    )

    samples_distributed: Optional[List[str]] = Field(
        default=None,
        description=(
            "A list of product samples physically given to the HCP during the visit "
            "(e.g., ['OncoBoost 10mg sample pack', 'CardioPlus brochure']). "
            "Set to null if no samples or materials were distributed."
        )
    )

    follow_up_required: Optional[bool] = Field(
        default=None,
        description=(
            "True ONLY if the representative explicitly mentions needing to follow up, "
            "schedule a next meeting, or send something. "
            "Set to null if not mentioned."
        )
    )

    follow_up_date: Optional[str] = Field(
        default=None,
        description=(
            "The date for the follow-up in YYYY-MM-DD format. "
            "Set to null if not mentioned."
        )
    )

    ai_sentiment: Optional[str] = Field(
        default=None,
        description=(
            "The sentiment of the interaction from the HCP's perspective. "
            "Must be EXACTLY one of: 'positive', 'neutral', or 'negative'. "
            "positive = HCP was receptive, enthusiastic, or agreed to next steps. "
            "negative = HCP was dismissive, skeptical, or raised strong concerns. "
            "Set to null if the user did NOT explicitly mention or imply the HCP's mood/sentiment."
        )
    )

    ai_summary: Optional[str] = Field(
        default=None,
        description=(
            "A concise 1-2 sentence summary of the ENTIRE interaction. "
            "Always generate this even if not explicitly requested."
        )
    )
