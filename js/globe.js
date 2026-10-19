/**
 * Interactive 3D globe (globe.gl) for the About and Locations pages.
 * Any element with data-globe becomes a globe; an element with data-globe-panel gets the service legend and
 * the country chips. Hover (or focus, or tap) a country chip or a pin to see which services the network offers
 * there; pick a service to highlight every country that offers it.
 * globe.gl loads only when the element nears the viewport, and the animation pauses while it is off screen.
 */
(function () {
    'use strict';

    // The network's seven services, with a colour for each (decorative: every dot sits beside its text label)
    var SERVICES = {
        r: { n: 'Company registration and bank account opening', c: '#EA5C1F' },
        l: { n: 'Logistics', c: '#F5F5F5' },
        t: { n: 'Tax and legal consulting', c: '#3AA7C9' },
        a: { n: 'Accounting services', c: '#A3A9B5' },
        c: { n: 'Counterparty search and background checks', c: '#F29B9B' },
        i: { n: 'International trading', c: '#B58BE0' },
        b: { n: 'Business missions', c: '#9CC9F0' }
    };
    var ORDER = ['r', 'l', 't', 'a', 'c', 'i', 'b'];

    // Network locations and the services each one offers. Edit here to change the globe, the chips and the cards.
    var COUNTRIES = [
        { n: 'Philippines', lat: 14.56, lng: 121.02, s: 'rltc', hq: true },
        { n: 'Poland', lat: 52.23, lng: 21.01, s: 'rltc' }, { n: 'Hungary', lat: 47.5, lng: 19.04, s: 'rltc' },
        { n: 'Serbia', lat: 44.79, lng: 20.45, s: 'rltc' }, { n: 'Turkiye', lat: 41.01, lng: 28.98, s: 'rtacb' },
        { n: 'United Kingdom', lat: 51.51, lng: -0.13, s: 'rtc' }, { n: 'Japan', lat: 35.68, lng: 139.69, s: 'rltc' },
        { n: 'South Korea', lat: 37.57, lng: 126.98, s: 'rltc' }, { n: 'India', lat: 28.61, lng: 77.21, s: 'rltibc' },
        { n: 'China', lat: 31.23, lng: 121.47, s: 'rltacib' }, { n: 'Hong Kong', lat: 22.32, lng: 114.17, s: 'rltac' },
        { n: 'Taiwan', lat: 25.03, lng: 121.57, s: 'rltacib' }, { n: 'Vietnam', lat: 10.82, lng: 106.63, s: 'rtcbi' },
        { n: 'Singapore', lat: 1.28, lng: 103.85, s: 'rtc' }, { n: 'Indonesia', lat: -6.21, lng: 106.85, s: 'rtbic' },
        { n: 'Malaysia', lat: 3.14, lng: 101.69, s: 'rtc' }, { n: 'Thailand', lat: 13.76, lng: 100.5, s: 'rtc' },
        { n: 'Kuwait', lat: 29.38, lng: 47.98, s: 'rt' }, { n: 'United Arab Emirates', lat: 25.2, lng: 55.27, s: 'rltacib' },
        { n: 'Bahrain', lat: 26.23, lng: 50.59, s: 'rtic' }, { n: 'Saudi Arabia', lat: 24.71, lng: 46.68, s: 'rtbic' },
        { n: 'Qatar', lat: 25.29, lng: 51.53, s: 'rtc' }, { n: 'Oman', lat: 23.59, lng: 58.41, s: 'rtabic' },
        { n: 'Egypt', lat: 30.04, lng: 31.24, s: 'rltib' }, { n: 'Morocco', lat: 33.57, lng: -7.59, s: 'rltc' },
        { n: 'Nigeria', lat: 6.52, lng: 3.38, s: 'rltbc' }, { n: 'Ethiopia', lat: 9.03, lng: 38.74, s: 'rltc' },
        { n: 'Kenya', lat: -1.29, lng: 36.82, s: 'rltc' }, { n: 'South Africa', lat: -26.2, lng: 28.05, s: 'rltbc' },
        { n: 'United States', lat: 40.71, lng: -74.01, s: 'rltc' }, { n: 'Cayman Islands', lat: 19.31, lng: -81.25, s: 'rlt' },
        { n: 'British Virgin Islands', lat: 18.43, lng: -64.62, s: 'rltab' }, { n: 'Brazil', lat: -23.55, lng: -46.63, s: 'rltacib' },
        { n: 'Argentina', lat: -34.6, lng: -58.38, s: 'rltacib' }, { n: 'Chile', lat: -33.45, lng: -70.67, s: 'rltacib' },
        { n: 'Paraguay', lat: -25.26, lng: -57.58, s: 'rltacib' }, { n: 'Uruguay', lat: -34.9, lng: -56.16, s: 'rltacib' }
    ];
    window.MILLS_COUNTRIES = COUNTRIES;

    // The connections form a mesh between neighbouring locations, not a hub: each one links to its three nearest
    function dist(a, b) {
        var r = Math.PI / 180, dl = (b.lng - a.lng) * r, p1 = a.lat * r, p2 = b.lat * r;
        return Math.acos(Math.min(1, Math.sin(p1) * Math.sin(p2) + Math.cos(p1) * Math.cos(p2) * Math.cos(dl)));
    }
    var LINKS = (function () {
        var seen = {}, out = [];
        COUNTRIES.forEach(function (c, i) {
            COUNTRIES.map(function (o, k) { return { k: k, d: k === i ? 9 : dist(c, o) }; })
                .sort(function (x, y) { return x.d - y.d; }).slice(0, 3).forEach(function (n) {
                    var key = Math.min(i, n.k) + '-' + Math.max(i, n.k);
                    if (!seen[key]) { seen[key] = 1; out.push([i, n.k]); }
                });
        });
        return out;
    })();
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var libPromise = null;

    function loadLib() {
        if (window.Globe) return Promise.resolve();
        if (libPromise) return libPromise;
        libPromise = new Promise(function (resolve, reject) {
            var s = document.createElement('script');
            s.src = 'js/vendor/globe.gl.min.js';
            s.onload = resolve;
            s.onerror = reject;
            document.head.appendChild(s);
        });
        return libPromise;
    }

    function offers(c, code) { return c.s.indexOf(code) !== -1; }
    function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text) e.textContent = text; return e; }
    function dot(code, cls) { var i = el('i', cls || 'globe-dot'); i.style.background = SERVICES[code].c; return i; }

    // The service legend and country chips next to the globe
    function buildPanel(panel, api) {
        panel.innerHTML = '';
        // the service legend lives in its own glass card, so it reads differently from the location pills below it
        var card = el('div', 'globe-legend-card');
        card.appendChild(el('p', 'globe-legend-card__title', 'Services our network offers'));
        card.appendChild(el('p', 'globe-legend-card__hint', 'Pick a service to see which countries offer it.'));
        var legend = el('div', 'globe-legend'); legend.setAttribute('role', 'group'); legend.setAttribute('aria-label', 'Filter countries by service');
        var legendBtns = {};
        ORDER.forEach(function (code) {
            var b = el('button', 'globe-legend__btn'); b.type = 'button'; b.setAttribute('aria-pressed', 'false');
            b.appendChild(dot(code)); b.appendChild(el('span', 'globe-legend__label', SERVICES[code].n));
            b.addEventListener('click', function () { api.setFilter(api.state.filter === code ? null : code); });
            legend.appendChild(b); legendBtns[code] = b;
        });
        card.appendChild(legend);
        var chipsLabel = el('p', 'globe-chips__label', 'Where we work. Hover a country to see what the network offers there.');
        var chips = el('div', 'globe-chips'); var chipEls = {};
        COUNTRIES.forEach(function (c, idx) {
            var b = el('button', 'globe-chip'); b.type = 'button';
            b.appendChild(el('span', 'globe-chip__name', c.n));
            var dots = el('span', 'globe-chip__dots'); dots.setAttribute('aria-hidden', 'true');
            ORDER.forEach(function (code) { if (offers(c, code)) dots.appendChild(dot(code, 'globe-chip__dot')); });
            b.appendChild(dots);
            b.addEventListener('mouseenter', function () { api.hover(idx, true); });
            b.addEventListener('focus', function () { api.hover(idx, true); });
            b.addEventListener('mouseleave', function () { api.leave(); });
            b.addEventListener('blur', function () { api.leave(); });
            b.addEventListener('click', function () { api.pin(idx); });
            chips.appendChild(b); chipEls[idx] = b;
        });
        panel.appendChild(card); panel.appendChild(chipsLabel); panel.appendChild(chips);
        return { legendBtns: legendBtns, chipEls: chipEls };
    }

    function start(el0) {
        loadLib().then(function () {
            var state = { hover: -1, pinned: -1, filter: null };
            var panelEl = document.querySelector('[data-globe-panel]');
            var card = el('div', 'globe-card'); card.hidden = true; card.setAttribute('aria-live', 'polite');
            el0.appendChild(card);
            var ui = null, leaveTimer = null, resumeTimer = null;

            function visible(c) { return !state.filter || offers(c, state.filter); }
            var arcs = function () {
                return LINKS.filter(function (l) { return visible(COUNTRIES[l[0]]) && visible(COUNTRIES[l[1]]); }).map(function (l) {
                    var a = COUNTRIES[l[0]], b = COUNTRIES[l[1]];
                    return { startLat: a.lat, startLng: a.lng, endLat: b.lat, endLng: b.lng };
                });
            };

            var g = window.Globe()(el0)
                .globeImageUrl('assets/images/globe/earth-day.jpg')
                .bumpImageUrl('assets/images/globe/earth-topology.png')
                .backgroundColor('rgba(0,0,0,0)')
                .atmosphereColor('#8FB8F0')
                .atmosphereAltitude(0.06)
                .width(el0.clientWidth)
                .height(el0.clientWidth)
                .pointsData(COUNTRIES)
                .pointLat('lat').pointLng('lng')
                .pointRadius(function (d) { return 0.42; })
                .arcsData(arcs())
                .arcColor(function () { return ['rgba(234,92,31,0.95)', 'rgba(255,255,255,0.35)']; })
                .arcStroke(0.32)
                .arcDashLength(0.45)
                .arcDashGap(0.9)
                .arcDashAnimateTime(reduce ? 0 : 4200)
                .arcAltitudeAutoScale(0.4)
                .labelsData(COUNTRIES)
                .labelLat('lat').labelLng('lng').labelText('n')
                .labelIncludeDot(false)
                .labelResolution(2);

            function styles() {
                var sel = state.pinned > -1 ? state.pinned : state.hover;
                g.pointColor(function (d) { var i = COUNTRIES.indexOf(d); return i === sel ? '#EA5C1F' : (!visible(d) ? 'rgba(255,255,255,0.25)' : '#FFFFFF'); })
                 .pointAltitude(function (d) { var i = COUNTRIES.indexOf(d); return i === sel ? 0.12 : 0.04; })
                 .labelSize(function (d) { var i = COUNTRIES.indexOf(d); return i === sel ? 1.5 : 0.95; })
                 .labelAltitude(function (d) { var i = COUNTRIES.indexOf(d); return i === sel ? 0.16 : 0.08; })
                 .labelColor(function (d) { var i = COUNTRIES.indexOf(d); return i === sel ? '#FFB48A' : (!visible(d) ? 'rgba(255,255,255,0.28)' : '#FFFFFF'); })
                 .arcsData(arcs());
                if (ui) {
                    COUNTRIES.forEach(function (c, i) {
                        var b = ui.chipEls[i];
                        b.classList.toggle('is-dim', !visible(c));
                        b.classList.toggle('is-active', i === sel);
                        b.setAttribute('aria-pressed', String(i === state.pinned));
                    });
                    ORDER.forEach(function (code) { ui.legendBtns[code].setAttribute('aria-pressed', String(state.filter === code)); });
                }
            }

            function showCard(i) {
                if (i < 0) { card.hidden = true; return; }
                var c = COUNTRIES[i];
                card.innerHTML = '';
                card.appendChild(el('h3', 'globe-card__title', c.n));
                card.appendChild(el('p', 'globe-card__sub', 'Partner network'));
                var ul = el('ul', 'globe-card__list');
                ORDER.forEach(function (code) {
                    if (!offers(c, code)) return;
                    var li = el('li'); li.appendChild(dot(code)); li.appendChild(document.createTextNode(SERVICES[code].n)); ul.appendChild(li);
                });
                card.appendChild(ul); card.hidden = false;
            }

            var controls = g.controls();
            controls.autoRotate = !reduce;
            controls.autoRotateSpeed = 0.55;
            controls.enableZoom = false;
            controls.enablePan = false;

            function focusOn(i) {
                var c = COUNTRIES[i];
                controls.autoRotate = false;
                g.pointOfView({ lat: c.lat, lng: c.lng, altitude: 1.6 }, reduce ? 0 : 900);
            }
            function resume() { clearTimeout(resumeTimer); resumeTimer = setTimeout(function () { if (state.pinned < 0 && state.hover < 0) controls.autoRotate = !reduce; }, 2500); }

            var api = {
                state: state,
                hover: function (i, rotate) {
                    clearTimeout(leaveTimer); clearTimeout(resumeTimer);
                    state.hover = i; if (rotate) focusOn(i);
                    styles(); showCard(state.pinned > -1 ? state.pinned : i);
                },
                leave: function () {
                    clearTimeout(leaveTimer);
                    leaveTimer = setTimeout(function () { state.hover = -1; styles(); showCard(state.pinned); if (state.pinned < 0) resume(); }, 160);
                },
                pin: function (i) {
                    state.pinned = state.pinned === i ? -1 : i;
                    if (state.pinned > -1) focusOn(i); else resume();
                    styles(); showCard(state.pinned > -1 ? state.pinned : state.hover);
                },
                setFilter: function (code) { state.filter = code; styles(); }
            };

            var hoverFn = function (d) { if (d) api.hover(COUNTRIES.indexOf(d), false); else api.leave(); };
            var clickFn = function (d) { if (d) api.pin(COUNTRIES.indexOf(d)); };
            g.onPointHover(hoverFn).onLabelHover(hoverFn).onPointClick(clickFn).onLabelClick(clickFn);

            if (panelEl) ui = buildPanel(panelEl, api);
            styles();
            g.renderer().setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.5));
            g.pointOfView({ lat: 14, lng: 121, altitude: 1.5 });

            if (window.ResizeObserver) {
                new ResizeObserver(function () { g.width(el0.clientWidth).height(el0.clientWidth); }).observe(el0);
            }
            if (window.IntersectionObserver) {
                new IntersectionObserver(function (entries) {
                    entries.forEach(function (en) { if (en.isIntersecting) g.resumeAnimation(); else g.pauseAnimation(); });
                }).observe(el0);
            }
            el0.__globe = g;
            el0.classList.add('is-ready');
        }).catch(function () { el0.classList.add('is-failed'); });
    }

    function init() {
        var els = document.querySelectorAll('[data-globe]');
        if (!els.length) return;
        els.forEach(function (e) {
            if (!('IntersectionObserver' in window)) { start(e); return; }
            var io = new IntersectionObserver(function (entries) {
                if (entries.some(function (x) { return x.isIntersecting; })) { io.disconnect(); start(e); }
            }, { rootMargin: '300px 0px' });
            io.observe(e);
        });
    }

    // count-up for the network stats
    function countUp() {
        var nums = document.querySelectorAll('[data-count]');
        if (!nums.length) return;
        function run(node) {
            var end = parseInt(node.getAttribute('data-count'), 10), suffix = node.getAttribute('data-suffix') || '', t0 = null, dur = 1800;
            if (reduce) { node.textContent = end + suffix; return; }
            function step(t) {
                if (t0 === null) t0 = t;
                var p = Math.min((t - t0) / dur, 1), e = 1 - Math.pow(1 - p, 3);
                node.textContent = Math.round(end * e) + suffix;
                if (p < 1) window.requestAnimationFrame(step);
            }
            window.requestAnimationFrame(step);
        }
        if (!('IntersectionObserver' in window)) return;
        nums.forEach(function (n) { n.textContent = '0' + (n.getAttribute('data-suffix') || ''); });
        var io = new IntersectionObserver(function (entries) {
            entries.forEach(function (en) { if (en.isIntersecting) { io.unobserve(en.target); run(en.target); } });
        }, { threshold: 0.6 });
        nums.forEach(function (n) { io.observe(n); });
    }

    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { init(); countUp(); });
    else { init(); countUp(); }
})();
