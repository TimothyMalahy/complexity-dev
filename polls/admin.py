# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import (
    Topic,
    Subject,
    SubjectScore,
    SubjectLinks,
    Vote,
    Ranking,
    TopicGroup,
)
# from guardian.admin import GuardedModelAdmin


class TopicGroupInline(admin.TabularInline):
    model = TopicGroup
    filter_horizontal = ("members",)
    fields = ("name", "description", "members")
    extra = 0


class SubjectInline(admin.TabularInline):
    model = Subject
    extra = 1


class TopicGroupInline(admin.TabularInline):
    model = TopicGroup
    filter_horizontal = ("members",)
    fields = ("name", "description", "members")
    extra = 0


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    class Media:
        css = {
            "all": ("css/polls/admin/topic-admin.css",),
        }
        js = {
            "js/polls/admin/topic-admin.js": ("js/polls/admin/topic-admin.js",),
        }

    list_display = ("id", "topic_text", "pub_date")
    list_filter = ("pub_date",)
    inlines = [SubjectInline, TopicGroupInline]


@admin.register(TopicGroup)
class TopicGroupAdmin(admin.ModelAdmin):
    list_display = ("topic", "name", "description")
    filter_horizontal = ("owners", "members")
    fieldsets = (
        ("Basic Information", {"fields": ("topic", "name", "description", "owners", "members")}),
        (
            "Group Management",
            {
                "fields": (
                    "can_create_group",
                    "can_update_group",
                    "can_add_users_to_group",
                    "can_set_group_permissions",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Topic Management",
            {
                "fields": (
                    "can_rename_topic",
                    "can_delete_topic",
                    "can_update_topic_visible",
                    "can_update_topic_votable",
                    "can_update_topic_subject_rules",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Subject Management",
            {
                "fields": (
                    "can_create_subjects",
                    "can_suggest_subjects",
                    "can_delete_subjects",
                    "can_vote_on_subjects",
                ),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("id", "topic", "subject_text", "details", "pub_date", "current_score")
    list_filter = ("topic", "pub_date")


@admin.register(SubjectScore)
class SubjectScoreAdmin(admin.ModelAdmin):
    list_display = ("id", "subject", "score")
    list_filter = ("subject",)


@admin.register(SubjectLinks)
class SubjectLinksAdmin(admin.ModelAdmin):
    list_display = ("id", "subject", "link_text", "link_url", "pub_date")
    list_filter = ("subject", "pub_date")


class RankingInline(admin.TabularInline):
    model = Ranking
    extra = 1
    readonly_fields = ("order",)


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "topic", "date_voted", "date_updated")
    readonly_fields = ("date_updated",)
    list_filter = ("user", "topic", "submitted")
    inlines = [RankingInline]
