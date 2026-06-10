/**
 * Read Later landing-page motion. No framework. ~2kb gzipped.
 *
 * Handles:
 *  - .reveal                    fade + lift when entering viewport
 *  - .reveal-lines              Dropset-style mask + slide-up per line
 *  - .reveal-eyebrow            small uppercase text fade-in
 *  - .reveal-image              blur + scale-in for hero imagery
 *  - [data-counter]             animated number count-up (e.g. 0 -> 50)
 *  - [data-scrolly]             pinned-device scrollytelling with sticky labels
 *  - [data-pinned-statement]    sticky-pinned anchor moment with staged reveal
 *  - [data-hero-icon]           cursor-driven fan out for the stacked-card icon
 *
 * Respects prefers-reduced-motion.
 */

function easeOutExpo(t: number): number {
  return t === 1 ? 1 : 1 - Math.pow(2, -10 * t);
}

function runCounter(el: HTMLElement) {
  const target = Number(el.dataset.counter ?? el.dataset.target ?? '0');
  const duration = Number(el.dataset.duration ?? '1400');
  const suffix = el.dataset.suffix ?? '';
  const start = performance.now();
  const initial = 0;

  function frame(now: number) {
    const elapsed = now - start;
    const progress = Math.min(elapsed / duration, 1);
    const eased = easeOutExpo(progress);
    const value = Math.round(initial + (target - initial) * eased);
    el.textContent = `${value}${suffix}`;
    if (progress < 1) requestAnimationFrame(frame);
  }

  requestAnimationFrame(frame);
}

function init() {
  document.documentElement.classList.add('js-ready');

  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const animatedSelectors = [
    '.reveal',
    '.reveal-lines',
    '.reveal-eyebrow',
    '.reveal-image',
    '.reveal-line-draw',
  ];

  const animated = document.querySelectorAll<HTMLElement>(animatedSelectors.join(','));

  if (reduced) {
    animated.forEach((el) => el.classList.add('is-visible'));
    document.querySelectorAll<HTMLElement>('[data-counter]').forEach((el) => {
      const target = el.dataset.counter ?? el.dataset.target ?? '0';
      const suffix = el.dataset.suffix ?? '';
      el.textContent = `${target}${suffix}`;
    });
  } else if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            io.unobserve(entry.target);
          }
        }
      },
      { threshold: 0.05, rootMargin: '0px 0px -4% 0px' },
    );
    animated.forEach((el) => io.observe(el));

    // Fallback: any element still hidden after 1.5s gets revealed.
    // Guards against IntersectionObserver edge cases in some renderers.
    window.setTimeout(() => {
      animated.forEach((el) => {
        if (!el.classList.contains('is-visible')) {
          el.classList.add('is-visible');
        }
      });
    }, 1500);

    const counterIO = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            runCounter(entry.target as HTMLElement);
            counterIO.unobserve(entry.target);
          }
        }
      },
      { threshold: 0.6 },
    );
    document
      .querySelectorAll<HTMLElement>('[data-counter]')
      .forEach((el) => counterIO.observe(el));
  } else {
    animated.forEach((el) => el.classList.add('is-visible'));
  }

  const scrolly = document.querySelector<HTMLElement>('[data-scrolly]');
  if (scrolly) {
    const labels = Array.from(scrolly.querySelectorAll<HTMLElement>('[data-scrolly-label]'));
    const screens = Array.from(scrolly.querySelectorAll<HTMLElement>('[data-scrolly-screen]'));
    const total = Math.max(labels.length, screens.length);

    function update() {
      const rect = scrolly!.getBoundingClientRect();
      const viewportH = window.innerHeight;
      const totalScrollable = scrolly!.offsetHeight - viewportH;
      const progressed = Math.min(Math.max(-rect.top, 0), totalScrollable);
      const ratio = totalScrollable > 0 ? progressed / totalScrollable : 0;

      const active = Math.min(Math.floor(ratio * total), total - 1);

      labels.forEach((label, i) => {
        label.classList.toggle('is-active', i === active);
      });
      screens.forEach((screen, i) => {
        screen.classList.toggle('is-active', i === active);
      });
    }

    update();
    window.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
  }

  const heroIcon = document.querySelector<HTMLElement>('[data-hero-icon]');
  if (heroIcon && !reduced) {
    heroIcon.addEventListener('mouseenter', () => heroIcon.classList.add('is-fanned'));
    heroIcon.addEventListener('mouseleave', () => heroIcon.classList.remove('is-fanned'));
  }

  // Converge headline observer.
  //
  // One-shot, intersection-triggered. When a `.converge-statement`
  // section is ~30% on screen with the headline visibly inside the
  // viewport, we add `is-visible` and the CSS handles the rest (left
  // word slides in from -100vw, right word from +100vw, body
  // materialises a beat later). Separate observer from the global
  // reveal IO because we want a stricter threshold — firing too
  // early would play the dramatic moment before the user can see it.
  const converges = document.querySelectorAll<HTMLElement>('.converge-statement');
  if (converges.length) {
    if (reduced || !('IntersectionObserver' in window)) {
      converges.forEach((el) => el.classList.add('is-visible'));
    } else {
      const convergeIO = new IntersectionObserver(
        (entries) => {
          for (const entry of entries) {
            if (entry.isIntersecting) {
              entry.target.classList.add('is-visible');
              convergeIO.unobserve(entry.target);
            }
          }
        },
        { threshold: 0.3, rootMargin: '0px 0px -10% 0px' },
      );
      converges.forEach((el) => convergeIO.observe(el));

      // Safety net: any converge section still hidden after 2.5s of
      // being painted gets revealed, mirroring the global reveal IO
      // fallback.
      window.setTimeout(() => {
        converges.forEach((el) => {
          if (!el.classList.contains('is-visible')) {
            el.classList.add('is-visible');
          }
        });
      }, 2500);
    }
  }
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}

export {};
