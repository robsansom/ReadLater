# Launch Checklist

Outstanding items for the Read Later website and App Store launch.

## Required before App Store launch

- [ ] Confirm `support@getreadlater.com` receives mail through the Eas ily alias.
- [ ] Decide how support replies will be sent without exposing a personal address.
- [ ] Replace the placeholder `#app-store` link in `src/config/site.ts` with the final App Store product URL.
- [ ] Confirm the published prices and limits: 50 free saves, GBP 12.99/year, and GBP 34.99 lifetime.
- [ ] Verify every Privacy Policy claim against the release build, especially analytics, crash reporting, CloudKit sharing, push notifications, AI features, and third-party SDKs.
- [ ] Verify the Terms of Use against the final purchase options and app behaviour.
- [ ] Add the website, support, and privacy-policy URLs in App Store Connect.

## Website and domain

- [ ] Wait for `getreadlater.com` and `www.getreadlater.com` DNS records to propagate.
- [ ] In GitHub Pages, run the domain check again after DNS propagation.
- [ ] Enable and verify HTTPS after GitHub provisions the certificate.
- [ ] Test the custom domain on iPhone, iPad, and desktop.
- [ ] Confirm all navigation, legal, email, and App Store links on the deployed site.
- [ ] Check the social preview image and metadata on the live HTTPS domain.

## Later

- [ ] Restore the testimonials section only when genuine reviews or approved tester quotes are available.
- [ ] Update legal-page dates whenever their wording changes.
