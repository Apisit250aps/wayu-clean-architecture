# Time handling

One rule set for dates, times, and time zones in every layer. Layer skills link here instead of repeating it. Adapt names to the repository's scope (`@<project>`).

## Principles

- Runtime values are the native `Date`, used as-is. `date-fns` and `@date-fns/tz` are plain functions applied to them; there is no wrapper type and no shared date utility package.
- Each package that needs date-fns declares `date-fns` and `@date-fns/tz` itself (same versions everywhere) and imports functions by name, like lodash. Do not create a shared wrapper, re-export, or `lib/time` module in Domain or anywhere else; Domain does not offer a date utility contract to other packages.
- Do not use Temporal or any second date library.
- Stored instants are UTC. A time zone is data (for example a site's `timezone`) or a named business default, never an implicit host or database setting.
- Business defaults such as `DEFAULT_TIME_ZONE` are domain constants (`constants/time.ts`), not helpers.
- Zone-free calendar dates and clock times are plain strings (`yyyy-MM-dd`, `HH:mm[:ss]`) validated at the boundary with Zod (`z.iso.date()`, `z.iso.time()`), not custom `LocalDate` types.

## Who reads the clock

| Layer       | Rule                                                                                                                                                                                                                                                                  |
| ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Domain      | Pure calculations receive `now`, `asOf`, and `timeZone` as arguments. No current-time reads (`new Date()` without input or `Date.now()`) in business rules; constructing a Date from an explicit value is allowed.                                                    |
| Application | A use case reads `new Date()` once per execution and passes it down. No clock port or injected clock service; unit tests use fake timers or assert the exact `now` passed to fakes.                                                                                   |
| Persistence | Repositories never read time. No `now()`, `clock_timestamp()`, `statement_timestamp()`, `current_date`, `Date.now()`, or `gt(col, new Date())` in queries. They receive `now`, `asOf`, and computed boundaries (for example `leaseExpiresAt`) as required parameters. |
| Web         | Only Web formats for display.                                                                                                                                                                                                                                         |

Exceptions: audit stamps written on mutation (`createdAt`/`updatedAt`/`deletedAt: new Date()`) and schema column defaults (`defaultNow()`) stay where they are.

Compute arithmetic (lease expiry, cutoffs) in the use case with date-fns (`addMilliseconds(now, ms)`), then pass the result to the repository. A guard such as "never extend an expired lease" compares against the passed `now` in SQL. Consequence to accept and document: the application host clock now decides leases, so multi-instance deployments need synchronized clocks (NTP).

Ports take required parameters, never optional `asOf` or a default that falls back to the database clock.

## Time zones in SQL

A per-row conversion from stored `date`/`time` columns to an instant may stay in SQL, but the zone is a bound parameter, never a literal:

```ts
sql`(${col.startDate}::timestamp) at time zone ${timeZone}`;
```

Postgres accepts IANA names. Fragments that embed the zone become functions of `timeZone` (`policySourceStart(timeZone)`), and the repository method receives `timeZone` from the use case. Prove the parameter is used with a test that runs a non-default zone and changes the result.

## Conversion recipes (backend and shared logic)

Use `const utc = tz("UTC")` for zone-free calendar math so the host `TZ` never leaks. Use `{ in: tz(zone) }` or `TZDate` only where a rule depends on a local calendar day.

| Need                                  | Replacement                                                                                                                                                                                                                                         |
| ------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Validate a date / time                | `z.iso.date()` / `z.iso.time()` (`isMatch` is lenient: it accepts `2026-1-01`)                                                                                                                                                                      |
| Validate an IANA zone                 | `isValid(new TZDate(0, zone))`                                                                                                                                                                                                                      |
| Add days/months/years to `yyyy-MM-dd` | `lightFormat(addDays(parseISO(d, { in: utc }), n), "yyyy-MM-dd")` (date-fns clamps month ends)                                                                                                                                                      |
| Difference in days                    | `differenceInCalendarDays(parseISO(b, { in: utc }), parseISO(a, { in: utc }))`                                                                                                                                                                      |
| Year / month / day of a date          | `getYear` / `getMonth(...) + 1` / `getDate` on `parseISO(d, { in: utc })`                                                                                                                                                                           |
| Weekday (ISO)                         | `getISODay(parseISO(d, { in: utc }))`                                                                                                                                                                                                               |
| Local date / time of an instant       | `lightFormat(new TZDate(value, zone), "yyyy-MM-dd")` / `"HH:mm"`                                                                                                                                                                                    |
| Minutes since local midnight          | `const t = new TZDate(value, zone); t.getHours() * 60 + t.getMinutes()`                                                                                                                                                                             |
| Today in a zone                       | `lightFormat(new TZDate(now, zone), "yyyy-MM-dd")` using the passed `now`                                                                                                                                                                           |
| Wall-clock time to instant            | `parse(\`${date} ${time}\`, "yyyy-MM-dd HH:mm", new Date(0), { in: tz(zone) })`                                                                                                                                                                     |
| DST gap / fold                        | Apply the explicit gap/fold policy for supported zones and round-trip the wall time. Do not assume all transitions are 30 or 60 minutes. Test the supported offset transitions; require an explicit `earlier`/`later` decision for ambiguous input. |
| UTC day key of an instant             | `lightFormat(new TZDate(value, "UTC"), "yyyy-MM-dd")`                                                                                                                                                                                               |

Serialize with `lightFormat` or `formatISO` only. Values computed in a zone flow on unconverted and may serialize with an offset (`+07:00`) instead of `Z`, so tests compare instants (`toEqual(new Date(...))`, `getTime()`), not ISO strings. Never cut date strings with `slice`, `substring`, or `split` (`split("T")`, `toISOString().slice(0, 10)`); parse and format instead. Parse zone-free values in UTC so a host DST gap cannot shift them.

## Display formatting (Web and UI only)

- One central formatter in the UI package owns every date shown to users. Features call it; they do not call `format`, `Intl.DateTimeFormat`, or `toLocale*String` themselves. Number formatting is not a date and may be exempt.
- Formatters take presets, not raw field options: `DATE_FORMATS.x = { patterns: { th, en } }` of date-fns patterns, and `options = { patterns?, timeZone? }`, so `{ ...DATE_FORMATS.time, timeZone }` composes. Add a preset when a screen needs a new shape instead of an inline pattern.
- Patterns are per language because word order differs (`d MMM yyyy` versus `MMM d, yyyy`). Map the app locale to a date-fns locale; keep the supported set explicit and fall back to one language for the rest.
- If the product shows a calendar date-fns lacks (for example Buddhist era), substitute the value as a quoted literal before `format` (a `{BE}` placeholder) rather than post-processing the output. Where ICU abbreviations differ from date-fns names, keep the browser-visible text through a placeholder as well.
- The display zone defaults to a display setting and is overridden by the data's own zone (site, assignment). Display zones are never saved or used to compute stored values.
- Strict calendar-date parsing: regex shape check, `parse(value, "yyyy-MM-dd", new Date(0), { in: utc })`, `isValid`, then a `lightFormat` round trip equal to the input.
- When replacing an `Intl`-based formatter, record the old outputs first (each preset × locales × several zones × edge instants such as midnight and year end), then assert the new formatter reproduces them. Keep a recorded subset as a unit test. Run Web tests under a second host zone (for example `TZ=America/New_York`).

## Enforcing with lint

Prefer small custom ESLint rules (one plugin, for example `time`) over growing `no-restricted-syntax`, which other configs may already own and silently override. Typical rules:

- `no-temporal`: forbid the Temporal package.
- `no-domains-time-lib`: forbid importing a domain date utility path, so a deleted helper cannot return.
- `no-display-format`: forbid date-fns display formatters (`format`, `formatDistance`, ...) outside Web/UI.
- `no-date-string-slice`: forbid `toISOString().slice(...)` and fixed `.slice(0, 10)` date cutting (relax only the literal slice check in tests).
- `no-repository-clock`: scoped to repository files; forbid clock SQL in template strings, `at time zone '<literal>'`, `Date.now()`, and comparison helpers called with `new Date()`. Audit-stamp `new Date()` must not match.

Register the plugin once; defining it twice for overlapping file globs fails with "Cannot redefine plugin". After adding a rule, add a temporary offending line, confirm the error, and remove it.

## Verification

- Type-check and lint every package that changed a port signature; a new required parameter breaks fakes in tests, so update them and assert the exact `now`/`timeZone` passed.
- Run repository tests against a real database when SQL changed, and compare against a baseline in an isolated checkout/source snapshot before attributing a pre-existing failure to the change. Preserve unrelated working-tree changes; do not stash them merely to run that comparison.
- Run date-sensitive tests under the default zone and a second zone.
- Do not claim screens display dates unchanged without either a browser check or recorded-output tests; ask before running browser tests when the task says so.
