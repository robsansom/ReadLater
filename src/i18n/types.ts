export interface TranslationSchema {
  meta: {
    title: string;
    description: string;
  };
  header: {
    features: string;
    support: string;
    download: string;
  };
  footer: {
    taglineEyebrow: string;
    taglineHeadline: string;
    taglineHeadlineDim: string;
    copyright: string;
    appleAffiliation: string;
    appleTrademarks: string;
    product: string;
    company: string;
    legal: string;
    features: string;
    download: string;
    support: string;
    contact: string;
    privacy: string;
    terms: string;
  };
  hero: {
    eyebrow: string;
    title: string;
    titleAccent: string;
    body: string;
    badgeLabel: string;
  };
  showcaseQuickSave: {
    eyebrow: string;
    headline: string;
    headlineAccent: string;
    body: string;
    imageAlt: string;
  };
  showcaseLibrary: {
    eyebrow: string;
    headline: string;
    headlineAccent: string;
    body: string;
    imageAlt: string;
  };
  showcaseIpad: {
    eyebrow: string;
    headline: string;
    headlineAccent: string;
    body: string;
    imageAltDark: string;
    imageAltLight: string;
  };
  showcaseCollections: {
    eyebrow: string;
    headline: string;
    headlineAccent: string;
    body: string;
    imageAlt: string;
  };
  splitHeadlinePrivacy: {
    eyebrow: string;
    first: string;
    second: string;
    body: string;
  };
  bento: {
    eyebrow: string;
    headline: string;
    headlineAccent: string;
    body: string;
    shareExtension: {
      eyebrow: string;
      title: string;
      body: string;
      alt: string;
    };
    collections: {
      eyebrow: string;
      title: string;
      body: string;
      alt: string;
    };
    find: {
      eyebrow: string;
      title: string;
      body: string;
      alt: string;
    };
    makeItYours: {
      eyebrow: string;
      title: string;
      body: string;
      alt: string;
    };
    privacy: {
      eyebrow: string;
      title: string;
      body: string;
      alt: string;
    };
    export: {
      eyebrow: string;
      title: string;
      body: string;
      alt: string;
    };
  };
  integration: {
    eyebrow: string;
    headline: string;
    headlineAccent: string;
    body: string;
    spotlight: {
      eyebrow: string;
      title: string;
      body: string;
    };
    siri: {
      eyebrow: string;
      title: string;
      body: string;
    };
    shortcuts: {
      eyebrow: string;
      title: string;
      actions: string[];
    };
  };
  privacyPage: {
    metaTitle: string;
    metaDescription: string;
    eyebrow: string;
    headline: string;
    headlineDim: string;
    lastUpdated: string;
    intro: string;
    promisesTitle: string;
    promises: string[];
    sections: {
      title: string;
      body: string;
    }[];
  };
  supportPage: {
    metaTitle: string;
    metaDescription: string;
    eyebrow: string;
    headline: string;
    headlineDim: string;
    intro: string;
    contactTitle: string;
    contactButton: string;
    faqTitle: string;
    faqs: {
      q: string;
      a: string;
    }[];
  };
  termsPage: {
    metaTitle: string;
    metaDescription: string;
    eyebrow: string;
    headline: string;
    headlineDim: string;
    lastUpdated: string;
    intro: string;
    tldrTitle: string;
    tldr: string[];
    sections: {
      title: string;
      body: string;
      bullets?: string[];
      link?: {
        label: string;
        href: string;
      };
    }[];
  };
}
