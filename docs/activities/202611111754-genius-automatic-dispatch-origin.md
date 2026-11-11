# Mark automatic Genius catalog propagation

The Genius #1492 coordination policy initially distinguished only schedule and
repository_dispatch from manual dispatch. This repository actually notifies
Genius with `gh workflow run`, which creates workflow_dispatch. The real
notification therefore bypassed the original automatic guard. An isolated
two-repository fixture captured that request and reproduced an unwanted main
push with an open PR and a recent pin. No real push or credential was involved.

Commit c588658 adds `automatic=true` to the existing validated-main notification.
The revision, existing token, permissions and target remain unchanged. Two
versioned tests execute the real notification shell with isolated gh: automatic
revision propagation and the existing missing-token hourly-sync fallback. The
agent ran 47 tests and validated all 185 packages plus index, versions and
Markdown coverage successfully. No skill package or digest was changed.

Genius support for the boolean input was published first in main 21940247.
Manual Genius dispatch defaults to false and stays immediate. The correction
does not retroactively mark already-dispatched legacy requests. The origin of
Genius catalog commit 865503f0 was not proved and is not attributed here.

Publication and remote validation of this repository are separate from these
local checks; no Genius release or user-device acceptance is claimed.

Session: 01a1bc7b-9a8d-7571-97a0-a6b22cad0668.
