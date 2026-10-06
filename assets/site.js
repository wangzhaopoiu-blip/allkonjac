(() => {
  'use strict';

  const header = document.querySelector('header');
  const button = document.querySelector('.menu-toggle');
  const navigation = document.querySelector('#primary-navigation');
  const switchers = [...document.querySelectorAll('.language-switcher')];
  const desktop = window.matchMedia('(min-width:1101px)');
  const hasNavigation = Boolean(header && button && navigation);

  const setNavigationOpen = (open) => {
    if (!hasNavigation) return;
    button.setAttribute('aria-expanded', String(open));
    navigation.classList.toggle('is-open', open);
    const label = button.getAttribute(open ? 'data-label-close' : 'data-label-open');
    if (label) button.setAttribute('aria-label', label);
  };

  const closeSwitchers = (except) => {
    switchers.forEach((switcher) => {
      if (switcher !== except) switcher.open = false;
    });
  };

  if (hasNavigation) {
    button.addEventListener('click', () => {
      const open = button.getAttribute('aria-expanded') !== 'true';
      if (open) closeSwitchers();
      setNavigationOpen(open);
    });
    navigation.addEventListener('click', (event) => {
      if (event.target.closest('a')) setNavigationOpen(false);
    });
    setNavigationOpen(false);
    header.classList.add('nav-enhanced');
  }

  switchers.forEach((switcher) => {
    switcher.addEventListener('toggle', () => {
      if (switcher.open) {
        closeSwitchers(switcher);
        setNavigationOpen(false);
      }
    });
  });

  document.addEventListener('click', (event) => {
    switchers.forEach((switcher) => {
      if (!switcher.contains(event.target)) switcher.open = false;
    });
    if (hasNavigation && !button.contains(event.target) && !navigation.contains(event.target)) {
      setNavigationOpen(false);
    }
  });

  document.addEventListener('keydown', (event) => {
    if (event.key !== 'Escape') return;
    const switcher = switchers.find((item) => item.open && item.contains(document.activeElement));
    if (switcher) {
      event.preventDefault();
      switcher.open = false;
      switcher.querySelector('summary').focus();
    } else if (hasNavigation && button.getAttribute('aria-expanded') === 'true') {
      event.preventDefault();
      setNavigationOpen(false);
      button.focus();
    }
  });

  desktop.addEventListener('change', (event) => {
    const focusedElement = document.activeElement;
    const focusedSwitcher = switchers.find((item) => item.open && item.contains(focusedElement));
    setNavigationOpen(false);
    closeSwitchers();
    if (focusedSwitcher) focusedSwitcher.querySelector('summary').focus();
    if (!hasNavigation) return;
    if (event.matches && focusedElement === button) {
      const firstLink = navigation.querySelector('a');
      if (firstLink) firstLink.focus();
    } else if (!event.matches && navigation.contains(focusedElement)) {
      button.focus();
    }
  });

  // Shared motion applies to all business pages in all three languages.
  if (!document.body.classList.contains('motion-enabled')) return;
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (reducedMotion.matches || !('IntersectionObserver' in window)) return;

  const pending = new Set();
  let observer;
  const reveal = (element, immediate = false) => {
    if (!pending.delete(element)) return;
    if (immediate) {
      element.style.setProperty('--reveal-order', '0');
      element.classList.add('reveal-immediate');
    }
    element.classList.remove('is-pending');
    if (observer) observer.unobserve(element);
  };
  const finishReveals = () => {
    [...pending].forEach((element) => reveal(element, true));
    if (observer) observer.disconnect();
  };

  try {
    // Clip the zoom inside the existing image dimensions without changing assets.
    document.querySelectorAll('.feature-grid > img, .gallery > img, .case-grid > img, .global-grid > img, .detail-copy > img').forEach((image) => {
      const frame = document.createElement('div');
      frame.className = 'motion-image';
      if (image.classList.contains('big')) frame.classList.add('big');
      image.parentNode.insertBefore(frame, image);
      frame.appendChild(image);
    });

    observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) reveal(entry.target);
      });
      if (!pending.size) observer.disconnect();
    }, { rootMargin: '0px 0px -24px 0px', threshold: 0.08 });

    const targets = [...document.querySelectorAll([
      '.hero-copy > *', '.strip-item', '.section-top > *', '.card',
      '.feature-grid > *', '.technology-intro > .wrap > .text-link',
      '.gallery', '.caption', '.case-grid > *', '.global-grid > *',
      '.faq-list > details', '.contact-box > *', '.contact-card',
      '.page-hero > .wrap > :not(.breadcrumbs)', '.detail-copy > *',
      'main > section > .wrap > h2', '.business-summary', '.related-links',
      '.contact > .wrap > .eyebrow', '.contact > .wrap > p', '.contact > .wrap > .actions'
    ].join(','))];
    const sequenceGroups = '.hero-copy, .strip-grid, .grid4, .contact-info, .page-hero > .wrap';
    targets.forEach((element) => {
      const siblings = element.parentElement.matches(sequenceGroups)
        ? [...element.parentElement.children].filter((item) => targets.includes(item))
        : [element];
      element.style.setProperty('--reveal-order', String(Math.min(siblings.indexOf(element), 4)));
      element.setAttribute('data-reveal', '');
      pending.add(element);
      element.classList.add('is-pending');
      observer.observe(element);
    });

    // Keyboard navigation must never focus an invisible control.
    document.addEventListener('focusin', (event) => {
      if (event.target instanceof Element) {
        let target = event.target.closest('[data-reveal]');
        while (target) {
          reveal(target, true);
          target = target.parentElement ? target.parentElement.closest('[data-reveal]') : null;
        }
      }
    });
    reducedMotion.addEventListener('change', (event) => {
      if (event.matches) finishReveals();
    });
    window.addEventListener('beforeprint', finishReveals);
  } catch (_) {
    // A failed enhancement must leave the complete static page readable.
    finishReveals();
  }
})();
