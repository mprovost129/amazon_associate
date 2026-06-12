class CampaignTrackingMiddleware:
    """Persist UTM/source data in the session so outbound clicks can be attributed."""

    UTM_KEYS = ('utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content')

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        campaign = request.session.get('campaign_attribution', {})
        changed = False

        for key in self.UTM_KEYS:
            value = request.GET.get(key, '').strip()
            if value:
                campaign[key] = value[:200]
                changed = True

        if changed:
            campaign['landing_page'] = request.get_full_path()[:500]
            request.session['campaign_attribution'] = campaign

        return self.get_response(request)
