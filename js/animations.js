/**
 * IntersectionObserver-based reveal animations and stat counters.
 * Self-initializes on DOMContentLoaded.
 */
document.addEventListener('DOMContentLoaded', () => {
    // 1. Scroll Reveal
    const revealElements = document.querySelectorAll('.animate-in');
    if (revealElements.length > 0) {
        const revealObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.15,
            rootMargin: '0px 0px -40px 0px'
        });

        revealElements.forEach(el => revealObserver.observe(el));
    }

    // 2. Stat Counter Animation
    const statElements = document.querySelectorAll('.stat-number[data-target]');
    if (statElements.length > 0) {
        const easeOutQuart = t => 1 - Math.pow(1 - t, 4);
        const DURATION = 2000;

        const statObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const el = entry.target;
                    const targetStr = el.getAttribute('data-target');
                    const target = parseFloat(targetStr);
                    if (isNaN(target)) return;

                    const suffix = el.getAttribute('data-suffix') || '';
                    const prefix = el.getAttribute('data-prefix') || '';
                    const isInt = target % 1 === 0;

                    let startTimestamp = null;
                    const step = (timestamp) => {
                        if (!startTimestamp) startTimestamp = timestamp;
                        const elapsed = timestamp - startTimestamp;
                        let progress = Math.min(elapsed / DURATION, 1);
                        
                        const easedProgress = easeOutQuart(progress);
                        const currentVal = easedProgress * target;
                        
                        let displayVal = isInt ? Math.round(currentVal).toString() : currentVal.toFixed(1);
                        
                        el.textContent = `${prefix}${displayVal}${suffix}`;
                        
                        if (progress < 1) {
                            requestAnimationFrame(step);
                        } else {
                            // Ensure final value is exact
                            el.textContent = `${prefix}${isInt ? target : target.toFixed(1)}${suffix}`;
                        }
                    };
                    
                    requestAnimationFrame(step);
                    observer.unobserve(el);
                }
            });
        }, {
            threshold: 0.5
        });

        statElements.forEach(el => {
            // the HTML holds the real figure (for crawlers and no-JS); count up from zero when it scrolls into view
            el.textContent = `${el.getAttribute('data-prefix') || ''}0${el.getAttribute('data-suffix') || ''}`;
            statObserver.observe(el);
        });
    }

    // 3. Services Slider - arrow nav + tap-to-reveal on touch devices
    // (CSS :hover/:focus-within already handles mouse + keyboard).
    const slider = document.getElementById('services-slider');
    if (slider) {
        const arrows = document.querySelectorAll('.services-slider__arrow');
        arrows.forEach(arrow => {
            arrow.addEventListener('click', () => {
                const dir = parseFloat(arrow.getAttribute('data-dir')) || 1;
                const card = slider.querySelector('.service-slide');
                const step = card ? card.getBoundingClientRect().width + 24 : 300;
                slider.scrollBy({ left: dir * step, behavior: 'smooth' });
            });
        });

        const isTouch = !(window.matchMedia && window.matchMedia('(hover: hover)').matches);
        if (isTouch) {
            const slides = slider.querySelectorAll('.service-slide');
            slides.forEach(slide => {
                slide.addEventListener('click', () => {
                    const wasOpen = slide.classList.contains('is-open');
                    slides.forEach(s => s.classList.remove('is-open'));
                    if (!wasOpen) slide.classList.add('is-open');
                });
                const link = slide.querySelector('.service-slide__link');
                if (link) link.addEventListener('click', (e) => e.stopPropagation());
            });
        }
    }

    // 4. Contact Form - composes a pre-filled mailto (static site, no backend)
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const data = new FormData(contactForm);
            const name = (data.get('name') || '').toString().trim();
            const company = (data.get('company') || '').toString().trim();
            const email = (data.get('email') || '').toString().trim();
            const message = (data.get('message') || '').toString().trim();
            const service = contactForm.getAttribute('data-service');
            const attr = window.mtgAttribution ? window.mtgAttribution() : {};
            const adSource = Object.keys(attr).map((k) => `${k}=${attr[k]}`).join('; ');

            const subjectLead = service ? `${service} inquiry` : 'Quote request';
            const subject = `${subjectLead} from ${name}${company ? ', ' + company : ''}`;
            const bodyLines = [
                message || '(No details provided)',
                '',
                service ? `Service: ${service}` : null,
                `Name: ${name}`,
                company ? `Company: ${company}` : null,
                `Reply-to email: ${email}`,
                adSource ? `Ad source: ${adSource}` : null
            ].filter(Boolean);

            const mailtoUrl = `mailto:inquiry@themillsglobal.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(bodyLines.join('\n'))}`;
            if (window.mtgTrack) window.mtgTrack('generate_lead', { lead_source: 'contact_form', service: service || 'general' });
            if (window.mtgConversion) window.mtgConversion('form');
            window.location.href = mailtoUrl;
        });
    }

    // 5. FAQ Accordion - each item toggles independently (not exclusive)
    const faqQuestions = document.querySelectorAll('.faq-question');
    faqQuestions.forEach(btn => {
        btn.addEventListener('click', () => {
            const item = btn.closest('.faq-item');
            if (item) item.classList.toggle('is-open');
            btn.setAttribute('aria-expanded', item && item.classList.contains('is-open') ? 'true' : 'false');
        });
    });

    // 6. Mobile Nav Toggle
    const navEl = document.getElementById('nav');
    const mobileToggle = document.querySelector('.nav__mobile-toggle');
    if (navEl && mobileToggle) {
        mobileToggle.addEventListener('click', () => {
            const isOpen = navEl.classList.toggle('mobile-open');
            mobileToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
            document.body.style.overflow = isOpen ? 'hidden' : '';
        });
        navEl.querySelectorAll('.nav__mobile-panel a').forEach((link) => {
            link.addEventListener('click', () => {
                navEl.classList.remove('mobile-open');
                mobileToggle.setAttribute('aria-expanded', 'false');
                document.body.style.overflow = '';
            });
        });
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && navEl.classList.contains('mobile-open')) {
                navEl.classList.remove('mobile-open');
                mobileToggle.setAttribute('aria-expanded', 'false');
                document.body.style.overflow = '';
            }
        });
    }

    // 7. Service Pill Hover Preview - small card that follows the cursor
    // near the hovered "Connected Services" pill on industry pages.
    const previewPills = document.querySelectorAll('.industry-pill[data-preview-desc]');
    if (previewPills.length > 0 && window.matchMedia('(hover: hover)').matches) {
        const preview = document.createElement('div');
        preview.className = 'pill-preview';
        preview.innerHTML = `
            <img class="pill-preview__img" alt="">
            <div class="pill-preview__body">
                <p class="pill-preview__title"></p>
                <p class="pill-preview__desc"></p>
            </div>
        `;
        document.body.appendChild(preview);
        const previewImg = preview.querySelector('.pill-preview__img');
        const previewTitle = preview.querySelector('.pill-preview__title');
        const previewDesc = preview.querySelector('.pill-preview__desc');

        const positionPreview = (e) => {
            const margin = 16;
            const rect = preview.getBoundingClientRect();
            let x = e.clientX + margin;
            let y = e.clientY + margin;
            if (x + rect.width > window.innerWidth - 12) x = e.clientX - rect.width - margin;
            if (y + rect.height > window.innerHeight - 12) y = e.clientY - rect.height - margin;
            preview.style.left = `${Math.max(12, x)}px`;
            preview.style.top = `${Math.max(12, y)}px`;
        };

        previewPills.forEach((pill) => {
            pill.addEventListener('mouseenter', (e) => {
                previewImg.src = pill.getAttribute('data-preview-img') || '';
                previewTitle.textContent = pill.getAttribute('data-preview-title') || '';
                previewDesc.textContent = pill.getAttribute('data-preview-desc') || '';
                positionPreview(e);
                preview.classList.add('is-visible');
            });
            pill.addEventListener('mousemove', positionPreview);
            pill.addEventListener('mouseleave', () => {
                preview.classList.remove('is-visible');
            });
        });
    }

    // 8. Process Timeline - scroll-fill line + lighting up numbered circles
    const timelines = document.querySelectorAll('.process-timeline');
    if (timelines.length > 0) {
        const triggerRatio = 0.65; // fraction down the viewport that "activates" a step
        let rafId = null;
        const updateTimelines = () => {
            const triggerY = window.innerHeight * triggerRatio;
            timelines.forEach((timeline) => {
                const track = timeline.querySelector('.process-timeline__track');
                const fill = timeline.querySelector('.process-timeline__track-fill');
                const circles = timeline.querySelectorAll('.process-timeline__circle');
                if (!track || !fill) return;
                const trackRect = track.getBoundingClientRect();
                const filledPx = Math.max(0, Math.min(trackRect.height, triggerY - trackRect.top));
                fill.style.height = `${filledPx}px`;
                circles.forEach((circle) => {
                    const circleRect = circle.getBoundingClientRect();
                    const circleCenterY = circleRect.top + circleRect.height / 2;
                    circle.classList.toggle('is-filled', circleCenterY <= triggerY);
                });
            });
            rafId = null;
        };
        const onScroll = () => {
            if (rafId === null) rafId = requestAnimationFrame(updateTimelines);
        };
        window.addEventListener('scroll', onScroll, { passive: true });
        window.addEventListener('resize', onScroll);
        updateTimelines();
    }

    // 9. "Who This Is For" hover backdrop - crossfades the section's
    // background image to match the hovered list item.
    const audienceHero = document.querySelector('.audience-hero');
    if (audienceHero) {
        const bgLayers = audienceHero.querySelectorAll('.audience-hero__bg');
        const items = audienceHero.querySelectorAll('.audience-list__item[data-bg]');
        let activeIndex = 0;
        const setBg = (url) => {
            if (!url || bgLayers.length < 2) return;
            const nextLayer = bgLayers[1 - activeIndex];
            const currentLayer = bgLayers[activeIndex];
            nextLayer.style.backgroundImage = `url('${url}')`;
            nextLayer.classList.add('is-active');
            currentLayer.classList.remove('is-active');
            activeIndex = 1 - activeIndex;
        };
        if (items.length > 0 && bgLayers.length >= 2) {
            const firstBg = items[0].getAttribute('data-bg');
            if (firstBg) {
                bgLayers[0].style.backgroundImage = `url('${firstBg}')`;
                bgLayers[0].classList.add('is-active');
            }
            items.forEach((item) => {
                item.addEventListener('mouseenter', () => setBg(item.getAttribute('data-bg')));
            });
        }
    }

    // 10. Smooth Scroll for Nav Links
    const navLinks = document.querySelectorAll('.nav__links a[href^="#"]');
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const targetId = link.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                e.preventDefault();
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

/**
 * Image placeholders: if a file exists at a slot's data-img path, swap it in.
 */
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.img-slot[data-img]').forEach(slot => {
        const src = slot.dataset.img;
        const probe = new Image();
        probe.onload = () => {
            slot.style.backgroundImage = `url("${src}")`;
            slot.classList.add('has-image');
            // floating stickers: the box takes the picture's own proportions
            if (slot.classList.contains('img-float')) {
                slot.style.aspectRatio = String(probe.naturalWidth / probe.naturalHeight);
            }
            // cutouts: size the box to the picture so it sits flush at the bottom
            if (slot.classList.contains('img-slot--cutout')) {
                const ratio = probe.naturalWidth / probe.naturalHeight;
                slot.style.aspectRatio = String(ratio);
                if (ratio < 1.15) slot.classList.add('img-slot--cutout-tall');
            }
        };
        probe.src = src;
    });
});

/**
 * Marquee logos: swap the placeholder tile for the real logo when the file exists.
 */
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.marquee__logo[data-img]').forEach(tile => {
        const probe = new Image();
        probe.onload = () => {
            const img = document.createElement('img');
            img.src = tile.dataset.img;
            img.alt = '';
            tile.textContent = '';
            tile.appendChild(img);
            tile.classList.add('has-image');
        };
        probe.src = tile.dataset.img;
    });
});

/**
 * Core Support pointer: a small container icon that travels through the
 * numbered items strictly in order (1, 2, 3 ...) as the user scrolls.
 * Waypoints sit at the top-right of each item; the path through them is a
 * Catmull-Rom spline, so it swoops in soft curves instead of straight lines.
 * Position is a pure function of scroll, then eased for an organic feel.
 */
document.addEventListener('DOMContentLoaded', () => {
    const grids = document.querySelectorAll('.service-feature-grid');
    const icon = '<svg viewBox="0 0 48 32" width="44" height="30" fill="none" aria-hidden="true">' +
        '<rect x="1" y="3" width="46" height="24" rx="3" fill="#EA5C1F"/>' +
        '<g stroke="#212431" stroke-opacity="0.4" stroke-width="2" stroke-linecap="round">' +
        '<line x1="9" y1="7" x2="9" y2="23"/><line x1="16" y1="7" x2="16" y2="23"/>' +
        '<line x1="23" y1="7" x2="23" y2="23"/><line x1="30" y1="7" x2="30" y2="23"/>' +
        '<line x1="37" y1="7" x2="37" y2="23"/></g>' +
        '<rect x="1" y="3" width="46" height="24" rx="3" stroke="#212431" stroke-opacity="0.55" stroke-width="1.5"/>' +
        '<rect x="3" y="27" width="6" height="3" rx="1" fill="#212431"/><rect x="39" y="27" width="6" height="3" rx="1" fill="#212431"/></svg>';
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const smooth = (f) => f * f * (3 - 2 * f);

    grids.forEach(grid => {
        const items = Array.from(grid.querySelectorAll('.service-feature'));
        if (!items.length) return;
        const pointer = document.createElement('div');
        pointer.className = 'feature-pointer';
        pointer.setAttribute('aria-hidden', 'true');
        pointer.innerHTML = '<div class="feature-pointer__bob">' + icon + '</div>';
        grid.appendChild(pointer);

        let pts = [];
        let keys = [];
        let single = true;
        let cur = null;
        let rot = 0;
        let rafId = null;

        const measure = () => {
            const n = items.length;
            const baseLeft = items[0].offsetLeft;
            single = items.every(it => Math.abs(it.offsetLeft - baseLeft) < 4);
            pts = items.map(it => ({
                x: it.offsetLeft + it.offsetWidth - Math.max(120, it.offsetWidth * 0.24) - 22,
                y: it.offsetTop + 10
            }));
            keys = items.map((it, i) => {
                const col = single ? 0 : (it.offsetLeft > baseLeft + 4 ? 1 : 0);
                return it.offsetTop + col * it.offsetHeight * 0.5;
            });
            for (let i = 1; i < n; i++) keys[i] = Math.max(keys[i], keys[i - 1] + 1);
        };

        const tAt = (u) => {
            const n = keys.length;
            if (n === 1 || u <= keys[0]) return { t: 0, j: 0, f: 0 };
            if (u >= keys[n - 1]) return { t: n - 1, j: n - 2, f: 1 };
            let j = 0;
            while (j < n - 2 && u >= keys[j + 1]) j++;
            const f = (u - keys[j]) / (keys[j + 1] - keys[j]);
            return { t: j + smooth(f), j, f };
        };

        const spline = (t) => {
            const n = pts.length;
            if (n === 1) return { x: pts[0].x, y: pts[0].y };
            const P = (i) => pts[Math.max(0, Math.min(n - 1, i))];
            const i = Math.min(Math.floor(t), n - 2);
            const f = t - i;
            const p0 = P(i - 1), p1 = P(i), p2 = P(i + 1), p3 = P(i + 2);
            const c = (a, b, cc, d) => 0.5 * (2 * b + (-a + cc) * f +
                (2 * a - 5 * b + 4 * cc - d) * f * f + (-a + 3 * b - 3 * cc + d) * f * f * f);
            return { x: c(p0.x, p1.x, p2.x, p3.x), y: c(p0.y, p1.y, p2.y, p3.y) };
        };

        const frame = () => {
            rafId = null;
            const g = grid.getBoundingClientRect();
            const vh = window.innerHeight;
            const visible = g.bottom > 0 && g.top < vh;
            pointer.classList.toggle('is-visible', visible);
            const u = vh * 0.55 - g.top;
            const seg = tAt(u);
            const pos = spline(seg.t);
            // soft S-bend between waypoints so the road feels organic
            const amp = single ? 14 : 5;
            pos.x += amp * Math.sin(seg.f * Math.PI) * (seg.j % 2 ? 1 : -1);
            if (!cur || reduce) cur = { x: pos.x, y: pos.y };
            const dx = pos.x - cur.x;
            const dy = pos.y - cur.y;
            cur.x += dx * 0.14;
            cur.y += dy * 0.14;
            const targetRot = Math.max(-12, Math.min(12, dx * 0.5));
            rot += (targetRot - rot) * 0.15;
            pointer.style.transform = `translate3d(${cur.x}px, ${cur.y}px, 0) rotate(${rot}deg)`;
            const active = Math.round(seg.t);
            items.forEach((it, i) => it.classList.toggle('is-active', i === active));
            if (visible && (Math.abs(dx) > 0.3 || Math.abs(dy) > 0.3 || Math.abs(rot) > 0.3)) {
                rafId = requestAnimationFrame(frame);
            }
        };
        const kick = () => { if (rafId === null) rafId = requestAnimationFrame(frame); };
        const remeasure = () => { measure(); kick(); };

        measure();
        window.addEventListener('scroll', kick, { passive: true });
        window.addEventListener('resize', remeasure);
        window.addEventListener('load', remeasure);
        if (window.ResizeObserver) new ResizeObserver(remeasure).observe(grid);
        setTimeout(remeasure, 700);
        setTimeout(remeasure, 1400);
        frame();
    });
});

/* Navbar dropdowns: hovering one tab hands over instantly, so the previous panel never lingers
   (including one held open by keyboard focus from an earlier click). */
(function () {
    var items = document.querySelectorAll('.nav__item--dropdown');
    if (!items.length) return;
    items.forEach(function (item) {
        item.addEventListener('mouseenter', function () {
            items.forEach(function (other) {
                if (other === item) { other.classList.remove('is-suppressed'); return; }
                other.classList.add('is-suppressed');
                if (other.contains(document.activeElement)) document.activeElement.blur();
            });
        });
    });
    var list = items[0].parentElement;
    list.addEventListener('mouseleave', function () {
        items.forEach(function (i) { i.classList.remove('is-suppressed'); });
    });
})();

/* Logo lockup: "TRADE WITHOUT LIMITS" sits under every Mills logo, fitted to the logo's width
   (nav, footer and anywhere else the logo image is used). */
(function () {
    var TEXT = 'TRADE WITHOUT LIMITS';
    var tags = [];
    function fit(t) {
        var img = t.img, w = img.getBoundingClientRect().width;
        if (!w) return;
        t.el.style.fontSize = (w * 0.07).toFixed(2) + 'px';
        t.el.style.letterSpacing = '0px';
        t.el.style.marginRight = '0px';
        var natural = t.el.getBoundingClientRect().width;
        var ls = (w - natural) / (TEXT.length - 1);
        t.el.style.letterSpacing = ls.toFixed(3) + 'px';
        t.el.style.marginRight = (-ls).toFixed(3) + 'px';
        t.el.style.marginTop = (w * 0.045).toFixed(2) + 'px';
    }
    function fitAll() { tags.forEach(fit); }
    document.querySelectorAll('img[src*="mills-logo"]').forEach(function (img) {
        var host = img.closest('a') || img.parentElement;
        if (!host || host.querySelector('.logo-tagline')) return;
        host.classList.add('logo-lockup');
        var el = document.createElement('span');
        el.className = 'logo-tagline';
        el.setAttribute('aria-hidden', 'true');
        el.textContent = TEXT;
        host.appendChild(el);
        var t = { img: img, el: el };
        tags.push(t);
        if (window.ResizeObserver) new ResizeObserver(function () { fit(t); }).observe(img);
    });
    if (!tags.length) return;
    fitAll();
    window.addEventListener('resize', fitAll);
    window.addEventListener('load', fitAll);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(fitAll);
})();
