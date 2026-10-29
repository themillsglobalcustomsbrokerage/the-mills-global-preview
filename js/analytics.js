/**
 * Tracking for The Mills Global.
 *
 * Third-party tags (Google Tag Manager, Google Ads, LinkedIn Insight,
 * ContentSquare) load ONLY on themillsglobal.com, so the GitHub and Vercel
 * preview addresses never send data to the real accounts.
 *
 * window.mtgTrack(name, params) pushes a custom event to the dataLayer.
 * Google Tag Manager picks these up with Custom Event triggers and forwards
 * them to GA4. Add ?ga_debug=1 to any URL to log events in the console.
 *
 * Also captures ad attribution (gclid, utm_*) for the lead magnet form.
 */
(function () {
    'use strict';

    var GTM_ID = 'GTM-K3QFNL94';
    var ADS_ID = 'AW-17000148570';
    var LINKEDIN_PARTNER_ID = '9889316';

    // One conversion action per outcome, so each source is reported separately.
    // Google Ads: 'AW-ACCOUNT/LABEL' from Goals > Conversions > the action's tag setup.
    // Leave a value empty until that conversion action exists; empty ones are skipped.
    var ADS_CONVERSIONS = {
        phone: 'AW-17000148570/gISqCI-RpqscENrcpqo_', // "Phone Click - Contact Us": Call Now / any tel: link click
        email: '',                                     // Email Us / any mailto: link click
        book_click: '',                                // Book a Consultation / Book a Call click
        book_scheduled: '',                            // a meeting was actually booked in Cal.com
        form: ''                                       // contact form or lead magnet submitted
    };
    // LinkedIn: numeric conversion rule IDs from Campaign Manager > Conversions.
    var LINKEDIN_CONVERSIONS = {
        phone: 0,
        email: 0,
        book_click: 28098724,
        book_scheduled: 0,
        form: 0
    };
    var CONTENTSQUARE_SRC = 'https://t.contentsquare.net/uxa/fde570633e6be.js';

    var host = window.location.hostname;
    var isProduction = /(^|\.)themillsglobal\.com$/.test(host);
    var debug = /[?&]ga_debug=1\b/.test(window.location.search) || !isProduction;

    window.dataLayer = window.dataLayer || [];
    if (!window.gtag) {
        window.gtag = function () { window.dataLayer.push(arguments); };
    }

    function loadScript(src) {
        var s = document.createElement('script');
        s.async = true;
        s.src = src;
        document.head.appendChild(s);
    }

    if (isProduction) {
        // Google Tag Manager
        window.dataLayer.push({ 'gtm.start': new Date().getTime(), event: 'gtm.js' });
        loadScript('https://www.googletagmanager.com/gtm.js?id=' + GTM_ID);

        // Google Ads (conversion on phone clicks)
        loadScript('https://www.googletagmanager.com/gtag/js?id=' + ADS_ID);
        window.gtag('js', new Date());
        window.gtag('config', ADS_ID);

        // LinkedIn Insight Tag
        window._linkedin_data_partner_ids = window._linkedin_data_partner_ids || [];
        window._linkedin_data_partner_ids.push(LINKEDIN_PARTNER_ID);
        if (!window.lintrk) {
            window.lintrk = function (a, b) { window.lintrk.q.push([a, b]); };
            window.lintrk.q = [];
        }
        loadScript('https://snap.licdn.com/li.lms-analytics/insight.min.js');

        // ContentSquare
        loadScript(CONTENTSQUARE_SRC);
    }

    function pageType() {
        var f = (window.location.pathname.split('/').pop() || 'index').replace(/\.html$/, '');
        if (f === '' || f === 'index') return 'home';
        if (f.indexOf('services-mills-') === 0) return 'service';
        if (f === 'industries') return 'industries_hub';
        if (f.indexOf('industries-') === 0) return 'industry';
        if (f.indexOf('legal-') === 0) return 'legal';
        if (f.indexOf('blog') === 0) return 'blog';
        return f.replace(/-/g, '_');
    }

    window.mtgTrack = function (name, params) {
        params = params || {};
        params.page_path = window.location.pathname;
        params.page_type = pageType();
        if (debug) console.debug('[event]', name, params);
        try {
            window.dataLayer.push(Object.assign({ event: name }, params));
        } catch (e) { /* never let tracking break the page */ }
    };

    // Ad attribution: remember gclid and utm_* from the landing URL for this visit
    var ATTR_KEYS = ['gclid', 'gbraid', 'wbraid', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'];
    var ATTR_STORE = 'mtgAttribution';
    try {
        var found = {};
        var q = new URLSearchParams(window.location.search);
        ATTR_KEYS.forEach(function (k) { if (q.get(k)) found[k] = q.get(k); });
        if (Object.keys(found).length) window.sessionStorage.setItem(ATTR_STORE, JSON.stringify(found));
    } catch (e) { /* storage blocked */ }
    window.mtgAttribution = function () {
        try { return JSON.parse(window.sessionStorage.getItem(ATTR_STORE) || '{}'); } catch (e) { return {}; }
    };

    // Fires the Google Ads and LinkedIn conversions for one outcome (production only).
    window.mtgConversion = function (action) {
        if (!isProduction) return;
        if (ADS_CONVERSIONS[action]) {
            window.gtag('event', 'conversion', { send_to: ADS_CONVERSIONS[action], value: 1.0, currency: 'PHP' });
        }
        if (LINKEDIN_CONVERSIONS[action] && window.lintrk) {
            window.lintrk('track', { conversion_id: LINKEDIN_CONVERSIONS[action] });
        }
    };

    // Where on the page a click happened: an explicit data-ga-label wins,
    // otherwise the nearest known region of the layout.
    function ctaLocation(el) {
        var tagged = el.closest('[data-ga-label]');
        if (tagged) return tagged.getAttribute('data-ga-label');
        if (el.closest('.nav')) return 'nav';
        if (el.closest('.footer')) return 'footer';
        if (el.closest('.book-call')) return 'book_call_section';
        if (el.closest('.lm-strip, .lm-popup')) return 'lead_magnet';
        if (el.closest('.contact-split__grid, #contact')) return 'contact_section';
        return 'other';
    }

    // One canonical GA4 event per kind of click, with the location as a parameter:
    //   call_click, email_click, book_consult_click
    document.addEventListener('click', function (e) {
        var el = e.target.closest ? e.target.closest('a, button') : null;
        if (!el) return;
        var href = el.getAttribute('href') || '';
        var text = (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 60);
        var details = { cta_location: ctaLocation(el), link_text: text };

        if (href.indexOf('tel:') === 0) {
            window.mtgTrack('call_click', details);
            window.mtgConversion('phone'); // never blocks the call
        } else if (href.indexOf('mailto:') === 0) {
            window.mtgTrack('email_click', details);
            window.mtgConversion('email');
        } else if (href === '#book-call' || href.indexOf('book-a-call') !== -1) {
            window.mtgTrack('book_consult_click', details);
            window.mtgConversion('book_click');
        } else {
            // any other element can opt in with data-ga="event_name"
            var tag = el.closest('[data-ga]');
            if (tag) window.mtgTrack(tag.getAttribute('data-ga'), details);
        }
    });
})();
