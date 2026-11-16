<!-- DRAFT (prompt 115, 2026-11-16): reference form of features/account-auth/F-109-registration.md. The live page is unchanged until QA accepts this one. Links to other pages point at features/ from this folder. -->
# F-109 — Registration

**Status:** Available on iOS and Android. Not available on Web: the web app asks the user to install the mobile app.
**Last updated:** 2026-11-16 (draft)

## Purpose

A person whose phone number has no Call.com account creates one in the mobile app. They confirm the number with an SMS code, enter a name and an email, and click the link in the confirmation email. The app then signs them in and shows onboarding ([F-110](../../features/account-auth/F-110-onboarding-get-a-number.md)).

## Quick overview

- New number on a phone: SMS code → "Create your account" → "Confirm your e-mail" → link in the email → signed in, onboarding — [Start with a new number](#start-with-a-new-number), [Fill in the form](#fill-in-create-your-account), [Confirm the email](#confirm-the-email)
- Web: no registration, store badges instead — [S04](#s04--web-install-the-mobile-app)
- Mistyped address, lost email, wrong code — [Fix a mistake](#fix-a-mistake)
- The user stops halfway and comes back — [Interrupted registration](#interrupted-registration)

## Availability

- iOS and Android only. On Web the user is asked to install the mobile app ([S04](#s04--web-install-the-mobile-app)).
- Signed out, with a number that has no finished account (see [States](#states)).

## Entry points

- Welcome → "Continue" → "Login / Register" → a number with no account → "Login".

## How it works

Status marks: ✓ Verified (QA, date) · Known issue · Described from code (not testable by QA) · Not verified.

### Start with a new number

- <a id="s01--start-with-a-new-number-and-confirm-it"></a>**S01** — When, on a phone and signed out, the user enters a number with no account (or an unfinished registration, [S11](#s11--registration-left-unfinished)) on "Login / Register" and taps "Login" ([F-105](F-105-log-in-with-phone-number.md)) → the SMS is sent at once; the 6-digit code from the SMS or voice call ([F-106 S01](../../features/account-auth/F-106-login-code-sms-voice.md#s01--new-user-confirms-the-phone-number-ios-and-android)) opens "Create your account", with the cursor in "Full name". ✓ Verified (QA, 2026-11-13)
- <a id="s04--web-install-the-mobile-app"></a>**S04** — When, on Web and signed out, the user enters a number with no finished account and taps "Login" → no SMS is sent; the "Register" screen shows "To register an account with Call.com you need to install our mobile phone app." and App Store and Google Play badges, which open the Call.com store pages. Back returns to the phone-number screen. ✓ Verified (QA, 2026-11-13)

### Fill in "Create your account"

The screen has:
- "Full name", caption "The name other Call.com users will see";
- "E-mail", caption "We need your e-mail address to send you future verification codes and service information.";
- the marketing consent checkbox ([S15](#s15--marketing-consent-on-the-registration-screen)); its text can be tapped too;
- "Continue".

Field checks: [Rules & limits](#rules--limits).

- <a id="s02--fill-in-the-registration-form"></a>**S02** — When the user enters a full name and an email (newsletter optional) and taps "Continue" (or the keyboard's done key in the email field) → "Confirm your e-mail" opens with "We sent a confirmation e-mail to:", the address as typed, and "Check your e-mail and click on the confirmation link to continue." ✓ Verified (QA, 2026-11-13)
- <a id="s17--loading-after-continue-one-email-only"></a>**S17** — When "Continue" is tapped twice quickly → a loading indicator shows after "Continue"; only one confirmation email arrives. ✓ Verified (QA, 2026-10-16; QA, 2026-11-13)
- <a id="s15--marketing-consent-on-the-registration-screen"></a>**S15** — Under "E-mail" there is the marketing consent "Subscribe to product updates, tips, and occasional calling credits in select campaigns. No spam. Unsubscribe anytime." It is off (unticked) by default for a new account. ✓ Verified (QA, 2026-09-30; QA, 2026-11-13)

"Confirm your e-mail" shows an envelope icon, the S02 texts, "Resend e-mail" and a back arrow. There is no code field and no "change email" button ([S08](#s08--change-the-email-address)). No time limit is shown on this screen.

### Confirm the email

- <a id="s14--the-confirmation-email-arrives"></a>**S14** — After S02 → an email arrives at the address typed, from "Call.com Support" <support@call.com>, subject "Call.com Email Verification", with "Welcome <name>"; "You have successfully created a Call.com account. Please confirm your email address by clicking the link below."; a green button "CONFIRM"; "Kind Regards", "The Call.com Team"; the footer "© 2023 Call.com. All rights reserved. Privacy & Terms". The link stops working once it has been used. ✓ Verified (QA, 2026-09-30; QA, 2026-11-13)

  ![Registration email "Call.com Email Verification" from Call.com Support: "Welcome" with the test account name, the confirmation text, a green "CONFIRM" button, "Kind Regards", "The Call.com Team" and the footer](../../features/account-auth/img/registration-email.png)
- <a id="s03--confirm-the-email-and-get-signed-in"></a>**S03** — When the app stays on "Confirm your e-mail" and the user clicks "CONFIRM" (on this phone or another device) → within about 5 seconds the app leaves the screen by itself, signs in and shows "Thank you for creating your account" ([F-110 S01](../../features/account-auth/F-110-onboarding-get-a-number.md#s01--the-welcome-screen-after-registration)). The browser opens a Call.com page: "Success! Verification of your email address is complete." and "Please close this page and return to the Call.com app." ✓ Verified (QA, 2026-11-13)
- <a id="s16--click-the-confirm-link-a-second-time"></a>**S16** — When "CONFIRM" in the same email is clicked again → the browser shows an error page: "Sorry!", "This verification link has been used and is no longer valid." and "Please check you have used the link from the latest email." ✓ Verified (QA, 2026-10-16; QA, 2026-11-13)
- <a id="s13--migrated-user-form-after-registration"></a>**S13** — When the email has just been confirmed and the user's own sign-in number still has the "migrated" status → the migrated-user form "Create your account" ([F-111](../../features/account-auth/F-111-migrated-user-onboarding.md)) opens first, before onboarding ("Thank you for creating your account", S03). Otherwise onboarding opens at once. The status comes from an external service: registering does not set it and does not clear it. ✓ Verified (QA, 2026-10-16; QA, 2026-11-13)

## States

What happens when the number is entered on "Login / Register", by the state of its registration. A number counts as new until both the phone and the email are confirmed.

| State of the number | What the user gets |
|---|---|
| No account | SMS code, then an empty "Create your account" (S01) |
| Registration not finished (the email link was not clicked) | Registration starts again: SMS code, then an empty form (S11) |
| Email link clicked after the app was closed | Email code, like an existing user; no "Thank you" screen (S12) |

## Rules & limits

| User action | What happens |
|---|---|
| Taps "Continue" with an empty field, a name over 50 characters or a wrong email | Nothing is sent; the field turns red ([S06](#s06--form-not-filled-in-correctly)) |
| Types an email with spaces at its start or end | The spaces are removed |
| Ticks the marketing checkbox | Turns on Settings → Notifications → "Email notifications" → "Call.com information" ([F-123](../../features/notifications/F-123-notification-settings.md)) |
| Taps "Resend e-mail" | A new email each time; no countdown and no limit ([S07](#s07--resend-the-confirmation-email)) |
| Clicks "CONFIRM" a second time | The link works only once: the "Sorry!" page ([S14](#s14--the-confirmation-email-arrives), [S16](#s16--click-the-confirm-link-a-second-time)) |
| Types wrong SMS codes | No limit today (known issue CALLCOM-5249, [S05](#s05--wrong-or-too-many-sms-codes)) |

- "Full name" and "E-mail" are required. The name has at most 50 characters.
- The email must look like name@domain.xx, with at least 2 letters at the end.
- "Push notifications" → "Call.com information" is on for every new account.
- Once the link from a newer email has been used, the link in an older email must no longer work ([S18](#s18--link-in-the-older-email-after-resend-e-mail); known issue: today it still shows "Success!").
- A sign-up attempt stays valid for 24 hours ([F-105](F-105-log-in-with-phone-number.md), Rules & limits); after that: [S09](#s09--sign-up-session-ran-out), [S20](#s20--sms-code-typed-after-the-sign-up-session-ran-out).

## Errors & edge cases

### Fix a mistake

- <a id="s06--form-not-filled-in-correctly"></a>**S06** — When a field is empty, the name is over 50 characters, or the email has no "@" or domain, and the user taps "Continue" → nothing is sent; the wrong field and its caption turn red; no error text is shown. ✓ Verified (QA, 2026-11-13)
- <a id="s08--change-the-email-address"></a>**S08** — When the address was mistyped and the user taps the back arrow on "Confirm your e-mail", corrects "E-mail" and taps "Continue" → name and checkbox keep their values; the email goes to the new address, which is shown on "Confirm your e-mail". ✓ Verified (QA, 2026-11-13)
- <a id="s07--resend-the-confirmation-email"></a>**S07** — When "Resend e-mail" is tapped → a new email goes to the same address and "Success" appears. The app has no countdown and no limit. Older links: S18. ✓ Verified (QA, 2026-11-13)
- <a id="s18--link-in-the-older-email-after-resend-e-mail"></a>**S18** — When "Resend e-mail" was tapped (S07), the link in the newer email was clicked, and then "CONFIRM" in the first email is clicked → expected: the link no longer works; the browser shows "Sorry!", "This verification link has been used and is no longer valid." and "Please check you have used the link from the latest email." **Actual:** the browser shows "Success! Verification of your email address is complete." and "Please close this page and return to the Call.com app." Known issue — reported by QA to the owners of the verification page, 2026-11-14 (no Jira ticket: the page belongs to an external service).
- <a id="s05--wrong-or-too-many-sms-codes"></a>**S05** — When wrong codes are typed on the registration code screen → "Failed code" appears; the boxes are emptied for a new try. Too many wrong codes: no limit today — known issue [CALLCOM-5249](https://norselab.atlassian.net/browse/CALLCOM-5249), see [F-106 S13](../../features/account-auth/F-106-login-code-sms-voice.md#s13--too-many-wrong-codes-during-registration). ✓ Verified (QA, 2026-11-14)

### The sign-up attempt ran out (24 hours)

- <a id="s20--sms-code-typed-after-the-sign-up-session-ran-out"></a>**S20** — When, on a phone, the registration code screen was left open for more than 24 hours and the user types the code from the SMS → "Session timeout" appears and "Login / Register" opens. Described from code.
- <a id="s09--sign-up-session-ran-out"></a>**S09** — When the form or "Confirm your e-mail" was left open for more than 24 hours and the user taps "Continue" or "Resend e-mail" → "Session timeout" appears and "Login / Register" opens. After "Resend e-mail" only the error appears, no "Success" (S19). Described from code.
- <a id="s19--resend-e-mail-fails-only-the-error"></a>**S19** — When "Resend e-mail" fails (for example after the sign-up session ran out) → only the error message appears; "Success" is not shown. ✓ Verified (QA, 2026-10-16; QA, 2026-11-13)

### Interrupted registration

- <a id="s11--registration-left-unfinished"></a>**S11** — When the app was closed before the email link was clicked and the user opens it and enters the same number → registration starts again with an SMS code (S01); after the code, "Create your account" opens empty: no name, no email, newsletter checkbox unticked. ✓ Verified (QA, 2026-11-14)
- <a id="s12--email-link-clicked-after-closing-the-app"></a>**S12** — When the app was closed on "Confirm your e-mail", the link was then clicked, and the user opens the app and enters the same number → the user is asked for an email code, like an existing user ([F-107](../../features/account-auth/F-107-login-code-email.md)); "Thank you for creating your account" is not shown. ✓ Verified (QA, 2026-10-16; QA, 2026-11-14)

### Registration cannot start

- <a id="s10--registration-cannot-start"></a>**S10** — When, on a phone, the SMS code cannot be sent to the new number after "Login" → an error is shown and registration does not start: no SMS code screen opens; the screen stays open, and "Login" can be tapped again. Described from code. _Error texts — after the error-handling rework._

## Platform differences

| What | Web | iOS | Android |
|---|---|---|---|
| Registration | Store badges only (S04) | Form and email link (S01–S03) | Same as iOS |
| Age check during registration: its block screen can appear ([F-117](../../features/account-auth/F-117-age-restriction.md)) | No | Yes | Yes |

## QA checklist

- [ ] New number on a phone: SMS code, the form, "Confirm your e-mail" (S01, S02, S17)
- [ ] The email and its link: signed in, onboarding; the link used twice shows "Sorry!" (S14, S03, S16)
- [ ] Form checks and the marketing checkbox (S06, S15)
- [ ] "Resend e-mail", changing the address, failed resend (S07, S08, S19); retest the older link after resend (S18)
- [ ] Wrong SMS codes; retest [CALLCOM-5249](https://norselab.atlassian.net/browse/CALLCOM-5249) (S05, [F-106 S13](../../features/account-auth/F-106-login-code-sms-voice.md#s13--too-many-wrong-codes-during-registration))
- [ ] Registration left unfinished, or the link clicked after closing the app (S11, S12)
- [ ] Web: install message and store badges (S04)
- [ ] SMS code cannot be sent: an error, registration does not start (S10)

## Known issues & open questions

**Known issues**
- [CALLCOM-5249](https://norselab.atlassian.net/browse/CALLCOM-5249) — No limit on wrong SMS codes during registration (S05; [F-106 S13](../../features/account-auth/F-106-login-code-sms-voice.md#s13--too-many-wrong-codes-during-registration)). Confirmed by QA, 2026-10-16.
- External verification service (no Jira ticket) — After "Resend e-mail" and "CONFIRM" in the newest email, "CONFIRM" in the first email still shows "Success! Verification of your email address is complete."; expected: "Sorry!" and "This verification link has been used and is no longer valid." (S18). Reported by QA to the owners of the verification page, 2026-11-14.

**Open questions** — None · **Not verified yet** — None

**Described from code (not testable by QA):** S09, S10, S20

**Error texts — after the error-handling rework:** S10

## Related features

- [F-105 — Log in with a phone number](F-105-log-in-with-phone-number.md) — the step that starts registration
- [F-106 — Login code by SMS or voice call](../../features/account-auth/F-106-login-code-sms-voice.md) — phone confirmation
- [F-110 — Onboarding: get a number](../../features/account-auth/F-110-onboarding-get-a-number.md) — opens after the email is confirmed
- [F-111 — Migrated-user onboarding](../../features/account-auth/F-111-migrated-user-onboarding.md) — same form (S13)
- [F-117 — Age restriction](../../features/account-auth/F-117-age-restriction.md) — can block registration
- [F-123 — Notification settings](../../features/notifications/F-123-notification-settings.md) — shows the marketing choices
