# Instagram profile manage skill

Created `skills/instagram/instagram-profile-manage/` with a channel matrix (public read, Graph API, logged-in browser, app) per profile item, authentication rules, an approval-first apply order and post-change verification. `scripts/read_profile.sh` reads a profile without login (Open Graph tags, rendered text, screenshot) and was tested on @sufficitti. `instagram-profile-setup` links to it. Registered in catalog/manifest; README counts 170.

Validation: `scripts/validate.py` passed.
