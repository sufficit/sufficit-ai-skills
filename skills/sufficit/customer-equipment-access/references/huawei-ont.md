# Huawei ONT web access (EchoLife EG8145V5 and similar)

## Transport trap: HTTPS on port 80

Many units serve **HTTPS on port 80** (`SSLPort=80`) with an old certificate
and legacy TLS renegotiation. Symptoms: `http://ip/` redirects to
`https://ip:80/`; browsers show a privacy error; Python `requests`/`curl` fail
with `UNSAFE_LEGACY_RENEGOTIATION_DISABLED`; automated browsers land on
`chrome-error://`.

Use `curl -k` with a dedicated OpenSSL configuration, exported only for that
command:

```ini
# legacy-openssl.cnf
openssl_conf = openssl_init
[openssl_init]
ssl_conf = ssl_sect
[ssl_sect]
system_default = system_default_sect
[system_default_sect]
CipherString = DEFAULT@SECLEVEL=0
Options = UnsafeLegacyRenegotiation
```

```bash
export OPENSSL_CONF=/tmp/legacy-openssl.cnf   # only in this shell
B=https://<ip>:80
```

## Login

1. `GET $B/` to obtain the initial cookie, then get the login token with
   `POST $B/asp/GetRandCount.asp` (the body is the token). Pages after login
   refresh their token through `GET $B/html/ssmp/common/GetRandToken.asp`.
2. `POST $B/login.cgi` with `UserName=<user>`, `PassWord=<base64(password)>`,
   `Language=english`, `x.X_HW_Token=<token>`, keeping a cookie jar and the
   cookie `Cookie=body:Language:english:id=-1;path=/`.
3. Success: `GET $B/index.asp` returns the menu (Home Page, One-Click Diagnosis,
   System Information, Advanced). A login page again means wrong credentials or
   token — stop after two failures; the unit locks out repeated attempts.

Operator accounts vary by ISP (`Epadmin`, `telecomadmin`, `root`…). Use the one
the customer gave; never guess default passwords.

## VoIP pages

The "Voice" menu loads pages under `html/voip/`, not `voice.asp`/`voip.asp`
(those return 404 or a JS shell):

- `html/voip/voipinterface/voipinterface.asp` — SIP server, ports, the line
  (Register User Name, Auth User Name, password masked, **URI**, enable).
- `html/voip/voipuser/voipuser.asp` — per-line user/codec settings.
- Status/diagnosis pages show line status (`Up`/`Idle`) and `RegisterError`.

Every page carries a fresh hidden token: `<input name="onttoken" id="hwonttoken" value="…">`.

## Writing a field

The page builds a form posted to `set.cgi?` (or `complex.cgi?` for server
profile changes) with object paths in the query and `<prefix>.<Field>` pairs in
the body, plus `x.X_HW_Token=<onttoken>` taken from **the page you just
loaded**. For the SIP line the relevant body fields are `c.AuthUserName`,
`c.URI` (and `c.AuthPassword` only when changing the password — the masked
`****` value must never be posted back) and `Add_b.DirectoryNumber`.

Practical rules:

- Read the page, extract its `ActionURL` construction and the line's object
  path (e.g. `InternetGatewayDevice.Services.VoiceService.1.VoiceProfile.1.Line.1`)
  from the JavaScript instead of guessing.
- Use the token of the same page load; a stale token returns an error such as
  `0x1` and nothing is saved.
- Post only the fields you change plus the token.
- Re-read the page and confirm the value persisted.

## The field that breaks registration

On these units the **URI** field of the SIP line is used as the identity in
REGISTER/authorization. If it holds the server domain (e.g. the PBX host name)
the central receives `AccountID=<domain>` and answers `InvalidPassword` even
with the right password. Set URI, Register User Name and Auth User Name to the
extension number (chan_sip legacy) or the endpoint login (PJSIP).
