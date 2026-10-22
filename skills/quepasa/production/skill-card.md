# quepasa-production

Operate Sufficit's production QuePasa (WhatsApp gateway) on Kubernetes — check health, diagnose a session or a failed send, read logs and metrics, re-pair or restart a session, replay webhook dead letters, roll out or roll back a new image and handle Galera/Redis — with the grants each task needs and the rules that keep WhatsApp sessions from being corrupted. Use when the request is about the production QuePasa service itself (is it up, why a number stopped sending, deploy/rollback, failover), not just calling its API.

Version: **0.1.0** · Sufficit · MIT-0

Read [SKILL.md](SKILL.md) to use this skill.

Source: [sufficit-ai-skills](https://github.com/sufficit/sufficit-ai-skills/tree/main/skills/quepasa/production).
