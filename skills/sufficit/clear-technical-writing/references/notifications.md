# Human-readable operational notifications

Use for incident notices, support requests and status updates sent to people by chat or email. This is writing guidance, not authorization to send or resend.

## Build around the recipient's task

- Start with a short, specific title and a personal greeting. State the problem and requested help early.
- Put the impact and main finding before diagnostic details. A contact who forwards the case needs a different level of detail from the engineer who investigates it.
- Separate context, key findings and requested action with blank lines. Use short section labels when they help scanning. Do not send a report compressed into one paragraph.
- Highlight only the few values or conclusions that determine the next action. Use bullets for parallel findings; do not bold whole paragraphs.
- Keep essential identifiers (affected endpoints, time window, reference) together in a compact block. Move packet counts, full routes, interface counters, hashes, logs and reproduction commands to a report or attachment unless the recipient needs them immediately.
- Explain unfamiliar terms on first use, or use everyday language: “packets did not arrive” instead of a sequence of NIC/UDP/RTT/pcap acronyms. Retain exact technical identifiers in the supporting evidence.
- End with an answerable request: what to check, who should coordinate, and whether a protocol or expected response time is needed. Do not invent a deadline or demand an SLA not agreed with the recipient.
- Keep measurement date/time and uncertainty visible. Historical measurements must not read as a live outage. Distinguish the affected route from proven responsibility.

## Match the channel

WhatsApp: use a standalone `*Short title*`, optional `*Section labels*`, real line breaks, blank lines and simple `- ` bullets. Avoid Markdown `#` headings, tables, HTML, or `**double-asterisk**` formatting. Use emphasis sparingly. The JSON serializer encodes real newlines; do not put literal backslash-n text in the message. Do not send screenshots of text to simulate formatting.

Email: use a meaningful subject and a readable plain-text body with short labels and blank lines; if HTML is supported, keep the plain-text alternative. Attach detailed evidence and mention what each attachment contains. Do not claim an attachment was sent unless it actually accompanies the message.

Do not split a notification into several sends merely to create sections. Prefer one readable message and an attachment/link for detail; follow the recipient's established conversation when available.

## Pre-send editorial check

Read the exact outgoing text after templating and before the authorized send:

1. Can the recipient identify the problem, timing and requested action at a glance?
2. Are there visible paragraph breaks and a clear title for a multi-part notice?
3. Are the numbers, direction, units and confidence faithful to the evidence?
4. Does the first block work without specialist knowledge? Are necessary technical details accessible separately?
5. Does the channel support the formatting used? Is the final request easy to answer?

For a screenshot complaint, identify the visible defect and repair the reusable template/instructions. Do not edit or resend an existing external message unless requested. A preview is not proof of rendering on the recipient's device; say which validation was actually performed.

## Example (fictional, formatting preview only)

```text
*Network issue — Site A → Site B*

Hello, Alex. Could you help investigate packet loss on this route?

*What we found*
- About 17% of packets did not arrive from A to B.
- In the reverse direction, all test packets arrived.
- The VPN was also affected during the measurement.

*Measurement window*
28 October, 22:30–22:34 (UTC−03:00).
These are the results from that window, not a new measurement.

*Requested action*
Please check the incoming route and coordinate with the other provider. Can you confirm receipt and share a ticket number and expected response time?

The detailed report is available for technical analysis. We have not yet identified which provider is responsible for the packet loss.
```
