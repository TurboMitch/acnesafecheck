#!/usr/bin/env python3
"""Single source of truth for the site's "last updated" date.

Bump CONTENT_UPDATED only when the ratings data or page content meaningfully
changes. Generators import this instead of stamping datetime.date.today(), so
a plain rebuild/redeploy no longer mass-bumps dateModified on 560+ unchanged
pages (a freshness-inflation / credibility problem for a YMYL site).
"""
import datetime

CONTENT_UPDATED = "2026-09-10"  # rating-first titles, list-page phrase, fungal-acne guide expansion

CONTENT_UPDATED_HUMAN = datetime.date.fromisoformat(CONTENT_UPDATED).strftime("%B %Y")
