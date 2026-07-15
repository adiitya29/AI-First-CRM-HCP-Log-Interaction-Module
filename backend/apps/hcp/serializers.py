"""
HCP module serializers.
Handles validation and transformation for HealthcareProfessional and Interaction models.
"""
from rest_framework import serializers
from .models import HealthcareProfessional, Interaction


class HealthcareProfessionalSerializer(serializers.ModelSerializer):
    """Full serializer for HCP – used in list/detail/create/update."""

    full_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = HealthcareProfessional
        fields = [
            "id",
            "full_name",
            "first_name",
            "last_name",
            "specialty",
            "email",
            "phone",
            "institution",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "full_name", "created_at", "updated_at"]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()


class HealthcareProfessionalMinimalSerializer(serializers.ModelSerializer):
    """Lightweight serializer used when embedding HCP inside Interaction."""

    full_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = HealthcareProfessional
        fields = ["id", "full_name", "specialty", "institution"]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()


class InteractionSerializer(serializers.ModelSerializer):
    """Full serializer for Interaction – supports both form and chat log methods."""

    hcp_detail = HealthcareProfessionalMinimalSerializer(source="hcp", read_only=True)

    class Meta:
        model = Interaction
        fields = [
            "id",
            "hcp",
            "hcp_detail",
            "interaction_type",
            "log_method",
            "date",
            "notes",
            "products_discussed",
            "follow_up_required",
            "follow_up_date",
            "ai_summary",
            "ai_sentiment",
            "created_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "hcp_detail", "ai_summary", "ai_sentiment", "created_at", "updated_at"]

    def validate(self, attrs):
        """Ensure follow_up_date is provided when follow_up_required is True."""
        if attrs.get("follow_up_required") and not attrs.get("follow_up_date"):
            raise serializers.ValidationError(
                {"follow_up_date": "follow_up_date is required when follow_up_required is True."}
            )
        return attrs


class InteractionListSerializer(serializers.ModelSerializer):
    """Compact serializer for listing interactions (less data over the wire)."""

    hcp_name = serializers.SerializerMethodField()

    class Meta:
        model = Interaction
        fields = [
            "id",
            "hcp",
            "hcp_name",
            "interaction_type",
            "log_method",
            "date",
            "follow_up_required",
            "ai_sentiment",
            "created_at",
        ]

    def get_hcp_name(self, obj):
        return f"{obj.hcp.first_name} {obj.hcp.last_name}".strip()
