# Original audio for queue hold music

## Hold music is not a greeting

| Requested effect | Resource and queue field | Correct verification |
| --- | --- | --- |
| Music while the caller waits | Music-on-hold class, queue options.musicClass | Owned class, its track listing and the effective queue class |
| One greeting when entering the queue | Sound/announcement, options.greeting | Greeting resource/destination; this does not configure hold music |
| Message played to the answering agent | Sound, options.agentAnnouncement | Agent announcement; it is not the caller's hold music |
| Announcement repeated during waiting | Sound, options.periodicAnnouncement | Its interval/policy; it does not replace the music class |

For “música de espera”, upload through the music-on-hold API to the verified
customer-owned class. Do not register the attachment only as a sound/greeting,
point an announcement destination at it or change greeting/agentAnnouncement/
periodicAnnouncement to simulate music. An audio ID and a music-class ID are
separate identities even though both may be GUIDs. Do not assume classId equals
contextId: confirm the actual class owner and queue association from the API.
A greeting upload receipt is not evidence of a music-on-hold upload. Preserve
existing greeting, announcement, destinations and other queue options.

Read [the customer-write context guard](../../sufficit-api/references/customer-write-context.md)
before any mutation, including an upload whose endpoint accepts only classId.

## Format and playback

A container, filename extension or successful upload does not prove playback.
A reported live incident involved WhatsApp OGG/Opus accepted by the upload API but
not playable as OGG by that PBX; WAV conversion was followed by a successful
caller test. Treat this as evidence to check the actual codec/deployed support,
not a claim that every PBX rejects every OGG. Renaming .ogg to.wav is not conversion.

Prefer the supported API's validated/converted telephony artifact. A conservative
prepared-file recipe uses uncompressed PCM16 WAV, mono8kHz. Preserve the source
identity/hash and record conversion and the upload artifact's separate hash.
Do not claim that the current additive helper converts: it validates the file's
signature/hash and uploads bytes; it does not transcode. If a necessary conversion
or codec check is absent from N1 APIs, name that integration gap and retain the
request; do not use SSH/Asterisk commands, upload a greeting instead, ask for the
same original again or declare playback from an API200. Never delete a working
track as a diagnostic experiment. Replacement/removal needs its own request.

## N1 API-only procedure

Adding customer-provided queue hold music is first-level telephony support when
the agent has the deployed API operation and authority for that validated customer.
Use only authenticated APIs and original-attachment export through the channel
integration. No SSH, SQL, direct PBX files or FreePBX commands belong to this
procedure. The same recipe applies to N1 and N2 agents; their actual customer
scope, audience and permissions remain distinct.

The [N1 agent briefing](../agents/n1-hold-music.md) is a compact Portuguese
training payload for customer-facing agents. Install it through managed training;
a public package update does not replace an already-pinned executor version.

If API synchronization or playback cannot be verified with available API tools,
report the exact pending evidence and use the configured private specialist
consultation. Missing equipment does not turn routine API work into a database
or infrastructure task, and a training installation grants no API privilege.

Start with an authorized request and the explicit customer context. Inspect the
requested queues and their current music class before writing. When the request
covers the customer's queues without exceptions and all share one customer-owned
class, adding to that class fulfils the scope without changing queue assignments.
Do not ask which queues again in that case. A request for one queue does not
permit affecting unrelated queues or a global default class.

A chat history entry saying an audio was saved under `anexos/...` means an original
was stored separately from recognition. In Fleet, workspace `read` in default text
mode returns recognition. Use `format="file"` to copy original bytes to the agent's
executor and obtain `localPath`, `size` and `sha256`. A recognition such as
“[música suave]” is not an audio file and does not mean the attachment is missing.

When the installed authenticated support-api helper supports it, create a JSON
manifest with `upload="music_on_hold_add"`, the real `contextId`, owned music
`classId`, exported local path in `file`, and the original `sha256`. Submit it via
`endpoints POST /Telephony/moh/Audio <manifest-file>` using the normal user
credential. Installed instructions are at `/data/support/api-client/README.md`.
`validateOnly=true` checks the source/class without an upload. The helper accepts
OGG/WAV/MP3/FLAC, verifies context and content and uses a deterministic content
name. It preserves existing tracks and reconciles a repeated title without
another upload; it does not delete, replace or change queue assignments.

“Adicionar” means add and preserve current tracks. Replacement needs an explicit
replacement request and the corresponding supported operation; never purge a
class to add one track. A separate recording catalog approval is not a prerequisite
unless the actual deployed workflow requires it. If original export or multipart
is unavailable, report the missing internal capability precisely; do not claim
that no file exists or that the person must upload it again by default.

After an accepted upload, independently re-read the file listing. Keep API
acceptance, listed storage object, asynchronous PBX synchronization and actual
playback separate. Existing classes may load on demand; absence from a live class
list alone is not proof of missing audio. After a lost reply, reconcile the same
content name; do not choose a fresh name and duplicate the track.
