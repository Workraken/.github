# Maintaining the organization profile

The public organization profile is `profile/README.md` (Spanish). The other five versions are linked from the circular flag selector.

Edit the translations in `i18n/profile.json`, then run:

```sh
python3 scripts/build_profiles.py
```

This regenerates all six READMEs and the twelve localized activity calendars. The calendar data is a dated snapshot in `profile/assets/activity-data.json`; regeneration does not fetch fresh activity or change the collection timestamp. Keep that timestamp tied to the actual data collection. The data contains aggregate counts only, including activity from private repositories.

Brand and contact assets remain in `Workraken/WorKraken`. The circular flags are copied from the Rey-de-Amarillo profile; their MIT attribution and license are in `profile/assets/flags/`.
