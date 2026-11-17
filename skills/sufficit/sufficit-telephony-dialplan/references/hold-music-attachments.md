# Original audio for queue hold music

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
